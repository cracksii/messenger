import enum
import time
import colorama


class LogLevel(enum.Enum):
    INFO = 0, ""
    WARNING = 0, colorama.Fore.YELLOW
    ERROR = 0, colorama.Back.RED + colorama.Fore.BLACK
    DEBUG = 1, colorama.Fore.BLUE
    EXT_DEBUG = 2, colorama.Fore.CYAN


class DebugLevel(enum.Enum):
    NO_DEBUGGING = 0
    BASIC_DEBUGGING = 1
    EXTENDED_DEBUGGING = 2


class log:
    log_lvl = DebugLevel.NO_DEBUGGING

    def __init__(self, lg_msg, lg_lvl: LogLevel = LogLevel.INFO, client=None, clr=None):
        clr = lg_lvl.value[1] if not clr else clr
        # print(self.debug.value, lg_lvl.value[0])
        lvl = lg_lvl.name
        if self.log_lvl.value >= lg_lvl.value[0]:
            print(f"{clr}[{time.strftime('%H:%M:%S')}] | {lvl}{' ' * (len('ext_debug') - len(lvl)) } | {client.address[0] + ': ' if client else ''}{lg_msg}")
