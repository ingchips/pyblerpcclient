from datetime import datetime

LOG_LEVEL_DBG   = 1
LOG_LEVEL_INFO  = 2
LOG_LEVEL_WARN  = 3
LOG_LEVEL_ERROR = 4

LOG_LEVEL = LOG_LEVEL_DBG

FAIL_COLOR = "\033[31;1m"
PASS_COLOR = "\033[32;1m"
WARN_COLOR = "\033[33;1m"
COLOR_END  = "\033[0m"

def PRINT(prefix: str, msg: str) -> None:
    print(datetime.now().strftime('[%m-%d %H:%M:%S.%f] '), end='')
    print(prefix, end='')
    print(msg)

def LOG_D(msg: str) -> None:
    if LOG_LEVEL <= LOG_LEVEL_DBG:
        PRINT("[DBG ] ", msg)

def LOG_I(msg: str) -> None:
    if LOG_LEVEL <= LOG_LEVEL_INFO:
        PRINT("[INFO] ", msg)

def LOG_W(msg: str) -> None:
    if LOG_LEVEL <= LOG_LEVEL_WARN:
        PRINT("[" + WARN_COLOR + "WARN" + COLOR_END + "] ", msg)

def LOG_E(msg: str) -> None:
    if LOG_LEVEL <= LOG_LEVEL_ERROR:
        PRINT("[" + FAIL_COLOR + "ERR " + COLOR_END + "] ", msg)


def LOG_PROG(msg: str):  PRINT("[....] ", msg)
def LOG_PASS(msg: str):  PRINT("[" + PASS_COLOR + "PASS" + COLOR_END + "] ", msg)
def LOG_FAIL(msg: str):  PRINT("[" + FAIL_COLOR + "FAIL" + COLOR_END + "] ", msg)
def LOG_OK(msg: str)  :  PRINT("[" + PASS_COLOR + " OK " + COLOR_END + "] ", msg)

def LOG_PLAIN(msg: str): PRINT('', msg)
