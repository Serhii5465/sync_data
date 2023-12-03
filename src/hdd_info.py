from typing import Dict

#: Wester Digital 1Tb (Maiwo External Enclosure)
def WD_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '01DA25E4223300B0',
        'name': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
def HITACHI_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '01DA25E89FDC5B70',
        'name': 'Hitachi (Maiwo)'
    }

#: 2.5″ Western Digital 320Gb (JMicron)
def JMICRON_DRIVE() -> Dict[str, str]:
    return {
            'uuid': 'C8CADB06CADAEFA4',
            'name': 'Western Digital (JMicron)'
    }

#: Wester Digital 1Tb (MSI GF63)
def MSI_GF63_DRIVE() -> Dict[str, str]:
    return {
        'uuid': 'CA607FCC607FBDAF'
    }

def DELL_INSPIRON_DRIVE() -> Dict[str, str]:
    return {
        'uuid': 'B8F0199BF01960C4'
    }