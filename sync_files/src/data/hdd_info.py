class HddInfo:

    def __init__(self):
        # Wester Digital 1Tb (Maiwo External Enclosure)
        self.__wd_drive = {
            'uuid' : '088C11A28C118AF8',
            'name' : 'Wester Digital (Maiwo)'
        }

        # Hitachi 500Gb (Maiwo External Enclosure)
        self.__hitachi_drive = {
            'uuid': '74FAE577FAE53650',
            'name': 'Hitachi (Maiwo)'
        }

        # Wester Digital 1Tb (Dell Inspiron 15 3576)
        self.__dell_3576_drive = {
            'uuid': 'CE0E2EF20E2ED36F'
        }

        # 2.5″ Western Digital 320Gb (JMicron)
        self.__jmicron_drive = {
            'uuid': '01D8C1D0373750C0',
            'name': 'Western Digital (JMicron)'
        }

    @property
    def wd_drive(self):
        return self.__wd_drive

    @property
    def hitachi_drive(self):
        return self.__hitachi_drive

    @property
    def dell_3576_drive(self):
        return self.__dell_3576_drive

    @property
    def jmicron_drive(self):
        return self.__jmicron_drive