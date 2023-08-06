import subprocess
import argparse
import site
import sys

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

debug_code_file = Path(
    f"{site.getusersitepackages()}/vracer/snoop_debug_{Path(user_file_name).stem}"
)

with open(debug_code_file, "w") as f:
    f.write(code)


# execute that file
# subprocess.run([sys.executable, debug_code_file])
process = subprocess.run([sys.executable, debug_code_file], stderr=subprocess.PIPE)

if process.returncode != 0:
    print("this is an error", process.stderr.decode("utf-8"))
    import json

    with open(json_file_name, "w") as f:
        json.dump({"error": process.stderr.decode("utf-8")}, f)


# removes the file
debug_code_file.unlink()
