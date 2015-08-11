try:  # Python 2
    import ConfigParser as configparser
except ImportError:  # Python 3
    import configparser


CONFIG_FILE = 'strongarm-msdns.ini'
SECTION = 'strongarm-msdns'


def write_config(**kwargs):
    """
    Write to disk a configuration file containing the given keyword arguments.

    """
    config = configparser.ConfigParser()
    config.add_section(SECTION)

    for key in kwargs:
        config.set(SECTION, key, kwargs[key])

    with open(CONFIG_FILE, 'w') as fout:
        config.write(fout)


def read_config():
    """Read configuration file from disk and return a dictionary."""

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    return {option: config.get(SECTION, option)
            for option in config.options(SECTION)}
