import requests
import re
import json
import time

import utils

def main():
    url = input('Input url: ')

    getfile = get_file(url)

    if getfile is None:
        print('File your trying to download is not available!')
        exit(1)

    id, filename, downloadUrl = getfile
    print('Downloading \033[1m%s\033[0m (%s)' % (filename, id))
    download(downloadUrl, outname=filename)

def get_file(url):
    webpage = requests.get(url)

    if webpage.status_code == 404:
        return None
    
    infoOptions = re.search(r"'viewerOptions', ({.+})\);", webpage.text)

    if infoOptions == None:
        raise Exception('Failed to get file source!')

    fileinfo = json.loads(infoOptions.group(1))
    
    urlid = url.replace('https://www.solidfiles.com/v/', '')
    filename = fileinfo['nodeName']
    downloadUrl = fileinfo['downloadUrl']

    return urlid, filename, downloadUrl

def download(url, outname=""):
    stream = requests.get(url, stream=True)
    filesize = int(stream.headers.get('content-length'))

    bytes_recv = 0
    startTimer = time.time()

    with open(outname, 'wb') as output:
        for chunk in stream.iter_content(1024):
            display_progress(bytes_recv, filesize, startTimer, time.time())
            bytes_recv += len(chunk)
            output.write(chunk)
            
def display_progress(recvBytes, totalBytes, startTimer, endTimer):
    downSpeed = utils.calc_speed(startTimer, endTimer, recvBytes)
    recvBytes = utils.bytesFormat(recvBytes)
    totalBytes = utils.bytesFormat(totalBytes)

    print('\r\033[K  %s of %s at %s/s' % (recvBytes, totalBytes, utils.bytesFormat(downSpeed)), end='')

if __name__ == '__main__':
    main()
