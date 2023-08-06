from ...client import Client
from ...command import CommandOption, Command
from ...interaction import InteractionTypeCommand
from .errors import Application_Command_NotFound
from inspect import signature

class Bot(Client):
    def __init__(self):
        super().__init__()
        self._commands = {}

    async def on_interaction(self, interaction):
        try:
            await self.process_command(interaction)
        except Exception as error:
            self.dispatch("application_command_error", interaction, error)

    async def process_command(self, interaction):
        data = interaction.data
        if isinstance(interaction.type, InteractionTypeCommand):
            if data["name"] in self._commands:
                kwargs = {}
                if data.get("options") is not None:
                    for option in data.get("options"):
                        kwargs[option["name"]] = option["value"]
                await self._commands[data["name"]](interaction, **kwargs)
            else:
                raise Application_Command_NotFound("The application command is not registered.")

    def add_command(self, name, coro):
        options = []
        values = signature(coro).parameters.values()
        self._commands[name] = coro
        for p in values:
            option_name = p.name
            if option_name in ["self", "ctx"]:
                continue
            option = p.annotation
            if not isinstance(option, CommandOption):
                options.append(CommandOption(name = option_name))
            else:
                options.append(option)
        super().add_command(Command(name = name, description = coro.kwargs.pop("description", "..."), options = options))
    
    def application_command(self, name, **kwargs):
        def deco(coro):
            coro.kwargs = kwargs
            self.add_command(name, coro)
            return coro
        return deco

    def run(self, token):
        super().run(token)
