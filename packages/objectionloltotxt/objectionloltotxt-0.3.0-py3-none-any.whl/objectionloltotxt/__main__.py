#!/usr/bin/env python
from objectionloltotxt import objectiontotxt
import argparse
import os
import sys


def parse_directory_argument(directory_argument):
    for folder in directory_argument:
        if str(folder) is not None and not os.path.isdir(str(folder)):
            print(f"{folder} directory doesn't exist")
        directory_argument.remove(folder) 
        assert directory_argument != (), "all the directories you provided are invalid" # Got to Improve this
        list_of_file = os.listdir(folder)

    for file in list_of_file:
        full_path = os.path.join(folder, file)
        if file.endswith(".objection"):
            objectiontotxt.convert_base64objection_to_readable_text_file(full_path)
        else:
            print(f"please rename {full_path} to have .objection extension if the file is an objection file")

def parse_filename_argument(filename_argument):
    for file in filename_argument:
        if not os.path.isfile(file):
            print("That file doesn't exist")
            sys.exit()
        elif file.endswith(".objection"):
            objectiontotxt.convert_base64objection_to_readable_text_file(file)
        else:
            print(f"please rename \"{file}\" to have .objection extension if the file is an objection file ")

def main():
    commandline_interface = argparse.ArgumentParser(prog='objtotxt', description='Convert .objection files to txt')
    mutually_exclusive_arguments = commandline_interface.add_mutually_exclusive_group(required=True)
    mutually_exclusive_arguments.add_argument('-f', '--filename', metavar="file", type=str, nargs='+',
                                              help="Filename of the .objection file")
    mutually_exclusive_arguments.add_argument('-d', '--directory', metavar="directory", type=str, nargs='+',
                                              help='convert the .objection files in a directory to readable text file')
    args = commandline_interface.parse_args()
    input_filename = args.filename
    input_directory = args.directory

    if input_directory != None:
        parse_directory_argument(input_directory)
    else:
        parse_filename_argument(input_filename)

if __name__ == "__main__":
    main()
