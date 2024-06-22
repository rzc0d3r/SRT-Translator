from modules.MBCI import *
from modules.SRT import *
from modules.SharedTools import *

import argparse
import traceback
import time
import sys

VERSION = ['v1.1.0.0', 1100]
LOGO = f"""
███████╗██████╗ ████████╗                                                            
██╔════╝██╔══██╗╚══██╔══╝                                                            
███████╗██████╔╝   ██║                                                               
╚════██║██╔══██╗   ██║                                                               
███████║██║  ██║   ██║                                                               
╚══════╝╚═╝  ╚═╝   ╚═╝                                                               
████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗ ██████╗ ██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                    Project Version: {VERSION[0]}
                                                    Project Devs: rzc0d3r        
"""

args = {
    'input_file': '',
    'output_file': '',

    'source_lang': 'en',
    'output_lang': 'ru'
}

def run_mbci():
    MainMenu = ViewMenu(LOGO+'\n---- Main Menu ----')
    
    SettingsMenu = ViewMenu(LOGO+'\n---- Settings Menu ----')
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='path to input file',
            action='manual_input',
            args_names='input_file',
            default_value=''
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='path to output file',
            action='manual_input',
            args_names='output_file',
            default_value=''
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='source subtitle language',
            action='choice',
            args_names='source_lang',
            choices=['en', 'ru', 'uk'],
            default_value='en'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='output subtitle language',
            action='choice',
            args_names='output_lang',
            choices=['en', 'ru', 'uk'],
            default_value='ru'
        )
    )
    SettingsMenu.add_item(MenuAction('Back', MainMenu))

    MainMenu.add_item(MenuAction('Settings', SettingsMenu))
    MainMenu.add_item(MenuAction(f'{colorama.Fore.LIGHTWHITE_EX}Do it, damn it!{colorama.Fore.RESET}', main))
    MainMenu.add_item(MenuAction('Exit', sys.exit))
    MainMenu.view()

def parse_argv():
    print(LOGO)
    if len(sys.argv) == 1: # Menu
        run_mbci()
    else: # CLI
        args_parser = argparse.ArgumentParser()
        # Required
        args_parser.add_argument('-i', '--input-file', type=str, required=True, help='Specify the path to the subtitle file in .srt format that will be translated')
        args_parser.add_argument('-o', '--output-file', type=str, default='', required=True, help='Specify the path to the file to which the translated subtitles will be saved')
        # Optional
        args_parser.add_argument('-sl', '--source-lang', type=str, default='en', help='Specify the input subtitle language (Specify the language code in ISO-639-1) - default value is EN')
        args_parser.add_argument('-ol', '--output-lang', type=str, default='ru', help='Specify the language into which subtitles should be translated (Specify the language code in ISO-639-1) - default value is RU')
        try:
            global args
            args = vars(args_parser.parse_args())
        except:
            time.sleep(3)
            sys.exit(-1)

def main():
    try:
        srt_data = SRT_Manager.read_from_file(args['input_file'])
        if len(sys.argv) == 1:
            print()
        srtt = SRTTranslator(srt_data, args['source_lang'], args['output_lang'])
        srtt.init()
        SRT_Manager.save_to_file(srtt.translate(), args['output_file'])
        print('\nSaved to:', args['output_file'])
    except Exception as E:
        traceback_string = traceback.format_exc()
        console_log(traceback_string, ERROR)
    if len(sys.argv) == 1:
        input('\nPress Enter to exit...')
    else:
        time.sleep(3) # exit-delay
    sys.exit()

if __name__ == '__main__':
    parse_argv() # if Menu, the main function will be called in automatic mode
    if len(sys.argv) > 1: # CLI
        main()