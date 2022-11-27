from typing import Dict


class HDDInfo:
    """
    Class represents information about HDD: UUID of partition and name model drive.
    """
    def __init__(self) -> None:
        """
        Initializes dicts with value of UUID and name model of HDD.
        """
        #: Wester Digital 1Tb (Maiwo External Enclosure)
        self.__wd_drive = {
            'uuid': '429ED9EB9ED9D80D',
            'name': 'Wester Digital (Maiwo)'
        }

        #: Hitachi 500Gb (Maiwo External Enclosure)
        self.__hitachi_drive = {
            'uuid': '6CC2DC3FC2DC0F68',
            'name': 'Hitachi (Maiwo)'
        }

        #: Wester Digital 1Tb (Dell Inspiron 15 3576)
        self.__dell_3576_drive = {
            'uuid': 'DC4476D34476B03E'
        }

        #: 2.5″ Western Digital 320Gb (JMicron)
        self.__jmicron_drive = {
            'uuid': '581A0D2A1A0D06AA',
            'name': 'Western Digital (JMicron)'
        }

    @property
    def wd_drive(self) -> Dict[str, str]:
        return self.__wd_drive

    @property
    def hitachi_drive(self) -> Dict[str, str]:
        return self.__hitachi_drive

    @property
    def dell_3576_drive(self) -> Dict[str, str]:
        return self.__dell_3576_drive

    @property
    def jmicron_drive(self) -> Dict[str, str]:
        return self.__jmicron_drive
