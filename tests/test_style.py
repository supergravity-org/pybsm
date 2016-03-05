import unittest
import os.path
import logging
import pytest


class TestCodeFormat(unittest.TestCase):

    def test_pylama(self):
        from pylama.main import parse_options, process_paths
        from pylama.config import LOGGER
        LOGGER.setLevel(logging.WARN)
        options = parse_options(['.'],
                                verbose=False
                                )
        errors = process_paths(options, error=False)
        if len(errors):
            if os.environ.get('DEV', None) == '1':
                pytest.skip(msg="Should not have pylama errors but has")
            else:
                pytest.fail(msg="Should not have pylama errors", pytrace=False)
        else:
            self.assertTrue(True, 'pylama with no errors')
