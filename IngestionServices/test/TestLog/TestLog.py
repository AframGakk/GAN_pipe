
from tests.TestLog.bcolors import bcolors

class TestLog:

    def debug(self, message):
        print(bcolors.OKBLUE + str(message) + bcolors.ENDC)

    def info(self, message):
        print(bcolors.OKGREEN + str(message) + bcolors.ENDC)

    def error(self, message):
        print(bcolors.FAIL + str(message) + bcolors.ENDC)
