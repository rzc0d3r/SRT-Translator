# All command line arguments
------------------------------------------------------------------------------------------------------------------------------------

# Required
| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --input-file  (-i)    | Specify the path to the subtitle file in .srt format that will be translated 								 |
| --output-file (-o)    | Specify the path to the file to which the translated subtitles will be saved              				 |

--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                               					                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --source-lang (-sl) | Specify the input subtitle language (Specify the language code in __ISO-639-1__) - **default value is EN**							 									 	                                   |
| --output-lang (-ol) | Specify the language into which subtitles should be translated (Specify the language code in __ISO-639-1__) - **default value is RU**                			         	   								   |
| --subtitle-blocks-create-thread (-sbct) | Specifies the required number of subtitle blocks to create 1 thread for them (example: if a subtitle file has 400 blocks, the srt-translator will use 8 threads) (**recommended: don't put it below 20, also only natural numbers are accepted!!!**) - **default value is 50** |