import disnake
from disnake.ext import commands

class commandloader:

  """
  Writes commands to a list for further storage
  """

  commandsToLoad = []

  def __init__(self, name: str = None, code: list = None):
    self.name = name
    self.code = code
    self.split = ";."

    commandloader.commandsToLoad.append(self)
