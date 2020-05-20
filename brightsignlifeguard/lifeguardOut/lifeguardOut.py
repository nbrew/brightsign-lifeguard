from __future__ import print_function
import shutil
import os
import xml.etree.cElementTree as ElementTree
import argparse
import logging
from copyfile import copyFile


def theprogram():
    parser = argparse.ArgumentParser()
    parser.add_argument("presentation_directory",
        # nargs=1,
        help="Root directory containing Brightsign presentation (current-sync.xml + pool/).")
    parser.add_argument('--dry-run',
        action='store_true',
        required=False,
        help='Just print what would happen. No modifications made.',
        default=False,
        dest='dry_run')
    args = parser.parse_args()
    PRESENTATION_LOCATION = args.presentation_directory
    DRY_RUN = args.dry_run

    if os.path.isdir(PRESENTATION_LOCATION):
        if PRESENTATION_LOCATION[-1] != '/':
            PRESENTATION_LOCATION = PRESENTATION_LOCATION + '/'
    else:
        print("ERROR: Target not a valid directory. (Sorry)")
        exit()

    if not os.path.isdir(PRESENTATION_LOCATION+"kiddie_pool"):
        os.mkdir(PRESENTATION_LOCATION+"kiddie_pool")


    sync_file = 'current-sync.xml'
    if not os.path.isfile(PRESENTATION_LOCATION + sync_file):
        sync_file = 'local-sync.xml'

    if not os.path.isfile(PRESENTATION_LOCATION + sync_file):
        print("""Presentation directory is missing a current-sync.xml or local-sync.xml file.
            Probably not a full Brightsign Presentation folder""")
        exit()

    tree = ElementTree.parse(PRESENTATION_LOCATION + sync_file)
    root = tree.getroot()
    if sync_file == 'current-sync.xml':
        baseurl = root.find('./meta/client/base').text
    else:
        baseurl = PRESENTATION_LOCATION

    for elem in root.findall('.//download'):
        name = elem.find('.//name').text
        urlpath = elem.find('.//link').text
        if sync_file == 'current-sync.xml':
            filepath = PRESENTATION_LOCATION + urlpath[len(baseurl)+1:]
        else:
            filepath = PRESENTATION_LOCATION + urlpath

        outpath = os.path.abspath(PRESENTATION_LOCATION+"kiddie_pool/"+name)
        if DRY_RUN:
            print('Would copy ' + filepath + ' to ' + outpath)
        else:
            copyFile(os.path.abspath(filepath), outpath)

    print("Adult swim is over. Presentation files are now in the kiddle_pool.")
