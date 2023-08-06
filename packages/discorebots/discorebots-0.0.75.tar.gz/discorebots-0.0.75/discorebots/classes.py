import disnake
from disnake.ext import commands
import os

class commandloader:

  commandsToLoad = []
  cog_commands = []

  def __init__(self, name: str = None, code: list = None):
    self.name = name
    self.code = code
    self.split = ";."

    commandloader.commandsToLoad.append(self)

class Database:
  def __init__(self, kwargs: dict={}):
    if "path" in kwargs:

      if str(kwargs["path"]).endswith(".json"):
        if not kwargs["path"] in os.listdir():
          with open(kwargs["path"], "w") as file:
            file.write("{}")

        self.path = kwargs["path"]
      else:
        print("Invalid file extension (use .json file)")
        self.path = "variables.json"
    else:
      self.path = "variables.json"
