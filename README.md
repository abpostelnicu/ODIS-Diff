# ODIS-Diff

Tool to compare ODIS-Engineering backups. It supports `xml` and `json` export files.
The `diff` file is generated in an `html` format in `result.html`.

## Project setup and usage

On MacOS only you must setup the virtualenvwrapper:
```
source /usr/local/bin/virtualenvwrapper.sh
```

Setup the virtualenv:
```
mkvirtualenv -p /usr/bin/python3 odis-diff
pip install -r requirements.txt
./odis-diff source.xml target.xml
```

## Development

You are more than welcome to `fork` this project and contribute to it.
Currently it supports a basic `vscode` integration in `.vscode`. Modify `args` field according to your needs.

## Notice of Non-Affiliation and Disclaimer

I'm not affiliated, associated, authorized, endorsed by, or in any way officially connected with the VOLKSWAGEN AG, or any of its subsidiaries or its affiliates. The official VOLKSWAGEN AG software or tools can be found at https://www.vw.com/.

The names VOLKWAGEN, VW and ODIS as well as related names, marks, emblems and images are registered trademarks of their respective owners.
