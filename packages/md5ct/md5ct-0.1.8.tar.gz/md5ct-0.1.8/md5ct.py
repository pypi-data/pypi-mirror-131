import os
import logging
from pathlib import Path
import time
import argparse
import random

CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

__VERSION__ = '0.1.8'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

TIME = lambda: int(time.time() * 1000)

old_file = set()
file_extensions = '.DS_Store', '.ini'
input_base_path = ''


def get_parser():
    parser = argparse.ArgumentParser(
        description='批量修改文件md5',
    )

    parser.add_argument(
        'path',
        metavar='PATH',
        type=str,
        help='文件或者文件夹路径',
    )
    parser.add_argument(
        '-r', '--reverse', action='store_true',
        help='是否将文件名反转'
    )
    parser.add_argument('-v', '--version',
                        action='version', version=__VERSION__, help='显示当前版本号')

    return parser


def checkIsNotIncludeFile(file):
    for extension in file_extensions:
        if extension in file:
            return False
    else:
        return True


def fileAppend(filename):
    random_str = ''.join(random.choice(CHARACTERS))
    temp = open(filename, 'a')

    temp.write(random_str)
    temp.close()


def reverse_string(a_string):
    return a_string[::-1]


def reverse_path(path_str):
    reverse_path_list = []
    for p in path_str.split(os.sep):
        reverse_path_list.append(reverse_string(p))
    return os.sep.join(reverse_path_list)


def changeMd5(path, reverse):
    if Path(path).exists():

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):

                for file in files:
                    filename = os.path.join(root, file)
                    fileAppend(filename)

                    if checkIsNotIncludeFile(file) and reverse:
                        (base_path, realfilename) = os.path.split(filename)
                        (file, ext) = os.path.splitext(filename)
                        extra_path = base_path.replace(input_base_path, '')
                        new_file = os.path.join(input_base_path, reverse_path(extra_path),
                                                (reverse_string(realfilename.replace(ext, ""))) + ext)
                        if new_file not in old_file:
                            os.renames(filename, new_file)
                            print('处理：' + new_file)
                else:
                    for directory in dirs:
                        changeMd5(root + "/" + directory, reverse)
        else:
            fileAppend(path)
            if checkIsNotIncludeFile(path) and reverse:
                (base_path, filename) = os.path.split(path)
                (file, ext) = os.path.splitext(path)
                extra_path = base_path.replace(input_base_path, '')
                os.renames(path, os.path.join(input_base_path,reverse_path(extra_path),  reverse_string(filename.replace(ext, "")) + ext))
                print('处理：' + os.path.join(input_base_path, reverse_string(extra_path),
                                           reverse_string(filename.replace(ext, "")) + ext))

    else:
        if path is not None:
            logging.error('路径不存在:' + path)
        else:
            logging.error('请出入路径:')


def addFileCache(path):
    if Path(path).exists():

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):

                for file in files:
                    filename = os.path.join(root, file)
                    old_file.add(filename)
                else:
                    for directory in dirs:
                        addFileCache(root + "/" + directory)
        else:
            old_file.add(path)
    else:
        if path is not None:
            logging.error('路径不存在:' + path)
        else:
            logging.error('请出入路径:')


def cli():
    args = vars(get_parser().parse_args())
    path = os.path.abspath(args.get('path', None))
    global input_base_path
    input_base_path = path + '/'
    reverse = args.get('reverse', False)
    begin = TIME()
    addFileCache(path)
    changeMd5(path, reverse)
    print("用时：" + str(TIME() - begin) + '毫秒')


if __name__ == '__main__':
    cli()
