# Small program to display the MicroPython verison
import sys
res = sys.implementation
print("Installed package")
print("-----------------")
print("Name    : %s" % str(res[0]))
major, minor, patch, dummy = res[1]
print("Version : %d.%d.%d" % (major, minor, patch))
print("Platform: %s" % str(res[2]))