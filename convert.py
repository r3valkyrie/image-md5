#!/usr/bin/env python3

"""
Generates an MD5 hash for every image in the in/ directory,
then moves them to a specified directory before running wpg -a on them.
"""

import argparse

from subprocess import run
from hashlib import md5
from PIL import Image
from os import rename
from filetype import guess


class ImageMD5:
    def __init__(self, wpg, outpath, images):
        if outpath[-1] != '/':
            self.outpath = outpath + '/'
        else:
            self.outpath = outpath
        self.images = images
        self.wpg = wpg

    def get_files(self):
        for file in self.images:
            yield file

    def conversion(self):
        for filename in self.get_files():
            md5hash = md5(Image.open(filename).tobytes())
            filetype = guess(filename)
            new_file = f'{self.outpath}{md5hash.hexdigest()}.{filetype.extension}'

            try:
                rename(filename, new_file)
            except Exception as exception:
                raise exception
            finally:
                print(f'Moved {filename}\n to: {new_file}')

            if self.wpg:
                try:
                    run(['wpg', '-a', new_file])
                except FileNotFoundError:
                    print('wpg not found in $PATH, ignoring...')
                    continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate md5 hashes from images, rename them, '
                                                 'move them, and optionally run wpg on them.')
    parser.add_argument('-o', '--out', default='./',
                        type=str, help='Directory where converted images are outputted.')
    parser.add_argument('-w', '--wpg',
                        action='store_true', help='Run wpg on the converted images.')
    parser.add_argument('FILES', nargs='+', help='Files to be converted.')

    args = vars(parser.parse_args())
    ImageMD5(args['wpg'], args['out'], args['FILES']).conversion()
