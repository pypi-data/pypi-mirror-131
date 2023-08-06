import json

class Database:
  def __init__(self, path: str=None):
    if path is not None:
      if path.endswith(".json"):
        self.path = path
      else:
        self.path = "variables.json"
    else:
      self.path = "variables.json"
      

  def createVar(self, key: str="key", value: str="value"):
    va = [key, value]
    with open(self.path, "r+", encoding = "utf-8") as f:
      try:
        data = json.load(f)
      except:
        data = {}

      if va[0] in data:
        print(f"createVar: Variable '{va[0]}' already exist")
      else:
        data[va[0]] = va[1]

        with open(self.path, "w+", encoding="utf-8") as f:
          json.dump(data, f, sort_keys=True, ensure_ascii=False, indent = 2)

  def getVar(self, key: str="key"):
    try:
      varname = key
      with open(self.path, "r+", encoding = "utf-8") as f:
        varsname = json.loads(f.read())
        return f"{str(varsname[varname])}"
    except:
      print(f"updateVar: Variable '{varname}' is not exist")

  def updateVar(self, key: str="key", new_value: str="new_value"):
    try:
      varname = [key, new_value]

      with open(self.path, "r+", encoding = "utf-8") as f:
        f_json = json.load(f)
        if varname[0] in f_json:
          f_json[varname[0]] = varname[1]

          with open(self.path, "r+", encoding = "utf-8") as f:
            json.dump(f_json, f, sort_keys=True, ensure_ascii=False, indent=2)
        else:
          print(f"updateVar: Variable '{varname[0]}' is not exist")
    except TypeError:
      pass

  def openAllVars(self):
    try:
      with open(self.path, "r+", encoding = "utf-8") as f:
        return f"```py\n{f.read()}```"
    except:
      print("openAllVars: error")