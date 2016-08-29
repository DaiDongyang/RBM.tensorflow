from __future__ import print_function
import os
import sys
import gzip
import json
import shutil
import zipfile
import argparse
import subprocess
from six.moves import urllib

from IPython import embed

parser = argparse.ArgumentParser(description='Download dataset for DCGAN.')
parser.add_argument('--datasets', metavar='N', type=str, nargs='+',
                    help='name of dataset to download [celebA, lsun, mnist]')

def download(url, dirpath):
    filename = url.split('/')[-1]
    filepath = os.path.join(dirpath, filename)
    u = urllib.request.urlopen(url)
    f = open(filepath, 'wb')
    filesize = int(u.headers["Content-Length"])
    print("Downloading: %s Bytes : %s" % (filename, filesize))

    downloaded = 0
    block_sz = 8192
    status_width = 70

    while True:
        buf = u.read(block_sz)
        if not buf:
            print('')
            break
        else:
            print('', end='\r')
        downloaded += len(buf)
        f.write(buf)
        status = (("[%-"+str(status_width+1)+"s] %3.2f%%") %
                  ('=' * int(float(downloaded) / filesize * status_width) + '>', downloaded * 100. / filesize))
        print(status, end='')
        sys.stdout.flush()
    f.close()
    return filepath

def unzip(filepath):
    print("Extracting: " + filepath)
    dirpath = os.path.dirname(filepath)
    with zipfile.ZipFile(filepath) as zf:
        zf.extractall(dirpath)
    os.remove(filepath)

def download_celeb_a(dirpath):
    data_dir = 'celebA'
    if os.path.exists(os.path.join(dirpath, data_dir)):
        print('Found Celeb-A - skip')
        return
    url = "http://www.dropbox.com/sh/8oqt9vytwxb3s4r/AADIKlz8PR9zr6Y20qbkunrba/Img/img_align_celeba.zip?dl=1&pv=1"
    filepath = download(url, dirpath)
    zip_dir = ''
    with zipfile.ZipFile(filepath) as zf:
        zip_dir = zf.namelist()[0]
        zf.extractall(dirpath)
    os.remove(filepath)
    os.rename(os.path.join(dirpath, zip_dir), os.path.join(dirpath, data_dir))

def _list_categories(tag):
    pass

def _download_lsun(outdir, category, set_name, tag):
    pass

def download_lsun(dirpath):
    pass

def download_mnist(dirpath):
    data_dir = os.path.join(dirpath, 'mnist')
    if os.path.exists(data_dir):
        print('Found MNist - skip')
        return
    else:
        os.mkdir(data_dir)
    url_base = 'http://yann.lecun.com/exdb/mnist/'
    file_names = ['train-images-idx3-ubyte.gz','train-labels-idx1-ubyte.gz','t10k-images-idx3-ubyte.gz','t10k-labels-idx1-ubyte.gz']
    for file_name in file_names:
        url = (url_base+file_name).format(**locals())
        print(url)
        out_path = os.path.join(data_dir, file_name)
        cmd = ['curl', url, '-o', out_path]
        subprocess.call(cmd)
        cmd = ['gzip', '-d', out_path]
        print('Decompressing ', file_name)
        subprocess.call(cmd)

def prepare_data_dir(path = './data'):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == '__main__':
    args = parser.parse_args()

    if not args.datasets:
        raise Exception(" [!] You need to specify the namee of datasets to download")

    prepare_data_dir()

    if 'celebA' in args.datasets:
        download_celeb_a('./data')
    if 'lsun' in args.datasets:
        download_lsun('./data')
    if 'mnist' in args.datasets:
        download_mnist('./data')


