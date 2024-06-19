

import subprocess
from os import path


def run_command(command):
    """Runs a system command and returns its response."""
    out, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    return out + err


def run(options):
    program_directory = options["program_directory"]
    launch_agent_name = options["loader_options"]["launch_agent_name"]
    launch_agent_file = path.join(program_directory, launch_agent_name + ".vbs")

    print("[remove_bot] Goodbye!")
    registries = [f'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v {launch_agent_name} /t REG_SZ /d "{launch_agent_file}"',
                       f'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v {launch_agent_name} /t REG_SZ /d "{launch_agent_file}"',
                       f'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices" /v {launch_agent_name} /t REG_SZ /d "{launch_agent_file}"',
                       f'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce" /v {launch_agent_name} /t REG_SZ /d "{launch_agent_file}"']

    for regs in registries:
        run_command(regs)
    run_command("rmdir " + program_directory)
    run_command("rmdir " + launch_agent_file)
    run_command("rmdir " + launch_agent_name)
