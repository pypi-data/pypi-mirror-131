"""
CARPI GPS REPORTER DAEMON
(C) 2021, Raphael "rGunti" Guntersweilerr
Licensed under MIT
"""

import gpsdaemon.keys as gpskeys
from redisdatabus.bus import TypedBusListener


def build_foreign_key(type: str, domain: str, key: str) -> str:
    return '{}{}.{}'.format(type, domain, key)


INPUT_DATA = {
    'latitude': gpskeys.KEY_LATITUDE,
    'longitude': gpskeys.KEY_LONGITUDE,
    'altitude': gpskeys.KEY_ALTITUDE,
    'epx': gpskeys.KEY_EPX,
    'epy': gpskeys.KEY_EPY,
    'speed': gpskeys.KEY_SPEED,
    'heading': gpskeys.KEY_TRACK,
    'timestamp': gpskeys.KEY_TIMESTAMP,
    'systimestamp': gpskeys.KEY_SYS_TIMESTAMP,
    'bat_soc': build_foreign_key(TypedBusListener.TYPE_PREFIX_FLOAT, 'carpi.can', 'BatterySoC')
}
