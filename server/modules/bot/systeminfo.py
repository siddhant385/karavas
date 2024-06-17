import platform
import subprocess
from os import getuid


def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    output = out + err

    if len(output.split("\n")) == 2:
        # Single line response.
        return output.replace("\n", "")
    else:
        return output



def run(options):
    string_builder = ""

    string_builder += "System version: %s\n" % str(platform.platform()[0])

    if getuid() == 0:
        string_builder += "We are root!\n"
    else:
        string_builder += "We are not root :(\n"
    print(string_builder)
