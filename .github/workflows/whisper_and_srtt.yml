name: Whisper + SRTT
on:
  workflow_dispatch:
    inputs:
      url_data:
        description: URL to Video/Audio file
        required: true
      output_language:
        description: Output subtitle language (Code)
        required: true
jobs:
  Preparing-Environment:
    runs-on: windows-latest
    steps:
      - name: Download WinWhisper
        run: |
          mkdir env
          cd env
          Invoke-WebRequest -Uri "https://github.com/GewoonJaap/WinWhisper/releases/download/V1.3.2/WinWhisper-1.3.2-standalone.zip" -OutFile "winwhisper.zip"
          Expand-Archive -Path "winwhisper.zip" -DestinationPath .
      - name: Download SRT-Translator
        run: |
          Invoke-WebRequest -Uri "https://github.com/rzc0d3r/SRT-Translator/releases/download/v1.2.0.0/SRT-Translator_v1.2.0.0_win64.exe" -OutFile "srtt.exe"
          Get-ChildItem -Path .\
  
  
