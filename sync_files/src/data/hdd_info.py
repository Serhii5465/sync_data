class HddInfo:

    @staticmethod
    def wd_drive():
        # Wester Digital 1Tb (Maiwo External Enclosure)
        return {
            'uuid' : '088C11A28C118AF8',
            'name' : 'Wester Digital (Maiwo)'
        }

    @staticmethod
    def hitachi_drive():
        # Hitachi 500Gb (Maiwo External Enclosure)
        return {
            'uuid': '74FAE577FAE53650',
            'name': 'Hitachi (Maiwo)'
        }

    @staticmethod
    def dell_3576_drive():
        # Wester Digital 1Tb (Dell Inspiron 15 3576)
        return {
            'uuid': 'CE0E2EF20E2ED36F'
        }

    @staticmethod
    def jmicron_drive():
        # 2.5″ Western Digital 320Gb (JMicron)
        return {
            'uuid': '01D8C1D0373750C0',
            'name': 'Western Digital (JMicron)'
        }