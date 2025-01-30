import os, sys

sys.path.append(os.path.relpath("src"))

from discord_bot import *

discord_bot = StudyBot()
discord_bot.run()