#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = "Erick Sibrain, Alec"

import os
import re
import sys
import urllib.request
import argparse
import requests
import webbrowser


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    urls = []
    with open(filename, "r+") as f:
        content = f.read()
    pattern = r"/edu/languages/google-python-class/images/puzzle/\S+"
    place_pattern = r"\w+bar-\S+"
    matches = re.findall(pattern, content)
    place_matches = re.findall(place_pattern, content)
    host_name = "http://code.google.com/"
    for items in matches:
        if place_pattern in place_matches:
            sorted_urls = sorted(list(set(urls)), lambda t: t[-1])
        else:
            url = f"{host_name}{items}"
            urls.append(url)
            sorted_urls = sorted(list(set(urls)))
    return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    print("its downloading")
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    count = 0
    url_list = []
    for url in img_urls:
        count += 1
        filename = f"image{count}.jpg"
        fullpath = os.path.join(dest_dir, filename)
        urllib.request.urlretrieve(url, filename=fullpath)
        url_list.append(filename)

    with open(f"{dest_dir}/index.html", "w",) as f:
        for list_url in url_list:
            html = f"<img src='{list_url}' alt='animal_slice'/>"
            f.write(html)
    webbrowser.open_new_tab(f"{dest_dir}/index.html")


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))
        print(img_urls)


if __name__ == '__main__':
    main(sys.argv[1:])
