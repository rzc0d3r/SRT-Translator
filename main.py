import sys

I_AM_EXECUTABLE = (True if (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) else False)
PATH_TO_SELF = sys.executable if I_AM_EXECUTABLE else __file__

from modules.LibraryDownloader import download_and_extract_libraries
from modules.ProgressBar import ProgressBar, CLASSIC_STYLE
from modules.FasterWhisper import FasterWhisper
from modules.SharedTools import *
from modules.MBCI import *
from modules.SRT import *

from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

from threading import Thread
from colorama import Fore, init as colorama_init

import argparse
import traceback
import platform
import pathlib
import time

VERSION = [f'v1.3.0.0', 1300]
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

SUBTITLE_BLOCKS_CREATE_THREAD = 10
TRANSCRIBE_MODEL = 'medium'
CHOICE_TRANSCRIBE_MODELS = ['tiny', 'base', 'small', 'medium', 'large']
WIN_7 = (platform.release() == '7' and sys.platform.startswith('win'))

if os.name == 'nt':
    LIBRARIES = [
        'cublas64_11.dll',
        'cublasLt64_11.dll',
        'cudnn_cnn_infer64_8.dll',
        'cudnn_ops_infer64_8.dll',
        'zlibwapi.dll'
    ]
elif os.name == 'posix':
    LIBRARIES = [
        'libcublas.so.11',
        'libcublasLt.so.11',
        'libcudnn_cnn_infer.so.8',
        'libcudnn_ops_infer.so.8'
    ]
else:
    LIBRARIES = []

args = {
    'input_file': '',
    'output_file': '',

    'source_lang': 'auto',
    'output_lang': 'english',
    'subtitle_blocks_create_thread': SUBTITLE_BLOCKS_CREATE_THREAD,
    'transcribe_model': TRANSCRIBE_MODEL,
    'custom_transcribe_model': '',
    'with_transcribe': False,
    'only_transcribe': False
}

def RunMenu():
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
            choices=['auto'] + list(GOOGLE_LANGUAGES_TO_CODES.keys()),
            default_value='auto'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Output subtitle language',
            action='choice',
            args_names='output_lang',
            choices=list(GOOGLE_LANGUAGES_TO_CODES.keys()),
            default_value='english'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Transcribe mode',
            action='store_true',
            args_names=['with-transcribe', 'only-transcribe'],
            default_value='disabled'
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Select a standart model for transcribing',
            action='choice',
            args_names='transcribe_model',
            choices=CHOICE_TRANSCRIBE_MODELS,
            default_value=TRANSCRIBE_MODEL
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Enter the name of the custom transcribe model',
            action='manual_input',
            args_names='custom_transcribe_model',
            default_value=''
        )
    )
    SettingsMenu.add_item(
        OptionAction(
            args=args,
            title='Required number of subtitle blocks to create a thread',
            action='manual_input',
            args_names='subtitle_blocks_create_thread',
            default_value=SUBTITLE_BLOCKS_CREATE_THREAD,
            data_type=int
        )
    )
    SettingsMenu.add_item(MenuAction('Back', SettingsMenu.close))

    MainMenu.add_item(MenuAction('Settings', SettingsMenu))
    MainMenu.add_item(MenuAction('Start', MainMenu.close))
    MainMenu.add_item(MenuAction('Exit', sys.exit))
    MainMenu.view()

