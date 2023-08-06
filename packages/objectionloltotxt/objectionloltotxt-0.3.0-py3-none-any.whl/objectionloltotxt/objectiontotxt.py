import base64
import json
import os
import sys


def base64_to_json(filename):
    """
    Opens the specified .objection or any base64 encoded file and converts it to
    prettyprint json. It will create the
    file to the directory of the file that is passed
    """
    assert filename.endswith(
        ".objection"), "the file you provided isn't a .objection file, if it is please make the file extension " \
                       ".objection "
    with open(filename + "_converted.json", 'w') as output_file, open(filename, 'r') as input_file:
        base64_input = input_file.read()
        base64_decoded_input = base64.b64decode(base64_input).decode()
        json_input = json.loads(base64_decoded_input)
        json.dump(json_input, output_file, sort_keys=True, indent=0)
        output_file.close()
        input_file.close()


def convert_objection_json_to_readable_text_file(filename):
    """
    Opens the specified converted objection file and converts it to readable
    text file. It will create the file to the directory of the file that is
    passed
    """
    with open(filename + "_readable_file.txt", 'w') as readable_file_output, open(filename, 'r') as objection_json_file:
        objection_python_dict = json.loads(objection_json_file.read())
        for frame in objection_python_dict["frames"]:
            readable_file_output.write(frame["username"] + ": " + frame["text"] + "\n\n")
        readable_file_output.close()
        objection_json_file.close()


def convert_base64objection_to_readable_text_file(filename):
    """
    Combines the other functions, not producing the .json output
    """
    assert filename.endswith(
        ".objection"), "the file you provided isn't a .objection file, if it is please make the file extension " \
                       ".objection "
    with open(filename + "_readable_file.txt", 'w') as readable_file_output, open(filename, 'r') as input_file:
        base64_input = input_file.read()
        base64_decoded_input = base64.b64decode(base64_input).decode()
        json_input = json.loads(base64_decoded_input)
        json_to_be_made_readable = json.dumps(json_input, sort_keys=True, indent=0)
        objection_python_dict = json.loads(json_to_be_made_readable)

        try: # Some older .objection files only have "frames" schema and nothing else, when trying to reach "frames" they raise
             # TypeError so if we get a TypeError when trying to reach "frames" the program instead reaches the only root schema
            for frame in objection_python_dict["frames"]:
                readable_file_output.write(frame["username"] + ": " + frame["text"] + "\n\n")
        except TypeError:
            for frame in objection_python_dict:
                readable_file_output.write(frame["username"] + ": " + frame["text"] + "\n\n")

        readable_file_output.close()
        input_file.close()
