"""
CARPI GPS REPORTER DAEMON
(C) 2021, Raphael "rGunti" Guntersweilerr
Licensed under MIT
"""
from datetime import datetime
from logging import Logger
from time import sleep
from typing import Any, Optional

from carpicommons.errors import CarPiExitException
from carpicommons.log import logger
from daemoncommons.daemon import Daemon
from redisdatabus.bus import TypedBusListener

from gpsreporter.keys import INPUT_DATA
from gpsreporter.targets.base import ReportingTarget, GpsData
from gpsreporter.targets.registry import is_target_known, get_target


class GpsReporterConfigError(CarPiExitException):
    EXIT_CODE = 0xD600

    def __init__(self):
        super().__init__(GpsReporterConfigError.EXIT_CODE)


class GpsReporterDaemon(Daemon):
    def __init__(self):
        super().__init__('GPS Reporter')
        self._reader = None
        self._log: Logger = None
        self._running = False
        self._current_values = dict()

    def _build_target(self) -> ReportingTarget:
        log = self._log

        target_type = self._get_config('Target', 'type', 'null')
        if not is_target_known(target_type):
            log.error('Target %s is not known and cannot be used!', target_type)
            raise GpsReporterConfigError()

        log.info('Initializing target %s ...', target_type)
        return get_target(target_type, self._config)

    def _build_bus_reader(self, channels: list) -> TypedBusListener:
        self._log.info('Connecting to Data Source Redis instance with %s keys ...',
                       len(channels))
        return TypedBusListener(channels,
                                host=self._get_config('Source', 'Host', '127.0.0.1'),
                                port=self._get_config_int('Source', 'Port', 6379),
                                db=self._get_config_int('Source', 'DB', 0),
                                password=self._get_config('Source', 'Password', None))

    def startup(self):
        self._log = log = logger(self.name)

        self._reader = reader = self._build_bus_reader(list(INPUT_DATA.values()))
        reader.register_global_callback(self._on_new_value_registered)

        target = self._build_target()
        interval = self._get_config_float('Target', 'interval', 5)

        self._running = True
        reader.start()

        log.info('GPS Reporter Daemon finished starting up, awaiting new data ...')
        while self._running:
            sleep(interval)
            self._step(target)

        reader.stop()

    def shutdown(self):
        self._log.info("Shutting down %s ...", self.name)
        self._running = False
        if self._reader:
            self._reader.stop()

    def _step(self, target: ReportingTarget):
        data = GpsData(self._get_stored_data('latitude'),
                       self._get_stored_data('longitude'),
                       self._get_stored_data('altitude'),
                       max(self._get_stored_data('epx'), self._get_stored_data('epy')),
                       self._get_stored_data('speed'),
                       self._get_stored_data('heading'),
                       self._get_stored_data('timestamp'),
                       self._get_stored_data('bat_soc'))
        target.report(data)

    def _get_stored_data(self, key: str) -> Optional[Any]:
        if not key in INPUT_DATA:
            self._log.error('Key %s is not known', key)
            return None
        if not INPUT_DATA[key] in self._current_values:
            self._log.warning('Key %s is not currently available', INPUT_DATA[key])
            return None
        return self._current_values[INPUT_DATA[key]]

    def _on_new_value_registered(self, channel: str, value: Any):
        self._log.debug('Received new value from %s: %s', channel, value)
        self._current_values[channel] = value
