import unittest

import mock


class MicrosoftDnsTestCase(unittest.TestCase):

    def setUp(self):

        # `import wmi` fails on non-windows machines. So before we import
        # anything, mock the entire wmi module.
        self.wmi_module_mock = mock.MagicMock()
        modules = {'wmi': self.wmi_module_mock}
        self.module_patcher = mock.patch.dict('sys.modules', modules)
        self.module_patcher.start()

        # Make the WMI instance builder return a Mock object.
        self.wmi_mock = mock.MagicMock()
        self.wmi_module_mock.WMI.return_value = self.wmi_mock

        # Make wmi_module_mock.x_wmi an Exception, like wmi.x_wmi.
        self.wmi_module_mock.x_wmi = Exception

    def tearDown(self):
        self.module_patcher.stop()

    def test_create_master_zone(self):
        """
        Test that when no master blackhole zone exists, the following calls
        happen:
        1. query for master zone receives empty list
        2. master zone is created
        3. query for master zone receives list containing the created zone
        4. master record is created in the zone
        5. master zone is saved to file

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater

        master_mock = mock.MagicMock()

        # The query should return an empty list the first time, a non-empty
        # list the second time.
        self.wmi_mock.MicrosoftDNS_Zone.side_effect = [[], [master_mock]]

        self.updater = MicrosoftDnsUpdater('127.0.0.1')

        excepted_calls = [
                mock.call(ContainerName=self.updater.MASTER_ZONE),
                mock.call.CreateZone(ZoneName=self.updater.MASTER_ZONE,
                                     ZoneType=0, DsIntegrated=False),
                mock.call(ContainerName=self.updater.MASTER_ZONE)
        ]

        # Verify calls 1, 2, and 3.
        self.wmi_mock.MicrosoftDNS_Zone.assert_has_calls(excepted_calls)

        # Verify the master zone is stored as an attribute.
        self.assertEqual(self.updater.master, master_mock)

        # Verify call 4.
        self.wmi_mock.MicrosoftDNS_AType.CreateInstanceFromPropertyData.assert_called_once_with(
                DnsServerName=self.updater.server,
                ContainerName=self.updater.MASTER_ZONE,
                OwnerName=self.updater.MASTER_ZONE,
                IPAddress=self.updater.blackhole_ip)

        # Verify call 5.
        master_mock.WriteBackZone.assert_called_once_with()

    def test_create_master_zone_fails(self):
        """
        Test that when master zone creation fails without raising wmi.x_wmi,
        MicrosoftDnsException is raised.

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater, MicrosoftDnsException

        # Make the query return an empty list both times it's called.
        self.wmi_mock.MicrosoftDNS_Zone.side_effect = [[], []]

        with self.assertRaises(MicrosoftDnsException):
            MicrosoftDnsUpdater('127.0.0.1')

    def test_create_master_record_fails(self):
        """
        Test that when a master record cannot be created, MicrosoftDnsException
        is raised.

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater, MicrosoftDnsException

        master_mock = mock.MagicMock()
        self.wmi_mock.MicrosoftDNS_Zone.side_effect = [[], [master_mock]]

        # Make CreateZone raise wmi.x_wmi.
        self.wmi_mock.MicrosoftDNS_AType.CreateInstanceFromPropertyData.side_effect = \
                self.wmi_module_mock.x_wmi

        with self.assertRaises(MicrosoftDnsException):
            MicrosoftDnsUpdater('127.0.0.1')

    def test_save_master_zone_fails(self):
        """
        Test that when a master record cannot be saved, MicrosoftDnsException
        is raised.

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater, MicrosoftDnsException

        master_mock = mock.MagicMock()
        self.wmi_mock.MicrosoftDNS_Zone.side_effect = [[], [master_mock]]

        # Make WriteBackZone raise wmi.x_wmi.
        master_mock.WriteBackZone.side_effect = self.wmi_module_mock.x_wmi

        with self.assertRaises(MicrosoftDnsException):
            MicrosoftDnsUpdater('127.0.0.1')

    def test_no_master_record(self):
        """
        Test that when a master blackhole zone exists but there's no record in
        it, one is created.

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater

        master_mock = mock.MagicMock()
        self.wmi_mock.MicrosoftDNS_Zone.return_value = [master_mock]
        self.wmi_mock.MicrosoftDNS_AType.return_value = []

        self.updater = MicrosoftDnsUpdater('127.0.0.1')

        self.wmi_mock.MicrosoftDNS_AType.CreateInstanceFromPropertyData.assert_called_once_with(
                DnsServerName=self.updater.server,
                ContainerName=self.updater.MASTER_ZONE,
                OwnerName=self.updater.MASTER_ZONE,
                IPAddress=self.updater.blackhole_ip)

        master_mock.WriteBackZone.assert_called_once_with()

    def test_change_ip_address(self):
        """
        Test that when the updater is instantiated with a different blackhole
        ip, existing zones are reloaded.

        """

        from strongarm_msdns.msdns import MicrosoftDnsUpdater

        master_mock = mock.MagicMock()
        self.wmi_mock.MicrosoftDNS_Zone.return_value = [master_mock]

        record_mock = mock.MagicMock()
        record_mock.RecordData = '0.0.0.0'
        self.wmi_mock.MicrosoftDNS_AType.return_value = [record_mock]

        self.updater = MicrosoftDnsUpdater('127.0.0.1')

        record_mock.Modify.assert_called_once_with(IPAddress=self.updater.blackhole_ip)
        master_mock.WriteBackZone.assert_called_once_with()

        self.assertEqual(self.updater.need_reload, True)
