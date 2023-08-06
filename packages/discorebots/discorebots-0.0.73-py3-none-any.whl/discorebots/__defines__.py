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