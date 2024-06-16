# All command line arguments
------------------------------------------------------------------------------------------------------------------------------------

# Required
| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --input-file          | Specify the path to the subtitle file in .srt format that will be translated 								 |
| --output-file         | Specify the path to the file to which the translated subtitles will be saved              				 |

--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                               					       |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --source-lang | Specify the input subtitle language (Specify the language code in __ISO-639-1__) - **default value is EN**							 									 	       |
| --target-lang | Specify the language into which subtitles should be translated (Specify the language code in __ISO-639-1__) - **default value is RU**                			         			   |
| --batch-size  | the maximum size of text that can be translated in one pass (the larger the value, the faster the translation will be done, but critical errors may occur) - **default value is 20** | 