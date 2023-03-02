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
            'uuid': '82AA94D0AA94C1D9',
            'name': 'Wester Digital (Maiwo)'
        }

        #: Hitachi 500Gb (Maiwo External Enclosure)
        self.__hitachi_drive = {
            'uuid': '9882EA7C82EA5DEE',
            'name': 'Hitachi (Maiwo)'
        }

        #: Wester Digital 1Tb (Dell Inspiron 15 3576)
        self.__dell_3576_drive = {
            'uuid': '01D937210A0E5460'
        }

        #: 2.5″ Western Digital 320Gb (JMicron)
        self.__jmicron_drive = {
            'uuid': '01D937619AC13910',
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
