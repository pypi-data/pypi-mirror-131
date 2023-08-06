def embeds_error(error: dict={}):
  if "title" in error:
    title = error["title"]
  else:
    title = False

  if "description" in error:
    description = error["description"]
  else:
    description = False

  if "color" in error:
    color = error["color"]
  else:
    color = False

  if "footer" in error:
    footer = error["footer"]
  else:
    footer = False

def checkCondition(condtition):
  def split_symbol(argument, symbol):
      arg = argument.split(symbol)
      return [arg[0], symbol, arg[1]]

  if "==" in condtition:
      x = split_symbol(condtition, "==")
  elif "<=" in condtition:
      x = split_symbol(condtition, "<=")
  elif ">=" in condtition:
      x = split_symbol(condtition, ">=")
  elif "!=" in condtition:
      x = split_symbol(condtition, "!=")
  elif "<" in condtition:
      x = split_symbol(condtition, "<")
  elif ">" in condtition:
      x = split_symbol(condtition, ">")
  arg1, cond, arg2 = x[0], x[1], x[2]
  if cond == "==":
      return arg1 == arg2
  elif cond == ">=":
      return bool(int(arg1)) >= bool(int(arg2))
  elif cond == "<=":
      return bool(int(arg1)) <= bool(int(arg2))
  elif cond == "!=":
      return arg1 != arg2
  elif cond == "<":
      return bool(int(arg1)) < bool(int(arg2))
  elif cond == ">":
      return bool(int(arg1)) > bool(int(arg2))