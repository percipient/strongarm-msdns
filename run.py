from strongarm_msdns import config, MicrosoftDnsException, MicrosoftDnsUpdater

try:
    settings = config.read_config()
except Exception:
    raise MicrosoftDnsException("Cannot read configuration file.")

try:
    api_key = settings['api_key']
    blackhole_ip = settings['blackhole_ip']
except KeyError:
    raise MicrosoftDnsException("Incomplete configuration file.")

MicrosoftDnsUpdater(blackhole_ip).run(api_key)
