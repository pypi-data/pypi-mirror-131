import argparse
from pathlib import Path

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=True, help="file name")
ap.add_argument("-j", "--jsonfilename", required=True, help="output name")
args = vars(ap.parse_args())

user_file_name = args["filename"]
json_file_name = args["jsonfilename"]

content_list = []
with open(user_file_name) as f:
    for line in f:
        content_list.append(f"    {line}")

content = "".join(content_list)

code = f"""
import snoop

snoop.install(columns="", json_file_path="{json_file_name}")


@snoop
def trace():
{content}

trace()
"""

debug_code_file = f".\\vracer\\snoop_debug_{user_file_name}"

with open(debug_code_file, "w") as f:
    f.write(code)

# execute that file here
import subprocess
import sys

subprocess.run([sys.executable, debug_code_file])