def parse_argv():
    global args
    print(LOGO)
    if len(sys.argv) == 1: # Menu
        RunMenu()
        if args['source_lang'] != 'auto':
            args['source_lang'] = name_to_language_code(args['source_lang'])
        args['output_lang'] = name_to_language_code(args['output_lang'])
    else: # CLI
        args_parser = argparse.ArgumentParser()
        # Required
        args_parser.add_argument('-i', '--input-file', type=str, required=True, help='Specify the path to the subtitle file in .srt format that will be translated (if the transcribe argument is passed, specify the path to the audio/video file)')
        args_parser.add_argument('-o', '--output-file', type=str, required=True, help='Specify the path to the file to which the translated subtitles will be saved')
        # Optional
        args_parser.add_argument('-sl', '--source-lang', type=str, default='auto', help='Specify the input subtitle language (Specify the language code in ISO-639-1) - default value is auto (auto detect source language)')
        args_parser.add_argument('-ol', '--output-lang', type=str, default='en', help='Specify the language into which subtitles should be translated (Specify the language code in ISO-639-1) - default value is en')
        args_parser.add_argument('-sbct', '--subtitle-blocks-create-thread', type=int, default=SUBTITLE_BLOCKS_CREATE_THREAD, help=f'Specifies the required number of subtitle blocks to create 1 thread for them (example: argument = 20, subtitle file - 400 blocks, the translator will use 20 threads) - default value is {SUBTITLE_BLOCKS_CREATE_THREAD}')
        args_parser.add_argument('--transcribe-model', choices=CHOICE_TRANSCRIBE_MODELS, default=TRANSCRIBE_MODEL, help=f'Choose a model to transcribe, the larger the model, the more accurate the result, but more time and memory required - default value is {TRANSCRIBE_MODEL}')
        args_parser.add_argument('--custom-transcribe-model', type=str, default='', help='Specifies the name of the custom model from hugginface.co that will be used in transcribing (example: jvh/whisper-base-quant-ct2)')
        args_transcribe_mode = args_parser.add_mutually_exclusive_group()
        args_transcribe_mode.add_argument('--with-transcribe', action='store_true', help='Transcribes the input file (audio/video) + Translate into the specified language in --output-lang')
        args_transcribe_mode.add_argument('--only-transcribe', action='store_true', help='Only transcribes the input file (audio/video)')
        try:
            args = vars(args_parser.parse_args())
            accepted_language_codes = [lang_code for _, lang_code in GOOGLE_LANGUAGES_TO_CODES.items()]
            if args['source_lang'] not in accepted_language_codes and args['source_lang'] != 'auto':
                console_log(f"'{args['source_lang']}' is not a valid language code (accepted language codes: {', '.join(accepted_language_codes)})", ERROR)
                raise RuntimeError
            if args['output_lang'] not in accepted_language_codes:
                console_log(f"'{args['output_lang']}' is not a valid language code (accepted language codes: {', '.join(accepted_language_codes)})", ERROR)
                raise RuntimeError
        except:
            time.sleep(3)
            sys.exit(-1)

def language_code_to_name(language_code):
    for lang_name, lang_code in GOOGLE_LANGUAGES_TO_CODES.items():
        if lang_code == language_code:
            return lang_name
    return None

def name_to_language_code(language_name):
    for lang_name, lang_code in GOOGLE_LANGUAGES_TO_CODES.items():
        if lang_name == language_name:
            return lang_code
    return None

def translate(srt_data: SRT_Data):
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
    
    # define of what is required for threads
    class ThreadExceptionInterception: # class for catching an error within the thread
        def __init__(self):
            self.thread_exception = None
            self.thread_index = 0

    # main thread function
    def thread_translate(srtt: SRTTranslator, thread_index: int, threads_translated_srt_data: dict, progressbar: ProgressBar, tei: ThreadExceptionInterception):
        try:
            threads_translated_srt_data[thread_index] = srtt.translate(progressbar)
        except Exception as E:
            tei.thread_exception = (E, str(sys.exc_info()[0]))
            tei.thread_index = thread_index+1

    # thread initialization and startup
    tei = ThreadExceptionInterception()
    threads = []
    threads_translated_srt_data = {}
    
    if WIN_7:
        print('Translating...')
    
    source_lang = args['source_lang']
    if source_lang != 'auto':
        source_lang = language_code_to_name(source_lang)
    progressbar = ProgressBar(len(srt_data), "Translate progress ['{0}' -> '{1}']: ".format(source_lang, language_code_to_name(args['output_lang'])), CLASSIC_STYLE)

    for i in range(THREADS_COUNT):
        threads.append(Thread(target=thread_translate, args=(srtts[i], i, threads_translated_srt_data, progressbar, tei)))
        threads[i].start()

    # rendering of translation progress
    while True:
        try:
            if tei.thread_exception is not None:
                print('\n')
                console_log(f'[{Fore.MAGENTA}Thread {Fore.YELLOW}{tei.thread_index}{Fore.RESET}] Error: {tei.thread_exception[1]}', ERROR, False)
                console_log('Stopping the program...', INFO)
                break
            if not WIN_7: # disable rendering for windows 7 (cmd.exe does not support ASCII control characters)
                progressbar.render()
            if progressbar.is_finished:
                break
            time.sleep(0.33)
        except KeyboardInterrupt:
            os._exit(1)

    # destroying all threads
    for i in range(THREADS_COUNT):
        threads[i].join()

    return (threads_translated_srt_data, tei.thread_exception is None)

