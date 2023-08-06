from libpyvinyl.BaseCalculator import BaseCalculator, CalculatorParameters
from libpyvinyl.Parameters.Parameter import Parameter
import Shadow
import inspect
import numpy

class Shadow3Calculator(BaseCalculator):
    def __init__(self,
                 name,
                 parameters=None,
                 dumpfile=None,
                 input_path=None,
                 output_path=None):

        super().__init__(name,
                         parameters=parameters,
                         dumpfile=dumpfile,
                         output_path=output_path)

        self.number_of_optical_elements = 0

    def setParams(self,
            source=None,
            beamline=[],
            number_of_optical_elements = 0,
            json=None,
            ):

        #
        # native format from json
        #
        if json is not None:
            self.parameters = CalculatorParameters.from_json(json)
            names = []
            for parameter in self.parameters:
                names.append(parameter.name)

            number_of_optical_elements = 0
            for i in range(1,100):
                if ("oe%d.DUMMY" % i) in names:
                    number_of_optical_elements += 1
            self.number_of_optical_elements = number_of_optical_elements  # todo automatize counted for json files
            return

        #
        #
        #
        self.number_of_optical_elements = number_of_optical_elements # todo automatize counted for json files
        # source
        if isinstance(source, Shadow.Source):
            oe0 = source
        else:
            oe0 = Shadow.Source()

        oe0_dict = oe0.to_dictionary()

        if not isinstance(self.parameters, CalculatorParameters):
            self.parameters = CalculatorParameters()

        for key in oe0_dict.keys():
            self.parameters.new_parameter("oe0."+key)
            value = oe0_dict[key]
            if isinstance(oe0_dict[key], bytes):
                value = value.decode("utf-8")

            self.parameters["oe0."+key] = (value)

        # beamline
        if len(beamline) == 0 and number_of_optical_elements > 0:
            beamline = [Shadow.OE()] * number_of_optical_elements

        for i in range(len(beamline)):
            if isinstance(beamline[i], Shadow.OE):
                oe_i = beamline[i]
            else:
                oe_i = Shadow.OE()

            oe_i_dict = oe_i.to_dictionary()

            if not isinstance(self.parameters, CalculatorParameters):
                self.parameters = CalculatorParameters()

            for key in oe_i_dict.keys():
                self.parameters.new_parameter("oe%d.%s" % (i+1, key))
                value = oe_i_dict[key]
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
                elif isinstance(value, numpy.ndarray):
                    value_new = []
                    for list_item in value:
                        if isinstance(list_item, bytes):
                            list_item = list_item.decode("utf-8")
                        value_new.append(list_item)
                    value = numpy.array(value_new)


                self.parameters["oe%d.%s" % (i+1, key)] = value



    def __get_valiable_list(self, object1):
        """
        returns a list of the Shadow.Source or Shadow.OE variables
        """
        mem = inspect.getmembers(object1)
        mylist = []
        for i,var in enumerate(mem):
            if var[0].isupper():
                mylist.append(var[0])
        return(mylist)

    def backengine(self,write_start_files_root=None):
        beam = Shadow.Beam()
        oe0 = Shadow.Source()


        oe0_list = self.__get_valiable_list(oe0)

        for name in oe0_list:
            try:
                value = self.parameters["oe0."+name].value
                if isinstance(value, str):
                    value = bytes(value, 'UTF-8')
                setattr(oe0, name, value)
            except:
                raise Exception("Error setting parameters name %s" % name)

        if write_start_files_root is not None:
            oe0.write(write_start_files_root + ".00")
        beam.genSource(oe0)

        if self.number_of_optical_elements > 0:
            oei_list = self.__get_valiable_list(Shadow.OE())
            for i in range(self.number_of_optical_elements):
                oe_i = Shadow.OE()
                for name in oei_list:
                    try:
                        value = self.parameters["oe%d.%s" % (i+1, name)].value
                        if isinstance(value, str):
                            value = bytes(value, 'UTF-8')
                        elif isinstance(value, numpy.ndarray):
                            for list_item in value:
                                if isinstance(list_item, str):
                                    list_item = bytes(list_item, 'UTF-8')
                        setattr(oe_i, name, value)
                    except:
                        raise Exception("Error setting parameters name %s" % name)

                if write_start_files_root is not None:
                    oe_i.write("%s.%d" % (write_start_files_root, i+1))
                beam.traceOE(oe_i, i+1)

        self._set_data(beam)
        return 0


    def dump(self,filename="star.01"): # overwritten method
        self.data.write(filename)

    def saveH5(self, filename="tmp.h5", openpmd=False):
        from orangecontrib.panosc.shadow.util.openPMD import saveShadowToHDF
        saveShadowToHDF(self.data, filename=filename)



if __name__ == "__main__":
    calculator = Shadow3Calculator("")

    ### Setup the parameters
    calculator.setParams(number_of_optical_elements=1)


    ### Run the backengine
    calculator.backengine()

    ### Plot results using ShadowTools
    try:
        from srxraylib.plot.gol import set_qt
        set_qt()
    except:
        pass

    Shadow.ShadowTools.plotxy(calculator.data, 1, 3, nbins=101, nolost=1, title="Real space")
