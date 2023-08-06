"""
CARPI GPS REPORTER DAEMON
(C) 2021, Raphael "rGunti" Guntersweilerr
Licensed under MIT
"""
from daemoncommons.daemon import DaemonRunner

from gpsreporter.daemon import GpsReporterDaemon

if __name__ == '__main__':
    d = DaemonRunner('GPS_REPORT_CFG', ['gpsreport.ini', '/etc/carpi/gpsreport.ini'])
    d.run(GpsReporterDaemon())
