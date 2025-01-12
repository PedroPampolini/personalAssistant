import env
from colorama import Fore, Style
from datetime import datetime

def debug(*args):
  if env.DEBUG:
    timeNow = datetime.now().strftime("%H:%M:%S")
    print(Fore.MAGENTA + f"[{timeNow}]: " + Style.RESET_ALL, end='')
    print(*args)