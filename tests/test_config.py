try:  # Python 2
    import __builtin__ as builtins
except ImportError:  # Python 3
    import builtins
import unittest

import mock

from strongarm_msdns import config


class ConfigTestCase(unittest.TestCase):

    def mock_readlines(self, text):
        """Return a mock_open that supports readline."""
        m = mock.mock_open(read_data=text)
        m.return_value.readline.side_effect = text.split('\n')
        m.return_value.__iter__ = lambda _: iter(text.split('\n'))
        return m

    def test_read_config(self):
        """
        Test that the correct dictionary is returned for a well-formed config.

        """

        data = """\
[strongarm-msdns]
api_key = some_key
blackhole_ip = 127.0.0.1
"""
        with mock.patch.object(builtins, 'open', self.mock_readlines(data)):
            self.assertEqual(config.read_config(),
                             {'api_key': 'some_key',
                              'blackhole_ip': '127.0.0.1'})

    def test_read_config_wrong_section(self):
        """
        Test that NoSectionError is raised when the section is incorrect.

        """

        data = """\
[strongarm]
api_key = some_key
blackhole_ip = 127.0.0.1
"""
        with self.assertRaises(config.configparser.NoSectionError):
            with mock.patch.object(builtins, 'open', self.mock_readlines(data)):
                self.assertEqual(config.read_config(),
                                 {'api_key': 'some_key',
                                  'blackhole_ip': '127.0.0.1'})

    def test_write_config(self):
        """
        Test that `write_config` writes the correct configuration to file.

        """

        m = mock.mock_open()
        with mock.patch.object(builtins, 'open', m):
            config.write_config(api_key='some_key', blackhole_ip='127.0.0.1')

        m.assert_called_once_with(config.CONFIG_FILE, 'w')

        # Check the right text is written, one `write` call per line.
        calls = ['[strongarm-msdns]\n',
                 'api_key = some_key\n',
                 'blackhole_ip = 127.0.0.1\n',
                 '\n']
        m().write.assert_has_calls(map(mock.call, calls), any_order=True)
