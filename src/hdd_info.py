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
        'uuid': 'FE821EBE821E7B7B',
        'name': 'Western Digital (JMicron)'
    }

#: Wester Digital 1Tb (MSI GF63)
def MSI_GF63_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '01DA431E36406280'
    }