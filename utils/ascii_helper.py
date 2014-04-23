""" Ascii 1D/2D LUT helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.2"
from utils.abstract_lut_helper import AbstractLUTHelper
import utils.lut_presets as presets
from utils.color_log_helper import print_error_message, print_success_message


class AsciiHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


class AsciiLutHelper(AbstractLUTHelper):
    """ Simple Ascii 1D/2D LUT.
        Supported by Scratch and others
        Looks Like :
        #Mikros LutUtils export
        LUT: 3 1024
        <r value>
        <r value>
        (...)
        <g value>
        <g value>
        (...)
        <b value>
        <b value>
        (...)

    """
    @staticmethod
    def get_default_preset():
        return {
                presets.TYPE: "1D",
                presets.EXT: '.lut',
                presets.IN_RANGE: [0, 1023],
                presets.OUT_RANGE: [0, 1023],
                presets.OUT_BITDEPTH: 10,
                presets.TITLE: "Ascii LUT",
                presets.COMMENT: ("Generated by ColorPipe-tools, ascii_helper "
                                 "{0}").format(__version__),
                presets.VERSION: "1"
                }

    def _write_1d_2d_lut(self, process_function, file_path, preset,
                         line_function):
        # check range
        for str_range in [presets.IN_RANGE, presets.OUT_RANGE]:
            arange = preset[str_range]
            presets.check_range_is_int(arange,
                                       self. _get_range_message(str_range,
                                                                arange))
        # output range max value must be equal to output bitdepth max value
        output_range_maxvalue = preset[presets.OUT_RANGE][1]
        bitdepth_size = pow(2, preset[presets.OUT_BITDEPTH])
        bitdepth_maxvalue = bitdepth_size - 1
        if  output_range_maxvalue != bitdepth_maxvalue:
            raise AsciiHelperException(("Output range max value ({0}) must be "
                                        "in adaquation with out bitdepth "
                                        "({1} bits --> {2} max value)"
                                        ).format(output_range_maxvalue,
                                                 preset[presets.OUT_BITDEPTH],
                                                 bitdepth_maxvalue))
        # get data
        data = self._get_1d_data(process_function, preset)
        lutfile = open(file_path, 'w+')
        # comment
        lutfile.write("# {0}\n".format(preset[presets.COMMENT]))
        # header
        lutfile.write('LUT: ')
        if preset[presets.TYPE] == '2D':
            lutfile.write('3 ')
        else:
            lutfile.write('1 ')
        lutfile.write("{0}\n".format(bitdepth_size))
        # data
        # line_function mustn't be used here
        for rgb in data:
            lutfile.write(self._get_pattern_1d(preset).format(rgb.r))
        if preset[presets.TYPE] == '2D':
            for rgb in data:
                lutfile.write(self._get_pattern_1d(preset).format(rgb.g))
            for rgb in data:
                lutfile.write(self._get_pattern_1d(preset).format(rgb.b))
        lutfile.close()
        print_success_message(self.get_export_message(file_path))

    def write_1d_lut(self, process_function, file_path, preset):
        preset[presets.TYPE] = '1D'
        AbstractLUTHelper.write_1d_lut(self, process_function, file_path,
                                       preset)

    def write_2d_lut(self, process_function, file_path, preset):
        preset[presets.TYPE] = '2D'
        AbstractLUTHelper.write_2d_lut(self, process_function, file_path,
                                       preset)

    def write_3d_lut(self, process_function, file_path, preset):
        message = "3D  LUT is not supported in Ascii format"
        print_error_message(message)
        raise AsciiHelperException(message)

    @staticmethod
    def _get_range_message(range_name, arange):
        """ Get range warning/error message

        Returns:
            .str

        """
        return ("Ascii {0} is expected to be int."
                " Ex: [0, 1023] or [0, 65535].\nYour range {1}"
                ).format(range_name, arange)

ASCII_HELPER = AsciiLutHelper()
