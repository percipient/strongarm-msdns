import wmi

from strongarm.dns_integration import (DnsBlackholeUpdaterException,
                                       DnsBlackholeIncrementalUpdater)


class MicrosoftDnsException(DnsBlackholeUpdaterException):
    pass


class MicrosoftDnsUpdater(DnsBlackholeIncrementalUpdater):
    """
    Blackholed domains updater for Microsoft Active Directory-intergrated DNS
    Server.

    Domain blackholing is accomplished by
    1. creating a master DNS zone with the blackhole IP as an A record
    2. saving the master zone to a zone data file
    3. creating a zone for each blackholed domain, using the saved data file

    Adapted from a Powershell script that achieves similiar functionality:
    https://cyber-defense.sans.org/blog/2010/08/31/windows-dns-server-blackhole-blacklist

    """

    MASTER_ZONE = 'blackhole.strongarm.local'
    MASTER_ZONE_FILE = MASTER_ZONE + '.dns'

    def __init__(self, blackhole_ip, server='localhost'):
        """
        Create or verify the master DNS zone with the provided blackhole IP.

        If the updater is not running on the DNS server, provide the `server`
        argument to specify which host to connect WMI to.

        """

        super(MicrosoftDnsUpdater, self).__init__(blackhole_ip, server)

        # Whether we need to reload all zones for a blackhole ip change.
        self.need_reload = False

        self.wmi = wmi.WMI(server, namespace="MicrosoftDNS")

        # Find the master blackhole zone by container name.
        zones = self.wmi.MicrosoftDNS_Zone(ContainerName=self.MASTER_ZONE)

        # If it already exists, check that the blackhole ip address is correct.
        if zones:
            self.master = zones[0]
            self.verify_master_record_ip()
        # Otherwise, create it from scratch.
        else:
            self.create_master_zone()

    def create_master_zone(self):
        """
        Create the master blackhole zone that other blackholed domains will use
        as a template.

        Add the blackhole ip as an A record to the zone, and write the zone to
        file.

        """

        try:
            # Create the master blackhole zone. This call returns an unhelpful
            # tuple of a single string on success, raises wmi.x_wmi on failure.
            self.wmi.MicrosoftDNS_Zone.CreateZone(
                    ZoneName=self.MASTER_ZONE, ZoneType=0, DsIntegrated=False)

            # Get the newly created zone and store as an attribute.
            self.master = self.wmi.MicrosoftDNS_Zone(ContainerName=self.MASTER_ZONE)[0]

        except (wmi.x_wmi, IndexError):
            raise MicrosoftDnsException("Failed to create master zone.")

        self.create_master_record()
        self.save_master_zone_to_file()

    def create_master_record(self):
        """
        Create an A record in the master zone for the blackhole ip.

        """

        try:
            self.wmi.MicrosoftDNS_AType.CreateInstanceFromPropertyData(
                    DnsServerName=self.server, ContainerName=self.MASTER_ZONE,
                    OwnerName=self.MASTER_ZONE, IPAddress=self.blackhole_ip)
        except wmi.x_wmi:
            raise MicrosoftDnsException("Failed to create A record.")

    def save_master_zone_to_file(self):
        try:
            self.master.WriteBackZone()
        except wmi.x_wmi:
            raise MicrosoftDnsException("Failed to write zone file.")

    def verify_master_record_ip(self):
        """
        Verify that the master zone contains an A record with the blackhole ip,
        creating a record or modifying the existing record if necessary.

        """

        records = self.wmi.MicrosoftDNS_AType(ContainerName=self.MASTER_ZONE)

        if not records:
            self.create_master_record()
            self.save_master_zone_to_file()
            return

        record = records[0]

        if record.RecordData != self.blackhole_ip:
            record.Modify(IPAddress=self.blackhole_ip)
            self.save_master_zone_to_file()

            # Mark that reloading all zones is needed on update.
            self.need_reload = True

    def update_domains(self, domains):
        failed = []

        if self.need_reload:
            # Reload blackholed domains from the updated master zone file.
            zones = self.wmi.MicrosoftDNS_Zone(DataFile=self.MASTER_ZONE_FILE)
            for zone in zones:
                if zone.ContainerName == self.MASTER_ZONE:
                    continue  # Skip the master zone itself.
                try:
                    zone.ReloadZone()
                except wmi.x_wmi:
                    failed.append(zone.ContainerName)

            self.need_reload = False

        return failed + super(MicrosoftDnsUpdater, self).update_domains(domains)

    def add_domains(self, domains):
        failed = []
        for domain in domains:
            try:
                self.wmi.MicrosoftDNS_Zone.CreateZone(
                        ZoneName=domain, ZoneType=0, DsIntegrated=False,
                        DataFileName=self.MASTER_ZONE_FILE)
            except wmi.x_wmi:
                failed.append(domain)

        return failed

    def remove_domains(self, domains):
        failed = []
        for domain in domains:
            zones = self.wmi.MicrosoftDNS_Zone(ContainerName=domain)
            if zones:
                try:
                    zones[0].Delete_()
                except wmi.x_wmi:
                    failed.append(domain)
            else:
                failed.append(domain)

        return failed

    def list_domains(self):
        zones = self.wmi.MicrosoftDNS_Zone(DataFile=self.MASTER_ZONE_FILE)
        return [zone.ContainerName for zone in zones
                if zone.ContainerName != self.MASTER_ZONE]
