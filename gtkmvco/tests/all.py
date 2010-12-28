"""
Only works when python is launched from within "tests".
"""
import glob
import os.path
import unittest

modules = []
for name in glob.glob("*.py"):
    if name != __file__:
        f = open(name, "rU")
        if "unittest" in f.read():
            modules.append(os.path.splitext(name)[0])
        f.close()

suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
runner = unittest.TextTestRunner()
runner.run(suite)

# Detect if some unittest.main quit Python.
print "All done, bye-bye"
