
import os
import subprocess
import sys

# Call the hoot command line directly.
binary = str(os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin/hoot"))
print([binary] + sys.argv[1:])
exit(subprocess.run([binary] + sys.argv[1:]).returncode)
