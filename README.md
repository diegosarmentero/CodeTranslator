CodeTranslator
==============

Localize source code api from one language to another


DEPENDENCIES
============

- pip install astor


USAGE
=====

code_translator.py [-h] [-p Project to PO] [-t Translate Project]
                          [-o Output Folder]

$code_translator -p project_path [-o output_path] [-t project_path]

optional arguments:
  -h, --help            show this help message and exit
  -p Project to PO, --po Project to PO
                        Read the source code of this project and generate po
                        files
  -t Translate Project, --translate Translate Project
                        Source code to translate
  -o Output Folder, --output Output Folder
                        Place to locate the outpur result

This program comes with ABSOLUTELY NO WARRANTY.This is free software, and you
are welcome to redistribute it under certain conditions; for details see
LICENSE.txt.
