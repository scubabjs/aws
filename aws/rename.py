#!/usr/bin/env python3
#  Copyright (c) 2019 - Brian J. Smith
#  Version 0.4


import os
import argparse
import pathlib


def Main():
    my_parser = argparse.ArgumentParser(
        prog='rename', description='remove unneeded torrent information from media files')
    group = my_parser.add_mutually_exclusive_group()
    # Example of filename -> TV.Show.S*E*.Size.Resolution.Misc.{mp4,mkv,avi}   -> TV.Show.S*.E*.{mp4,mkv,avi}

    group.add_argument('-s', '--show', type=str,
                       help='prefix for media file is a tv series ')
    # Example of filename -> Movie Title (year).{mp4,mkv,avi}
    group.add_argument('-m', '--movie', type=str,
                       help='prefix for media file is a movie')
    args = my_parser.parse_args()

    if (args.show):
        media = args.show
        filetype = 'show'
    elif (args.movie):
        media = args.movie
        filetype = 'movie'

    print(media, filetype)
    cur_dir = pathlib.Path.cwd()
    # Could pass the path to check into this function.
    file_list = get_list_of_files(cur_dir)
    # print(file_list)
    for p in (file_list):
        print(p)


def get_list_of_files(cur_dir):

    flist = []
    for p in pathlib.Path(cur_dir).iterdir():
        if p.is_file():
            print(p)
            flist.append(p)
    return(flist)


if __name__ == '__main__':
    Main()
