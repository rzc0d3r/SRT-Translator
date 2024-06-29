from modules.MBCI import *
from modules.SRT import *
from modules.SharedTools import *
from modules.ProgressBar import ProgressBar, CLASSIC_STYLE

from threading import Thread
from colorama import Fore, init as colorama_init

import argparse
import traceback
import platform
import time
import sys

VERSION = [f'v1.2.0.0', 1200]
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
    'output_lang': 'ru',
    'subtitle_blocks_create_thread': 50
}

def run_mbci():
    MainMenu = ViewMenu(LOGO+'\n---- Main Menu ----')
    
    SettingsMenu = ViewMenu(LOGO+'\n---- Settings Menu ----')
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Path to input file',
            action='manual_input',
            args_names='input_file',
            default_value=''
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Path to output file',
            action='manual_input',
            args_names='output_file',
            default_value=''
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Source subtitle language',
            action='choice',
            args_names='source_lang',
            choices=['en', 'ru', 'uk'],
            default_value='en'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Output subtitle language',
            action='choice',
            args_names='output_lang',
            choices=['en', 'ru', 'uk'],
            default_value='ru'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Required number of subtitle blocks to create a thread',
            action='manual_input',
            args_names='subtitle_blocks_create_thread',
            default_value=50,
            data_type=int
        )
    )
    SettingsMenu.add_item(MenuAction('Back', MainMenu))

    MainMenu.add_item(MenuAction('Settings', SettingsMenu))
    MainMenu.add_item(MenuAction(f'{Fore.LIGHTWHITE_EX}Do it, damn it!{Fore.RESET}', main))
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
        args_parser.add_argument('-sbct', '--subtitle-blocks-create-thread', type=int, default=50, help='Specifies the required number of subtitle blocks to create 1 thread for them (example: if a subtitle file has 400 blocks, the srt-translator will use 8 threads) (recommended: don\'t put it below 20, also only natural numbers are accepted!!!) - default value is 50')
        
        try:
            global args
            args = vars(args_parser.parse_args())
        except:
            time.sleep(3)
            sys.exit(-1)

def main():
    try:
        colorama_init()
        srt_data = SRT_Manager.read_from_file(args['input_file'])
        if len(sys.argv) == 1:
            print()

        # multithreading initialization
        REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD = args['subtitle_blocks_create_thread']
        if len(srt_data) < REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD or len(srt_data)//REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD == 1:
            THREADS_COUNT = 1
            len_srt_data_tbatch = REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD
        else:
            THREADS_COUNT = len(srt_data)//REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD # there is 1 thread for every REQUIRED_SUBTITLE_BLOCKS_CREATE_THREAD subtitle blocks
            len_srt_data_tbatch = len(srt_data)//THREADS_COUNT
        # srt_data allocation for each threads
        srtts = []
        len_residue_srt_data_tbatch = len(srt_data)-(len_srt_data_tbatch*THREADS_COUNT)
        if len_residue_srt_data_tbatch > 0:
            THREADS_COUNT += 1
        console_log(f'Initialization of {THREADS_COUNT} threads...\n', INFO)

        for i in range(0, THREADS_COUNT): # for main threads (here len(srt_data_thread) identical for all threads)
            srt_data_thread = srt_data.get_blocks((i*len_srt_data_tbatch), (i+1)*len_srt_data_tbatch, True)
            srtt_thread = SRTTranslator(srt_data_thread, args['source_lang'], args['output_lang'])
            srtts.append(srtt_thread)
        if len_residue_srt_data_tbatch > 0: # if not everything fits in the main threads, everything else goes to the additional thread
            residue_srt_data_thread = srt_data.get_blocks(len_srt_data_tbatch*(THREADS_COUNT-1), len(srt_data), True)
            srtt_thread = SRTTranslator(residue_srt_data_thread, args['source_lang'], args['output_lang'])
            srtts.append(srtt_thread)
        
        # thread initialization and startup
        class TranslateThread(Thread):
            def __init__(self, srtt: SRTTranslator, progressbar: ProgressBar):
                Thread.__init__(self)
                self.srtt = srtt
                self.results = None
                self.progressbar = progressbar
                
            def run(self):
                try:
                    self.results = self.srtt.translate(progressbar)
                except Exception as E:
                    console_log(f'[{Fore.MAGENTA}{self.name}{Fore.RESET}] Error: {str(sys.exc_info()[0])}', ERROR, False)
                    os._exit(-1)  

        threads = []
        progressbar = ProgressBar(len(srt_data), 'Translate progress: ', CLASSIC_STYLE)

        exec_start_time = time.time()
        for i in range(THREADS_COUNT):
            threads.append(TranslateThread(srtts[i], progressbar))
            threads[i].start()
        
        # rendering of translation progress
        OK = False
        try:
            while True:
                if progressbar.is_finished:
                    progressbar.render()
                    OK = True
                    break
                progressbar.render()
                time.sleep(0.33)
        except KeyboardInterrupt:
            os._exit(-1)

        # saving translation results to a file
        if OK: # if there were no errors in the threads
            translated_srt_data = SRT_Data()
            for thread in threads:
                for srt_block in thread.results:
                    translated_srt_data.add_block(srt_block)

            if platform.system().lower() == 'windows' and platform.release() not in ['10']: # fix for old Windows
                console_log(f'\nThe subtitles were translated in {Fore.CYAN}{round(time.time()-exec_start_time, 2)}{Fore.RESET} second!!!', INFO, False)
            else:
                console_log(f'The subtitles were translated in {Fore.CYAN}{round(time.time()-exec_start_time, 2)}{Fore.RESET} second!!!', INFO, False)
            SRT_Manager.save_to_file(translated_srt_data, args['output_file'])
            console_log(f'Saved to: {Fore.LIGHTYELLOW_EX}{args["output_file"]}{Fore.RESET}', WARN)

    except Exception as E:
        traceback_string = traceback.format_exc()
        console_log(traceback_string, ERROR)
    if len(sys.argv) == 1:
        input('\nPress Enter to exit...')
    else:
        time.sleep(3) # exit-delay
    sys.exit(1)

if __name__ == '__main__':
    parse_argv() # if Menu, the main function will be called in automatic mode
    if len(sys.argv) > 1: # CLI
        main()
