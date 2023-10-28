from typing import Dict

#: Wester Digital 1Tb (Maiwo External Enclosure)
def WD_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '4EB4A2C6B4A2B03F',
        'name': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
def HITACHI_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '247AE4E87AE4B826',
        'name': 'Hitachi (Maiwo)'
    }

#: 2.5″ Western Digital 320Gb (JMicron)
def JMICRON_DRIVE() -> Dict[str, str]:
    return {
            'uuid': 'CC1C8A351C8A1B1A',
            'name': 'Western Digital (JMicron)'
    }

#: Wester Digital 1Tb (MSI GF63)
def MSI_GF63_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '1EA45183A4515DF9'
    }

def DELL_INSPIRON_DRIVE() -> Dict[str, str]:
    return {
        'uuid': 'B8F0199BF01960C4'
    }