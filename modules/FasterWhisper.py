from faster_whisper import WhisperModel
from colorama import Fore

from .ProgressBar import ProgressBar, CLASSIC_STYLE
from .SharedTools import console_log, INFO, ERROR, WARN
from .SRT import SRT_Data, SRT_Block

from time import time

class FasterWhisper:
    def __init__(self, model_name: str, language=None):
        self.model_name = model_name
        self.model = None
        self.language = language
        self.srt_data = None
        console_log(f'Model used: {Fore.CYAN}{self.model_name}{Fore.RESET}', INFO)
        try:
            console_log(f'Attempt to start execution on CUDA-device...', INFO)
            self.model = WhisperModel(model_name, device="cuda")
        except:
            console_log('Error starting execution on CUDA-device!!!', ERROR)
            console_log('Attempt to start execution on CPU-device...', INFO)
            try:       
                self.model = WhisperModel(model_name, device="cpu")
            except:
                console_log('Error starting execution on CPU-device!!!', ERROR)
                raise RuntimeError('Unable to start transcribing!!!')
        if language is not None and language not in self.model.supported_languages:
            raise ValueError(f"'{language}' is not a supported by the model (supported language codes: {', '.join(self.model.supported_languages)})")

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"
    
    def transcribe(self, path_to_file: str):
        segments, info = self.model.transcribe(path_to_file, beam_size=5, word_timestamps=True)
        if self.language is not None and info.language != self.language and info.language_probability >= 0.85:
            console_log(f"Detected language '{info.language}' with probability {round(info.language_probability, 2)}, but you specified '{self.language}', language changed to '{info.language}'\n", INFO)
            segments, info = self.model.transcribe(path_to_file, beam_size=5, language=info.language)
        else:
            console_log(f"Detected language '{info.language}' with probability {round(info.language_probability, 2)}", INFO)
            if info.language_probability < 0.85:
                console_log('The model may not have detected the language accurately, it is recommended to specify the language explicitly!!!\n', WARN)
            else:
                print()
        exec_start_time = time()
        progressbar = ProgressBar(int(info.duration), 'Transcribing: ', CLASSIC_STYLE)
        segment_index = 0
        self.srt_data = SRT_Data()
        for segment in segments:
            segment_index += 1
            segment_start = self.format_time(segment.start)
            segment_end = self.format_time(segment.end)
            srt_block = SRT_Block(segment_index, [segment_start, segment_end], segment.text.strip())
            self.srt_data.add_block(srt_block)
            progressbar.update(int(segment.end), True)
            progressbar.render()
        if not progressbar.is_finished:
            progressbar.force_finish()
            progressbar.render()
        console_log(f'\nTranscribing completed for {Fore.CYAN}{round(time()-exec_start_time, 2)}{Fore.RESET} second!!!', INFO, False)
        return info.language