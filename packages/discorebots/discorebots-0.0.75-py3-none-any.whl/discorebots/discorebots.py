#===Сторонние импорты===
#Работа с дискордом через disnake
import disnake as discord
from disnake.ext import commands

#Без категории
import typing
import ast
import os
from colorama import Fore, Back

#Работа с временем
import datetime
import time

#Json
import json
import betterjsondb

#Работа с запросами
import requests

#Рандомизация
import random

#Асинхронные функции
import asyncio

#===Внешние импорты===
#Ошибки и функции
from .__defines__ import embeds_error, checkCondition

#Версия модуля
from .__versions__ import packageVersion

#Классы
from .classes import commandloader

version = packageVersion

class setupBot(commandloader):
  def __init__(self, intents: bool=False, token: str=None, prefix: str="", sharding: bool=False, shardsAmount: int=2, database: dict={"file": "variables.json"}):
    "Create bot"
    if not database["file"] in os.listdir():
      with open(database["file"], "w") as file:
        file.write("{}")
    self.__token = token
    self.__intents = intents
    self.__prefix = prefix
    self.__sharding = sharding
    self.__shardsAmount = shardsAmount
    self.__database = betterjsondb.connect(file=f'{database["file"]}', prefix="-->")
    if self.__intents is True:
      if self.__sharding is True:
        self.__clientUse = commands.AutoShardedBot(shard_count=self.__shardsAmount, command_prefix=self.__prefix, intents=discord.Intents.all())
      else:
        self.__clientUse = commands.Bot(command_prefix=self.__prefix, intents=discord.Intents.all())
    else:
      if self.__sharding is True:
        self.__clientUse = commands.AutoShardedBot(shard_count=self.__shardsAmount, command_prefix=self.__prefix)
      else:
        self.__clientUse = commands.Bot(command_prefix=self.__prefix)

  def setBotStatus(self, status: str=None, status_type: str=None, text="discorebots.py lib", stream_url: str="https://discord.com"):
    "Set status to bot"
    self.__status = status_type
    self.__statust = status
    self.__stream_url = stream_url
    self.__text = text

  def onWebsocketResponse(self, to_console: str=None):
    "Ready command"
    self.__started_timeout = time.time()
    print(f"Approximate time to turn on: ({self.__shardsAmount * 2}sec ~ {self.__shardsAmount * 7}sec)")
    @self.__clientUse.event
    async def on_ready():
      if to_console is not None:
        start = round(time.time()-self.__started_timeout, 1)
        print(f"{to_console} ({start}s)")
      await asyncio.sleep(5)
      if self.__status is not None:
        try:
          if self.__status == "game":
            if self.__statust == "dnd":
              await self.__clientUse.change_presence(status = discord.Status.dnd, activity=discord.Game(name=f"{self.__text}"))
            elif self.__statust == "idle":
              await self.__clientUse.change_presence(status = discord.Status.idle, activity=discord.Game(name=f"{self.__text}"))
            elif self.__statust == "online":
              await self.__clientUse.change_presence(status = discord.Status.online, activity=discord.Game(name=f"{self.__text}"))
            else:
              print("Status: Error status")
          elif self.__status == "stream":
            if self.__statust == "dnd":
              await self.__clientUse.change_presence(status = discord.Status.dnd, activity=discord.Streaming(name=f"{self.__text}", url=f"{self.__stream_url}"))
            elif self.__statust == "idle":
              await self.__clientUse.change_presence(status = discord.Status.idle, activity=discord.Streaming(name=f"{self.__text}", url=f"{self.__stream_url}"))
            elif self.__statust == "online":
              await self.__clientUse.change_presence(status = discord.Status.online, activity=discord.Streaming(name=f"{self.__text}", url=f"{self.__stream_url}"))
            elif self.__statust == "only_stream":
              await self.__clientUse.change_presence(activity=discord.Streaming(name=f"{self.__text}", url=f"{self.__stream_url}"))
            else:
              print("Status: Error status")
          elif self.__status == "listen":
            if self.__statust == "dnd":
              await self.__clientUse.change_presence(status = discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.__text}"))
            elif self.__statust == "idle":
              await self.__clientUse.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.__text}"))
            elif self.__statust == "online":
              await self.__clientUse.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.__text}"))
            else:
              print("Status: Error status")
          elif self.__status == "watch":
            if self.__statust == "dnd":
              await self.__clientUse.change_presence(status = discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.__text}"))
            elif self.__statust == "idle":
              await self.__clientUse.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.__text}"))
            elif self.__statust == "online":
              await self.__clientUse.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.__text}"))
            else:
              print("Status: Error status")
          else:
            print("Status: Error set status (incorrect type)")
        except Exception as e:
          print(e)
        
        self.__start_time = time.time()

  def load_commands(self, path: str = None, load_text: str="[COG] command [<command>] loaded, status: [<status>]"):
    loader_info = []
    self.__text_to_load = load_text
    try:
      for file in os.listdir(path):
        with open("{}/{}".format(path, file), "r") as file:
          comds = eval(file.read())
          for cmd in comds:
            if "prefix" in cmd:
              gerprefix_to_cog = cmd["prefix"]
            else:
              gerprefix_to_cog = self.__prefix
            apdn = [cmd["name"], cmd["code"], gerprefix_to_cog]

            def text_to_load(text, status):
              while "[<command>]" in text:
                text = text.replace("[<command>]", f'{gerprefix_to_cog}{cmd["name"]}')
                break

              while "[<status>]" in text:
                text = text.replace("[<status>]", f'{status}')
                break

              while "[<loaded>]" in text:
                text = text.replace("[<loaded>]", str(len(loader_info)))

              return text


            loader_info.append(cmd)

            commandloader.cog_commands.append(apdn)
            print(f'{text_to_load(self.__text_to_load, Fore.GREEN + "done" + Fore.RESET)}')
    except FileNotFoundError:
        print(f'{text_to_load(self.__text_to_load, Fore.RED + "failed" + Fore.RESET)}')

  def addCommand(self, name: str = None, code: list = None, prefix: str = None):
    """
    create a new command
    @param (str) name: commandName
    @param (list) code: code of your command
    """
    commandName = name
    commandCode = code
    if prefix is not None:
      commandPrefix = prefix
    else:
      commandPrefix = self.__prefix

    commandloader.commandsToLoad.append([commandName, commandCode, commandPrefix])

  def onClientMessage(self):
    """
    Allows the bot to use commands
    """
    commandloader.commandsToLoad = [*commandloader.cog_commands, *commandloader.commandsToLoad]

    @self.__clientUse.event
    async def on_message(message):
      for x in self.__clientUse.guilds:
        users_massiv = [y for y in x.members]
      
      if message.channel.type is not discord.ChannelType.private:
        if not message.author.bot:
            
          for commandinfo in commandloader.commandsToLoad:
            commandname = commandinfo[0].lower()
            commandcode = commandinfo[1]
            prefix = commandinfo[2].lower()
            
            try:
              trigger = message.content.split()[0]
            except Exception:
              trigger = message.content

            if str(trigger).lower() == str(prefix + commandname):
              
              
              channel = message.channel.id

              app = await self.__clientUse.application_info()

              global view
              view = discord.ui.View()

              embed = discord.Embed()

              async def getMessage(index: int = None):
                try:
                  Msg = message.content.lstrip(f"{trigger} ")
                  if index:
                    return Msg.split()[index-1]
                  else:
                    return Msg
                except Exception as e:
                  print("message: Error find message")
                  return ""

              class CreateButtonClass(discord.ui.Button):
                def __init__(self, label=None, ephemeral="false", usecode=None, button_style=None):

                  if button_style == "blue":
                    buttonStyle = discord.ButtonStyle.blurple
                  elif button_style == "red":
                    buttonStyle = discord.ButtonStyle.red
                  elif button_style == "green":
                    buttonStyle = discord.ButtonStyle.green
                  elif button_style == "grey":
                    buttonStyle = discord.ButtonStyle.grey
                  else:
                    buttonStyle = discord.ButtonStyle.blurple

                  super().__init__(label=label, style=buttonStyle)
                  self.usecode = usecode
                  self.ephe = ephemeral

                async def callback(self, interaction):
                  
                  if self.ephe.lower() == "true":
                    ephe = True
                  else:
                    ephe = False

                  embed = discord.Embed()

                  while "$interactionAuthorID" in self.usecode:
                    self.usecode = self.usecode.replace("$interactionAuthorID", str(f"{interaction.author.id}"))
                    break

                  while "$interactionTag" in self.usecode:
                    self.usecode = self.usecode.replace("$interactionTag", str(f"{interaction.author}"))
                    break

                  try:
                    await interaction.response.send_message(f"{self.usecode}", ephemeral = ephe)
                  except Exception:
                    pass

              codestatus = {
                "addReactions": {
                  "enabled": False,
                  "reactions": []
                },
                "onlyAdmin": False,
                "onlyForIDs": {
                  "enabled": False,
                  "ids": []
                },
                "let": {},
                "onlyIf": {
                  "enabled": False,
                  "error": ""
                },
                "reply": {
                  "enabled": False,
                  "mention": True
                }
              }
              
              while "$addCmdReactions[" in commandcode:
                reactions = commandcode.split("$addCmdReactions[")[1].split("]")[0]
                commandcode = commandcode.replace("$addCmdReactions[{}]".format(reactions), "")
                for react in reactions.split(";"):
                    await message.add_reaction(react)

              while "$addReactions[" in commandcode:
                reactions = commandcode.split("$addReactions[")[1].split("]")[0]
                commandcode = commandcode.replace("$addReactions[{}]".format(reactions), "")
                codestatus["addReactions"]["reactions"] = reactions.split(";")
                codestatus["addReactions"]["enabled"] = True

              def insert_returns(body):
                if isinstance(body[-1], ast.Expr):
                  body[-1] = ast.Return(body[-1].value)
                  ast.fix_missing_locations(body[-1])
                  if isinstance(body[-1], ast.If):
                    insert_returns(body[-1].body)
                    insert_returns(body[-1].orelse)
                    if isinstance(body[-1], ast.With):
                      insert_returns(body[-1].body)

              while "$eval[" in commandcode:
                codetouse = commandcode.split("$eval[")[1].split("]")[0]
                commandcode = commandcode.replace(f"$eval[{codetouse}]", codetouse)
                break

              while "$pyEval[" in commandcode:
                pycode = commandcode.split("$pyEval[")[1].split("]")[0]
                ctx = await self.__clientUse.get_context(message)
                try:
                  fn_name = "_eval_expr"
                  cmd = pycode.strip("```")
                  cmd = "\n".join(f" {i}" for i in cmd.splitlines())
                  body = f"async def {fn_name}():\n{cmd}"
                  parsed = ast.parse(body)
                  body = parsed.body[0].body
                  insert_returns(body)
                  env = {
                    "bot":self.__clientUse,
                    'disnake': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__
                  }
                  exec(compile(parsed, filename="<ast>", mode="exec"), env)
                  result = (await eval(f"{fn_name}()", env))
                  commandcode = commandcode.replace(f"$pyEval[{pycode}]", "")
                except Exception as e:
                  commandcode = commandcode.replace(f"$pyEval[{pycode}]", str(e))
                  break

              if "$createNormalButton[" in commandcode:
                button_config = commandcode.split("$createNormalButton[")[1].split("]")[0].split(";")
                if codestatus['onlyForIDs'] == True:
                  break
                else:
                  is_name = button_config[0]
                  is_ephe = button_config[1]
                  is_style = button_config[2]
                  is_code = button_config[3]
                  button = CreateButtonClass(f"{is_name}", f"{is_ephe}", f"{is_code}", f"{is_style}")
                  view.add_item(button)
                  codestatus['iters'] = True
                  commandcode = commandcode.replace(f"$createNormalButton[{button_config[0]};{button_config[1]};{button_config[2]};{button_config[3]}]", str(f""))

              if "$createUrlButton[" in commandcode:
                button_config = commandcode.split("$createUrlButton[")[1].split("]")[0].split(";")
                if codestatus['onlyForIDs'] == True:
                  break
                else:
                  view.clear_items()
                  is_name = button_config[0]
                  is_url = button_config[1]
                  button = discord.ui.Button(label=f"{is_name}", url=f"{is_url}")
                  view.add_item(button)
                  codestatus['iters'] = True
                  commandcode = commandcode.replace(f"$createUrlButton[{button_config[0]};{button_config[1]}]", str(f""))

              while "$message[" in commandcode:
                  index = int(commandcode.split("$message[")[1].split("]")[0])
                  commandcode = commandcode.replace(f"$message[{index}]", f"{await getMessage(index)}")

              while "$message" in commandcode:
                  commandcode = commandcode.replace("$message", f"{await getMessage()}")

              while "$authorID" in commandcode:
                commandcode = commandcode.replace("$authorID", str(message.author.id))
                break

              while "$mentioned[" in commandcode:
                index = int(commandcode.split("$mentioned[")[1].split("]")[0])
                mentions = [str(m.id) for m in message.mentions]
                mention_list = "[" + ";".join(mentions[:-1]) + ";" + mentions[-1] + "]"
                getmention = mention_list.split("[")[1].split("]")[0].split(";")
                if getmention[0] == "" or getmention[0] is None:
                  mention_list = mention_list.replace(";", str(""))

                getmention = mention_list.split("[")[1].split("]")[0].split(";")
                try:
                  commandcode = commandcode.replace(f"$mentioned[{index}]", f"{getmention[index-1]}")
                except IndexError:
                  commandcode = commandcode.replace(f"$mentioned[{index}]", str(""))
                  break
                
              while "$createServerInvite[" in commandcode:
                invite_info = commandcode.split("$createServerInvite[")[1].split("]")[0]
                try:
                  link = await message.channel.create_invite(xkcd=True, max_age = int(invite_info), max_uses = 0)
                  commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", f"{link}")
                except Exception:
                  try:
                    link = await message.channel.create_invite(xkcd=True, max_age = 0, max_uses = 0)
                    commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", f"{link}")
                  except Exception:
                    commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", "createServerInvite: Failed to create invite")
                    break

              while "$setServerVar[" in commandcode:
                var = commandcode.split("$setServerVar[")[1].split("]")[0].split(";")
                self.__database.push(f"server_{var[0]}_{message.guild.id}", f"{var[1]}")
                commandcode = commandcode.replace(f"$setServerVar[{var[0]};{var[1]}]", str(""))
                break

              while "$getServerVar[" in commandcode:
                var = commandcode.split("$getServerVar[")[1].split("]")[0]
                try:
                  response = self.__database.get(f"server_{var}_{message.guild.id}")
                  commandcode = commandcode.replace(f"$getServerVar[{var}]", str(f"{response}"))
                except KeyError:
                  commandcode = commandcode.replace(f"$getServerVar[{var}]", str(f"getServerVar: variable '{var}' not found"))
                  break

              while "$setVar[" in commandcode:
                var = commandcode.split("$setVar[")[1].split("]")[0].split(";")
                self.__database.push(f"var_{var[0]}", f"{var[1]}")
                commandcode = commandcode.replace(f"$setVar[{var[0]};{var[1]}]", str(""))
                break

              while "$getVar[" in commandcode:
                var = commandcode.split("$getVar[")[1].split("]")[0]
                try:
                  response = self.__database.get(f"var_{var}")
                  commandcode = commandcode.replace(f"$getVar[{var}]", str(f"{response}"))
                except KeyError:
                  commandcode = commandcode.replace(f"$getVar[{var}]", str(f"getVar: variable '{var}' not found"))
                  break

              while "$serverName" in commandcode:
                commandcode = commandcode.replace("$serverName", f"{message.guild.name}")

              while "$authorName" in commandcode:
                commandcode = commandcode.replace("$authorName", str(message.author.name))
                break
              
              while "$ping" in commandcode:
                commandcode = commandcode.replace("$ping", f"{round(self.__clientUse.latency*1000)}")
                break

              while "$uptime" in commandcode:
                current_time = time.time()
                difference = int(round(current_time - self.__start_time))
                text = str(datetime.timedelta(seconds=difference))
                commandcode = commandcode.replace("$uptime", f"{text}")
                break

              while "$readyTimestamp" in commandcode:
                commandcode = commandcode.replace("$readyTimestamp", f"{int(self.__start_time)}")

              while "$channelID" in commandcode:
                commandcode = commandcode.replace("$channelID", str(message.channel.id))
                break

              while "$clientID" in commandcode:
                commandcode = commandcode.replace("$clientID", str(self.__clientUse.user.id))
                break

              while "$authorAvatar" in commandcode:
                getuser = discord.utils.get(message.guild.members, id=message.author.id)
                commandcode = commandcode.replace("$authorAvatar",f"{getuser.avatar}")
                break

              while "$userTag[" in commandcode:
                try:
                  finduserid = commandcode.split("$userTag[")[1].split("]")[0]
                  kvas = await self.__clientUse.fetch_user(finduserid)
                  commandcode = commandcode.replace(f"$userTag[{finduserid}]", f"{kvas.name}#{kvas.discriminator}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$userTag[{finduserid}]", f"```userTag: Incorrect UserID in $userTag[{finduserid}]```")
                  break

              while "$findUserID[" in commandcode:
                try:
                  finduserid = commandcode.split("$findUserID[")[1].split("]")[0]
                  strelkarak = discord.utils.get(message.guild.members, name=finduserid)
                  commandcode = commandcode.replace(f"$findUserID[{finduserid}]", f"{strelkarak.id}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$findUserID[{finduserid}]", f"findUserID: Incorrect UserID in $findUserID[{finduserid}]")
                  break

              
              
              while "$jsonRequest[" in commandcode:
                request = commandcode.split("$jsonRequest[")[1].split("]")[0].split(";")
                try:
                  commandcode = commandcode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", str(f"{requests.get(request[0]).json()[request[1]]}"))
                except KeyError as e:
                  commandcode = commandcode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", f"{request[2]}")
                  break

              while "$round[" in commandcode:
                to_round = commandcode.split("$round[")[1].split("]")[0]
                try:
                  commandcode = commandcode.replace(f"$round[{to_round}]", f"{round(float(to_round))}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$round[{to_round}]", f"round: Incorrect Number in $round[{to_round}]")
                  break

              while "$shardID" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    commandcode = commandcode.replace("$shardID", f"{shard_id}")
                else:
                  commandcode = commandcode.replace("$shardID", f"shardID: Sharding disabled")
              
              while "$shardCount" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    commandcode = commandcode.replace("$shardCount", f"{self.__shardsAmount}")
                  else:
                    commandcode = commandcode.replace("$shardCount", f"shardCount: Sharding error< shards count only >= 2")
                else:
                  commandcode = commandcode.replace("$shardCount", f"shardCount: Sharding disabled")

              while "$shardPing" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    shard = self.__clientUse.get_shard(shard_id)
                    shard_ping = shard.latency
                    commandcode = commandcode.replace("$shardPing", f"{round(shard_ping*1000)}")
                else:
                  commandcode = commandcode.replace("$shardPing", f"shardPing: Sharding disabled")
              
              while "$shardGuilds" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    shard = self.__clientUse.get_shard(shard_id)
                    shard_ping = shard.latency
                    shard_guilds = len([guild for guild in self.__clientUse.guilds if guild.shard_id == shard_id])
                    commandcode = commandcode.replace("$shardGuilds", f"{shard_guilds}")
                else:
                  commandcode = commandcode.replace("$shardGuilds", f"shardGuilds: Sharding disabled")

              while "$guildsCount" in commandcode:
                commandcode = commandcode.replace("$guildsCount", f"{len(self.__clientUse.guilds)}")
                break

              while "$guildID" in commandcode:
                commandcode = commandcode.replace("$guildID", f"{message.guild.id}")
                break

              while "$serverIcon" in commandcode:
                try:
                  icon_url = message.guild.icon
                  commandcode = commandcode.replace("$serverIcon", f"{icon_url}")
                except Exception as e:
                  commandcode = commandcode.replace("$serverIcon", str(""))

              while "$randomUserID" in commandcode:
                commandcode = commandcode.replace("$randomUserID", str(random.choice(message.guild.members).id))
                break

              while "$randomNumber[" in commandcode:
                randnumber = commandcode.split("$randomNumber[")[1].split("]")[0].split(";")
                try:
                  resrandnumber = random.randint(int(randnumber[0]),int(randnumber[1]))
                  commandcode = commandcode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]","{0}".format(resrandnumber))
                except:
                  commandcode = commandcode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]", f"```randomNumber: Error in $random[{int(randnumber[0])};{int(randnumber[1])}]```")
                  break

              while "$randomText[" in commandcode:
                randtext = commandcode.split("$randomText[")[1].split("]")[0]
                try:
                  rand = random.choice(randtext.split(";"))
                  commandcode = commandcode.replace(f"$randomText[{randtext}]", str(rand))
                except:
                  commandcode = commandcode.replace(f"$randomText[{randtext}]", f"```randomText: Error in $randomText[{randtext}]```")
                  break

              while "$onlyForIDs[" in commandcode:
                onlyusers = commandcode.split("$onlyForIDs[")[1].split("]")[0]
                if str(message.author.id) in onlyusers.split(";")[:-1]:
                  codestatus["onlyForIDs"]["enabled"] = False
                  commandcode = commandcode.replace(f"$onlyForIDs[{onlyusers}]", f"")
                else:
                  await message.channel.send(str(onlyusers.split(";")[-1]))
                  codestatus["onlyForIDs"]["enabled"] = True
                  commandcode = commandcode.replace(f"$onlyForIDs[{onlyusers}]", f"")
                break

              while "$ban[" in commandcode:
                args = commandcode.split("$ban[")[1].split("]")[0].split(";")
                user = discord.utils.get(message.guild.members, id=int(args[0]))
                reason = args[1]
                try:
                  commandcode = commandcode.replace(f"$ban[{args[0]};{args[1]}]", str(""))
                  if reason is None or reason == "":
                    reason = str("")
                    await user.ban()
                  else:
                    await user.ban(reason=reason)
                except Exception:
                  commandcode = commandcode.replace(f"$ban[{args[0]};{args[1]}]", "ban: Failed to ban user")
                  break
              
              while "$kick[" in commandcode:
                args = commandcode.split("$kick[")[1].split("]")[0].split(";")
                commandcode = commandcode.replace(f"$kick[{args[0]};{args[1]}]", str(""))
                user = discord.utils.get(message.guild.members, id=int(args[0]))
                reason = args[1]
                try:
                  if reason is None or reason == "":
                    reason = str("")
                    await user.kick()
                  else:
                    await user.kick(reason=reason)
                except Exception:
                  commandcode = commandcode.replace(f"$kick[{args[0]};{args[1]}]", "kick: Failed to kick user")
                  break

              while "$giveRole[" in commandcode:
                userandrole = commandcode.split("$giveRole[")[1].split("]")[0].split(";")
                resmember = discord.utils.get(message.guild.members, id=int(userandrole[0]))
                resrole = discord.utils.get(message.guild.roles, id = int(userandrole[1]))
                try:
                  await resmember.add_roles(resrole)
                  commandcode = commandcode.replace(f"$giveRole[{userandrole[0]};{userandrole[1]}]", f"")
                except Exception as e:
                  commandcode = commandcode.replace(f"$giveRole[{userandrole[0]};{userandrole[1]}]", "```giveRole: Failed to add role```")
                  break

              while "$takeRole[" in commandcode:
                userandrole = commandcode.split("$takeRole[")[1].split("]")[0].split(";")
                resmember = discord.utils.get(message.guild.members, id=int(userandrole[0]))
                resrole = discord.utils.get(message.guild.roles, id = int(userandrole[1]))
                try:
                  await resmember.remove_roles(resrole)
                  commandcode = commandcode.replace(f"$takeRole[{userandrole[0]};{userandrole[1]}]", f"")
                except Exception as e:
                  commandcode = commandcode.replace(f"$takeRole[{userandrole[0]};{userandrole[1]}]", "```takeRole: Failed to remove role```")
                  break

              while "$onlyAdmin[" in commandcode:
                onlyadmins = commandcode.split(f"$onlyAdmin[")[1].split("]")[0]
                if message.author.guild_permissions.administrator:
                  codestatus["onlyAdmin"] = False
                  commandcode = commandcode.replace(f"$onlyAdmin[{onlyadmins}]", f"")
                elif not message.author.guild_permissions.administrator:
                  codestatus["onlyAdmin"] = True
                  await message.channel.send(onlyadmins)
                  commandcode = commandcode.replace(f"$onlyAdmin[{onlyadmins}]", f"")
                break

              while "$packageVersion" in commandcode:
                commandcode = commandcode.replace("$packageVersion", f"{version}")
                break

              while "$delMessage" in commandcode:
                try:
                  commandcode = commandcode.replace("$delMessage", f" ")
                  await message.delete()
                except Exception as e:
                  commandcode = commandcode.replace(f"$delMessage", "delMessage: Failed to delete message")
                  break

              if "$setTitle[" in commandcode:
                title = commandcode.split("$setTitle[")[1].split("]")[0]
                embed.title = title
                commandcode = commandcode.replace(f"$setTitle[{title}]", str(""))
                codestatus['embed'] = True

              if "$setDescription[" in commandcode:
                descr = commandcode.split("$setDescription[")[1].split("]")[0]
                embed.description = descr
                commandcode = commandcode.replace(f"$setDescription[{descr}]", str(""))
                codestatus['embed'] = True

              if "$setColor[" in commandcode:
                colour = commandcode.split("$setColor[")[1].split("]")[0]
                if colour == "random":
                  embed.color = discord.Color.random()
                  commandcode = commandcode.replace(f"$setColor[random]", str(""))
                else:
                  embed.color = eval(f"0x{str(colour)}")
                  commandcode = commandcode.replace(f"$setColor[{colour}]", str(""))

              if "$setFooter[" in commandcode:
                try:
                  fo = commandcode.split("$setFooter[")[1].split("]")[0].split(";")
                  if "$authorAvatar" in fo[1]:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};$authorAvatar]", str(""))
                    embed.set_footer(text = fo[0], icon_url = message.author.avatar)
                  elif "$serverIcon" in fo[1]:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};$serverIcon]", str(""))
                    embed.set_footer(text = fo[0], icon_url = message.guild.icon)
                  else:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};{fo[1]}]", str(""))
                    embed.set_footer(text = fo[0], icon_url = fo[1])
                except Exception as e:
                  foer = commandcode.split("$setFooter[")[1].split("]")[0]
                  commandcode = commandcode.replace(f"$setFooter[{foer}]", str(""))
                  embed.set_footer(text = foer)
                codestatus['embed'] = True


              if "$setThumbnail[" in commandcode:
                thum = commandcode.split("$setThumbnail[")[1].split("]")[0]
                if "$authorAvatar" in thum:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = message.author.avatar)
                elif "$serverIcon" in thum:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = message.guild.icon)
                else:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = thum)
                codestatus['embed'] = True


              if "$setAuthor[" in commandcode:
                try:
                  aut = commandcode.split("$setAuthor[")[1].split("]")[0].split(";")
                  if "$authorAvatar" in aut[1]:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};$authorAvatar]", str(""))
                    embed.set_author(name=aut[0], icon_url = message.author.avatar)
                  elif "$serverIcon" in aut[1]:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};$serverIcon]", str(""))
                    embed.set_author(name=aut[0], icon_url = message.guild.icon)
                  else:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};{aut[1]}]", str(""))
                    embed.set_author(name = aut[0], icon_url = aut[1])
                except:
                  aut = commandcode.split("$setAuthor[")[1].split("]")[0]
                  commandcode = commandcode.replace(f"$setAuthor[{aut}]", str(""))
                  embed.set_author(name = aut)
                codestatus['embed'] = True

              if "$setImage[" in commandcode:
                url = commandcode.split("$setImage[")[1].split("]")[0]
                if "$authorAvatar" in url:
                  commandcode = commandcode.replace("$setImage[$authorAvatar]", str(""))
                  embed.set_image(url = message.author.avatar)
                elif "$serverIcon" in url:
                  commandcode = commandcode.replace(f"$setImage[$serverIcon]", str(""))
                  embed.set_image(url = message.guild.icon)
                else:
                  commandcode = commandcode.replace(f"$setImage[{url}]", str(""))
                  embed.set_image(url = url)
                codestatus['embed'] = True

              if "$addTimestamp" in commandcode:
                try:
                  embed.timestamp = datetime.datetime.utcnow()
                  commandcode = commandcode.replace("$addTimestamp", str(""))
                  codestatus['embed'] = True
                except Exception:
                  commandcode = commandcode.replace("$addTimestamp", str(""))

              while "$addField[" in commandcode:
                field = commandcode.split("$addField[")[1].split("]")[0].split(";")
                embed.add_field(name=field[0], value=field[1])
                commandcode = commandcode.replace("$addField[{};{}]".format(field[0], field[1]), str(""))
                codestatus['embed'] = True

              while "$let[" in commandcode:
                  let = commandcode.split("$let[")[1].split("]")[0].split(";")
                  commandcode = commandcode.replace("$let[{};{}]".format(let[0], let[1]), str(""))
                  if not let[0] in codestatus["let"]:
                      codestatus["let"][let[0]] = let[1]

              if "$reply[" in commandcode:
                mention = commandcode.split("$reply[")[1].split("]")[0].lower()
                codestatus["reply"]["enabled"] = True
                if mention == "true":
                  codestatus["reply"]["mention"] = True
                elif mention == "false":
                  codestatus["reply"]["mention"] = False
                else:
                  codestatus["reply"]["mention"] = True
                commandcode = commandcode.replace(f"$reply[{mention}]", str(""))
                      
              while "$get[" in commandcode:
                  get = commandcode.split("$get[")[1].split("]")[0]
                  commandcode = commandcode.replace("$get[{}]".format(get), codestatus["let"][get])

              if codestatus["onlyForIDs"]["enabled"]:
                break

              while "$onlyIf[" in commandcode:
                only = commandcode.split("$onlyIf[")[1].split("]")[0].split(";")
                commandcode = commandcode.replace("$onlyIf[{};{}]".format(only[0], only[1]), "")

                if not checkCondition(only[0]):
                    codestatus["onlyIf"]["enabled"] = True
                    codestatus["onlyIf"]["error"] = only[1]

              if codestatus["onlyIf"]["enabled"]:
                await message.channel.send(str(codestatus["onlyIf"]["error"]))
                break

              if codestatus["onlyAdmin"]:
                break

              if codestatus["reply"]["enabled"]:
                if codestatus["reply"]["mention"] is False:
                  try:
                    try:
                      msg = await message.reply(f"{commandcode}", embed=embed, view=view, mention_author=False)
                    except discord.errors.HTTPException:
                        msg = await message.reply(f"{commandcode}", embed=embed, mention_author=False)
                  except discord.errors.HTTPException:
                    try:
                      msg = await message.reply(f"{commandcode}", view=view, mention_author=False)
                    except discord.errors.HTTPException:
                      try:
                        msg = await message.reply(f"{commandcode}", view=view, mention_author=False)
                      except discord.errors.HTTPException:
                        try:
                          msg = await message.reply(f"{commandcode}", mention_author=False)
                        except discord.errors.HTTPException:
                          pass
                else:
                  try:
                    try:
                      msg = await message.reply(f"{commandcode}", embed=embed, view=view)
                    except discord.errors.HTTPException:
                        msg = await message.reply(f"{commandcode}", embed=embed)
                  except discord.errors.HTTPException:
                    try:
                      msg = await message.reply(f"{commandcode}", view=view)
                    except discord.errors.HTTPException:
                      try:
                        msg = await message.reply(f"{commandcode}", view=view)
                      except discord.errors.HTTPException:
                        try:
                          msg = await message.reply(f"{commandcode}")
                        except discord.errors.HTTPException:
                          pass
              else:
                try:
                  try:
                    msg = await message.channel.send(f"{commandcode}", embed=embed, view=view)
                  except discord.errors.HTTPException:
                      msg = await message.channel.send(f"{commandcode}", embed=embed)
                except discord.errors.HTTPException:
                  try:
                    msg = await message.channel.send(f"{commandcode}", view=view)
                  except discord.errors.HTTPException:
                    try:
                      msg = await message.channel.send(f"{commandcode}", view=view)
                    except discord.errors.HTTPException:
                      try:
                        msg = await message.channel.send(f"{commandcode}")
                      except discord.errors.HTTPException:
                        pass

              if codestatus["addReactions"]["enabled"]:
                  for react in codestatus["addReactions"]["reactions"]:
                      try:
                          await msg.add_reaction(react)
                      except Exception:
                          pass

  def start(self):
    try:
      self.__clientUse.run(self.__token)
    except Exception as e:
      print("An error connection occured while acessing to Discord!\n\n{0}".format(str(e)))