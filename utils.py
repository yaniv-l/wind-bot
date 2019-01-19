import os
import sys

# configparser module was changed to ConfigParser in python 3 - check which runtime version to and load correct module for version
if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser
else:
    from configparser import SafeConfigParser

# Init config
config = SafeConfigParser()
# Read the config file - if file cannot be found in the script dir, then assert.
assert (config.read(os.path.dirname(__file__) + "/wind-bot.cfg"))