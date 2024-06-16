from deep_translator import GoogleTranslator

import argparse
import time
import sys
import os

VERSION = ['v1.0.0.0', 1000]
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

def parseSRTFile(path):
    srt_data = {}
    srt_batch = []
    f = open(path, 'r')
    for line in f.readlines():
        line = line.strip()
        if line == '':
            srt_data[int(srt_batch[0])] = [srt_batch[1], srt_batch[2:]]
            srt_batch = []
        else:
            srt_batch.append(line)
    return srt_data

def translateSRTFile(path, source_lang, target_lang, batch_size):
    srt_data = parseSRTFile(path)
    translated_srt_data = {}
    translator = GoogleTranslator(source_lang, target_lang)
    index = 1
    tindex = -(batch_size-1)
    text_batch = ''
    available_batchs = len(srt_data)//batch_size
    for index in range(1, available_batchs*batch_size+1):
        text_batch += ('\n'.join(srt_data[index][1])+'\n#\n')
        if index%batch_size==0:
            translated_text_batch = translator.translate(text_batch.strip()).split('#')
            for translated_text in translated_text_batch:
                translated_text = translated_text.strip()
                if translated_text != '':
                    translated_srt_data[tindex+index] = [srt_data[tindex+index][0], translated_text.split('\n')]
                    tindex += 1
            text_batch = ''
            tindex = -(batch_size-1)
            os.system('cls')
            print(f'{len(translated_srt_data)} of {len(srt_data)} blocks of Subtitles translated!')
    for index in range(index+1, len(srt_data)+1):
        translated_text = translator.translate('\n'.join(srt_data[index][1]).strip()).strip()
        if translated_text != '':
            translated_srt_data[index] = [srt_data[index][0], translated_text.split('\n')]
        os.system('cls')
        print(f'{len(translated_srt_data)} of {len(srt_data)} blocks of Subtitles translated!')
    return translated_srt_data

def saveSRTFile(srt_data, path):
    f = open(path, 'w')
    for index in srt_data:
        vtime, text = srt_data[index]
        f.write(str(index)+'\n')
        f.write(vtime+'\n')
        f.write('\n'.join(text))
        f.write('\n\n')
    f.close()

if __name__ == '__main__':
    print(LOGO)
    args_parser = argparse.ArgumentParser()
    # Required
    args_parser.add_argument('--input-file', type=str, required=True)
    args_parser.add_argument('--output-file', type=str, default='', required=True)
    # Optional
    args_parser.add_argument('--source-lang', type=str, default='en')
    args_parser.add_argument('--target-lang', type=str, default='ru')
    args_parser.add_argument('--batch-size', type=int, default=20)
    try:
        global args
        args = vars(args_parser.parse_args())
    except:
        time.sleep(3)
        sys.exit(-1)
    translated_srt = translateSRTFile(args['input_file'], args['source_lang'], args['target_lang'], args['batch_size'])
    saveSRTFile(translated_srt, args['output_file'])