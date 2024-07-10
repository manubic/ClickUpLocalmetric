from lib.clickUp.api.fields import Fields
from lib.clickUp.api.spaces import Spaces
from lib.clickUp.api.folders import Folders
from lib.clickUp.api.lists import Lists
from lib.clickUp.api.tasks import Tasks



class ClickUp:
    def __init__(self, config) -> None:
        self.Fields = Fields(config)
        self.Spaces = Spaces(config)
        self.Folders = Folders(config)
        self.Lists = Lists(config)
        self.Tasks = Tasks(config)