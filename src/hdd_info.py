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

#: Wester Digital 1Tb (MSI GF63)
def MSI_GF63_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '01D937210A0E5460'
    }

#: 2.5″ Western Digital 320Gb (JMicron)
def JMICRON_DRIVE() -> Dict[str, str]:
    return {
            'uuid': 'CE9A33B69A339A43',
            'name': 'Western Digital (JMicron)'
    }