# Tamil Dictionary 2

Second attempt at dictionary lookup.

Files:
- `./main.py`: main script to launch the search website
- `./process.py`: script to convert the database files into an inverted index and postings file 
- `./search.py`: searching script for quick lookup 
- `./utils.py`: shared functions and constants
- `./letters.py`: script for processing tamil text including proper letter segmentation

generate required indices:

```
python process.py
```

run:

```
python main.py
```
(edit the mode in `main.py` to change the `mode` or remove it to default to chromium)
