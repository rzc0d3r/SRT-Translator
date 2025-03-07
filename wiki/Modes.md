# Modes

---

## Transcribe
There are 2 sub-modes:
* ```--with-transcribe``` - Extracts text from the audio or video that was specified in the ```--input-file``` argument and translates the extracted result into the language specified in ```--output-lang``` and saves it to a file specified in ```--output-file```.
* ```--only-transcribe``` - Only extracts text from the audio or video that was specified in the ```--input-file``` argument and saves the extracted result to a file specified in ```--output-file```.

### Screenshots
![Windows](https://github.com/rzc0d3r/SRT-Translator/blob/main/img/mbci_transcribe_mode_example.png)

![Windows](https://github.com/rzc0d3r/SRT-Translator/blob/main/img/execution_transcribe_mode_example.png)

---

## Translate
If you do not specify the following command line arguments:
* ```--with-transcribe```
* ```--only-transcribe```

Then the program works in the translator mode (original behavior before v1.3.0.0), and ```--input-file``` argument expects the path to the subtitle file in **.srt** format.

This file will be translated into the language specified in the ```--output-lang``` argument, and the result will be saved to the file specified in ```--output-file```.

### Screenshots
![Windows](https://github.com/rzc0d3r/SRT-Translator/blob/main/img/mbci_translate_mode_example.png)

![Windows](https://github.com/rzc0d3r/SRT-Translator/blob/main/img/execution_translate_mode_example.png)
