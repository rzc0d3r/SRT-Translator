from .SharedTools import console_log, INFO, ERROR, OK
from .ProgressBar import ProgressBar, CLASSIC_STYLE

import requests
import pathlib
import zipfile
import os

def get_libraries_download_url(cuda_version=11, cude_sub_version=2):
    os_name = ''
    if os.name == 'nt':
        os_name = 'win'
    elif os.name == 'posix':
        os_name = 'linux'
    url = f'https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA{cuda_version}_{os_name}_v{cude_sub_version}.zip'
    if requests.head(url, allow_redirects=True).status_code == 200:
        return url

def download_and_extract_libraries(url=None, cuda_version=11, cude_sub_version=2, disable_progress_bar=False):
    if url is None:
        url = get_libraries_download_url(cuda_version, cude_sub_version)
        if url is None:
            console_log('Could not find libraries for your system!!!', ERROR)
            return False
    try:
        response = requests.get(url, stream=True)
        try:
            filename = response.headers.get('content-disposition').split('filename=')[1]
            console_log(f'Downloading {filename}...', INFO)
        except:
            pass
        total_length = response.headers.get('content-length')
        if total_length is None or disable_progress_bar: # No content length header
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            task = ProgressBar(int(total_length), '           ', CLASSIC_STYLE)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        task.update(len(chunk))
                        task.render()
        zip_path = str(pathlib.Path(filename).resolve())
        console_log('Successfully downloaded!!!', OK)
        console_log('Extracting libraries...', INFO)
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall()
        console_log('Successfully extracted!!!', OK)
        return True
    except Exception as e:
        console_log(f"Error downloading or extracting files: {e}", ERROR)
        return False