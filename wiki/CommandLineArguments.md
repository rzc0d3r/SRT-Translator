# All command line arguments
------------------------------------------------------------------------------------------------------------------------------------

# Required
| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --input-file (-i)     | Specify the path to the subtitle file in .srt format that will be translated 								 |
| --output-file (-o)    | Specify the path to the file to which the translated subtitles will be saved              				 |
--------------------------------------------------------------------------------------------------------------------------------------

# Optional
## Transcribe mode
> Need to enter only one argument from this group!!!

| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --with-transcribe     | Transcribes the input file (audio/video) + Translate into the specified language in ```--output-lang```    |
| --only-transcribe     | Only transcribes the input file (audio/video)                                                              |
--------------------------------------------------------------------------------------------------------------------------------------

## Without a group
|              Argument Command           |                                                Description                                             |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| --source-lang (-sl)                     | Specify the input subtitle language (Specify the language code in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) - **default value is EN** |
| --output-lang (-ol)                     | Specify the language into which subtitles should be translated (Specify the language code in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) - **default value is RU** |
| --subtitle-blocks-create-thread (-sbct) | Specifies the required number of subtitle blocks to create 1 thread for them (example: argument = 20, subtitle file - 400 blocks, the translator will use 20 threads) - **default value is 10** |
| --transcribe-model                      | Choose a model to transcribe, the larger the model, the more accurate the result, but more time and memory required - default value is **medium** |
| --custom-transcribe-model               | Specifies the name of the custom model from hugginface.co that will be used in transcribing (example: **jvh/whisper-base-quant-ct2**) |
