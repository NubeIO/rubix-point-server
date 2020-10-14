import BAC0
import logging
import sys
# turn off BAC0 logging
BAC0.log_level('silence')

# Define a new logger
mylog = logging.getLogger('MyNewLogger')
mylog.logLevel(logging.DEBUG)

# Define a console handler
console = logging.StreamHandler(sys.stdout)
console.set_name("stdout")
console.setLevel(logging.DEBUG)

# Attach to mylog
mylog.addHandler(console)