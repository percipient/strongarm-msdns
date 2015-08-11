import os
from sys import modules

import pythoncom
import servicemanager
import win32event
import win32service
import win32serviceutil
import winerror

from strongarm_msdns.config import read_config
from strongarm_msdns.msdns import MicrosoftDnsException, MicrosoftDnsUpdater


class MicrosoftDnsUpdaterService(win32serviceutil.ServiceFramework):

    # Run the updater every `interval` minutes.
    interval = 5

    _svc_name_ = "strongarm"
    _svc_display_name_ = "STRONGARM DNS Updater"
    _svc_description_ = ("This service updates zones on a Microsoft DNS server"
                         "according to domains blackholed in STRONGARM.")

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)

        self.read_config()

        # Event used for signaling the stop of the service.
        self.stopEvent = win32event.CreateEvent(None, 0, 0, None)

        # Make WMI happy when it's run in a thread.
        pythoncom.CoInitialize()

        self.updater = MicrosoftDnsUpdater(self.blackhole_ip)

    def read_config(self):

        # Change the working directory to the one containing the executable,
        # where the config file is supposed to be.
        from sys import executable
        os.chdir(os.path.dirname(executable))

        try:
            settings = read_config()
        except Exception:
            raise MicrosoftDnsException("Cannot read configuration file.")

        try:
            self.api_key = settings['api_key']
            self.blackhole_ip = settings['blackhole_ip']
        except KeyError:
            raise MicrosoftDnsException("Incomplete configuration file.")

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def SvcDoRun(self):
        """Run the updater repeatedly until a stop event is received."""

        while True:

            failed = self.updater.run(self.api_key)
            self.log('These domains failed to update: %s' % failed)

            # Block and wait for the stop event for `interval` minutes.
            wait_ms = self.interval * 60 * 1000
            if (win32event.WaitForSingleObject(self.stopEvent, wait_ms) ==
                    win32event.WAIT_OBJECT_0):
                break

    def SvcStop(self):
        # Report the status change to the service manager.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        # Fire the event to stop the service.
        win32event.SetEvent(self.stopEvent)


if __name__ == '__main__':

    # When the executable is run directly, use HandleCommandLine to make it
    # possible to install/start/stop the service. When the executable is run by
    # Windows Service Manager, run the actual service.
    # From https://mail.python.org/pipermail/python-win32/2008-April/007299.html

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(MicrosoftDnsUpdaterService)
            servicemanager.Initialize('MicrosoftDnsUpdaterService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error, details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(MicrosoftDnsUpdaterService)
