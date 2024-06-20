# -*- coding: utf-8 -*-
__author__ = "Marten4n6, Siddhant385"
__license__ = "GPLv3"

from server.modules.helper import *
from base64 import b64decode
import json

class Module(ModuleABC):
    def get_info(self):
        return {
            "Author:": ["Marten4n6"],
            "Description": "Gets the system information of bot/Client",
            "References": [],
            "Stoppable": False
        }

    
    def process_response(self, response, response_options):
            try:
                response = json.loads(response)
                res = ""
                res = "Total RAM: " +   response['RAM_total'] + "\n\n"
                res += "Free RAM: " + response['RAM_free'] + "\n\n"
                res += "RAM Used: " + response['RAM_used'] + "\n\n"
                res += "OS Name: " + response['OS_Name'] + "\n\n"
                res += "Os Install Date :" + response['OS_InstallDate'] + "\n\n"
                res += "Os Last Boot Up Time: " + response['OS_LastBootUpTime'] + "\n\n"
                res += "Os Architecture: " + response['OS_Architecture'] + "\n\n"
                res += "Os System Drive: " + response['OS_SystemDrive'] + "\n\n"
                res += "Os Windows Directory: " + response['OS_WindowsDirectory'] + "\n\n"
                res += "Os Build Number: " + response['OS_BuildNumber'] + "\n\n"
                res += "Os Serial Number: " + response['OS_SerialNumber'] + "\n\n"
                res += "Os Version: " + response['OS_Version'] + "\n\n"
                res += "Os Manufacturer: " + response['OS_Manufacturer'] + "\n\n"
                res += "Cs Owner: " + response['CS_Owner'] + "\n\n"
                res += "CPU Manufacturer: " + response['CPU_Manufacturer'] + "\n\n"
                res += "CPU Max Clock Speed: " + response['CPU_MaxClockSpeed'] + "\n\n"
                res += "CPU Used: " + response['CPU_Used'] + "\n\n"
                res += "CPU Free: " + response['CPU_Free'] + "\n\n"
                res += "Disk ID: " + response['Disk_ID'] + "\n\n"
                res += "Disk Total Space: " + response['Disk_TotalSpace'] + "\n\n"
                res += "Disk Free Space: " + response['Disk_FreeSpace'] + "\n\n"
                res += "Disk Used Space: " + response['Disk_UsedSpace'] + "\n\n"
                res += "IPConfig: " + response['ipconfig'] + "\n\n"
                res += "Drive Query: " + response['driverquery'] + "\n\n"
                res += "netstart: " + response['netstart'] + "\n\n"
                res += "System Info: " + response['systeminfo'] + "\n\n"
                return res
            except ValueError:
                 res = "Response is not of json Type"
                 return res