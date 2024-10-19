# aistudio-parser

## Name
aidstudio-parser

## Description
This is a python util for parsing a file from ai studio. It returns a file that can be attached to a new session in ai studio to continue where left off.

This can be used to continue an AI writing session or RP session.

## Prerequisites
python 3


## Instructions
1. Use the "get code" button in the upper right of AI studio to clipboard the code for the session.
2. Paste it into a notebook file or other text file.
3. Run this utility on it to produce an output file
4. Attache the output file to a new ai Studio Session
5. Cut and past instructions from the beginning of the output into the new AI studio session
5. Continue the session.

## Usage

```bash
# will generate an exchange between "user" and "model"
./ai_processor.py -i input.txt -o output.txt 

# will generate prose using only model
./ai_processor.py -i input.txt -o output.txt -m prose
```

## Help file

```bash
$ ./ai_processor.py -h
usage: ai_processor.py [-h] -i INPUT -o OUTPUT [-m {prose,exchange}] [-v] [--version]

A utility for processing input files and generating output files.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input file. Required.
  -o OUTPUT, --output OUTPUT
                        Path to the output file. Required.
  -m {prose,exchange}, --mode {prose,exchange}
                        Mode of output. "prose" outputs only model responses, "exchange" alternates between user and
                        model. Default is "exchange".
  -v, --verbose         Enable verbose (debug) mode.
  --version             Show the application version and exit.
```

## Develop and Install

### Instructions for compiling on Windows



## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
Add other input file types and other output formats

## Authors and acknowledgment
Henry Grantham

## License
Open Source

## Project status
Work in progress