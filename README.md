# ODIS-Diff

Tool to compare ODIS-Engineering backups. It supports `xml` and `json` export files.
The `diff` file is generated in an `html` format in `result.html`.

## Project setup and usage

```
mkvirtualenv -p /usr/bin/python3 odis-diff
pip install -r requirements.txt
./odis-diff source.xml target.xml
```

## Development

You are more than welcome to `fork` this project and contribute to it.
Currently it supports a basic `vscode` integration in `.vscode`. Modify `args`
field according to your needs.