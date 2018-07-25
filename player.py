import subprocess
import os
import sys

currentDirectory = os.path.dirname(__file__)

p = subprocess.Popen([sys.executable, '/path/to/script.py'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)

