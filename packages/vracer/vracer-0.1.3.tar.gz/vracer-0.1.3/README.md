installation

```bash
pip install vracer
```

usage

```bash
python -m vracer -f path_to_file_to_be_debugged.py -j path_to_output_debugged_json_file.json

# or

python -m vracer --filename some_python_file.py --jsonfilename output_file_path.json
```

this library is based on snoop debugger library.

it creates a trace of the code that is passed (python fbvile) along with tracking the change of variables value. The tracked output is outputted as a json file.