def main():
    try:
        colorama_init() 
        ecode = 0
        if len(sys.argv) == 1:
            print()
        
        if args['with_transcribe'] or args['only_transcribe']:
            console_log('Initialization Faster-Whisper... ', INFO)

            number_installed_libraries = 0
            for obj in os.listdir(pathlib.Path(PATH_TO_SELF).resolve().parent):
                if os.path.isfile(obj) and obj in LIBRARIES:
                    number_installed_libraries += 1
                    if number_installed_libraries == len(LIBRARIES):
                        break
            if number_installed_libraries != len(LIBRARIES):
                console_log('Missing libraries have been detected!!! Starting downloading...', WARN)
                if not download_and_extract_libraries(disable_progress_bar=WIN_7):
                    raise RuntimeError('Error in module: Library Downloader!!!')
    
            if args['custom_transcribe_model'] != '':
                args['transcribe_model'] = args['custom_transcribe_model']
            faster_whisper = FasterWhisper(args['transcribe_model'], None if args['source_lang'] == 'auto' else args['source_lang'])
            args['source_lang'] = faster_whisper.transcribe(args['input_file'])
            if args['source_lang'] == args['output_lang']: # skip translation if the source language is the same as the output language
                args['only_transcribe'] = True
            srt_data = faster_whisper.srt_data
            print()
        else:
            srt_data = SRT_Manager.read_from_file(args['input_file'])

        srt_data2 = SRT_Manager.compress(srt_data)
        if len(srt_data2) != len(srt_data):
            print('Compressed with {0} to {1} subtitle blocks ({2}%)\n'.format(len(srt_data), len(srt_data2), round((1-len(srt_data2)/len(srt_data))*100, 2)))
            srt_data = srt_data2

        if args['only_transcribe']:
            SRT_Manager.save_to_file(srt_data, args['output_file'])
            console_log(f'Saved to: {Fore.LIGHTYELLOW_EX}{args["output_file"]}{Fore.RESET}', WARN)
        else:
            exec_start_time = time.time()
            threads_translated_srt_data, successfully_translated = translate(srt_data)
            if successfully_translated:
                translated_srt_data = SRT_Data()
                for thread_index in range(len(threads_translated_srt_data)):
                    for srt_block in threads_translated_srt_data[thread_index]:
                        translated_srt_data.add_block(srt_block)
                console_log(f'\nThe subtitles were translated in {Fore.CYAN}{round(time.time()-exec_start_time, 2)}{Fore.RESET} second!!!', INFO, False)
                SRT_Manager.save_to_file(translated_srt_data, args['output_file'])
                console_log(f'Saved to: {Fore.LIGHTYELLOW_EX}{args["output_file"]}{Fore.RESET}', WARN)
    except Exception as E:
        ecode = 1
        traceback_string = traceback.format_exc()
        console_log(traceback_string, ERROR)
    if len(sys.argv) == 1:
        input('\nPress Enter to exit...')
    else:
        time.sleep(3) # exit-delay
    sys.exit(ecode)

if __name__ == '__main__':
    parse_argv()
    main()