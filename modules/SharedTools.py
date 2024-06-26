from colorama import Fore, Style, init as colorama_init

colorama_init()

class LoggerType:
    def __init__(self, sborder, eborder, title, color, fill_text):
        self.sborder = sborder
        self.eborder = eborder
        self.title = title
        self.color = color
        self.fill_text = fill_text

    @property
    def data(self):
        return self.sborder + self.color + self.title + Fore.RESET + self.eborder

ERROR = LoggerType('[ ', ' ]', 'FAILED', Fore.RED, True)
OK = LoggerType('[   ', '   ]', 'OK', Fore.GREEN, False)
INFO = LoggerType('[  ', '  ]', 'INFO', Fore.LIGHTBLACK_EX, True)
DEVINFO = LoggerType('[ ', ' ]', 'DEBUG', Fore.CYAN, True)
WARN = LoggerType('[  ', '  ]', 'WARN', Fore.YELLOW, False)

def console_log(text='', logger_type=None, fill_text=None):
    if isinstance(logger_type, LoggerType):
        ni = 0
        for i in range(0, len(text)):
            if text[i] != '\n':
                ni = i
                break
            print()
        if logger_type.fill_text and fill_text is None:
            fill_text = True
        if logger_type.fill_text and fill_text:
            print(logger_type.data + ' ' + logger_type.color + text[ni:] + Fore.RESET)
        else:
            print(logger_type.data + ' ' + text[ni:])
    else:
        print(text)