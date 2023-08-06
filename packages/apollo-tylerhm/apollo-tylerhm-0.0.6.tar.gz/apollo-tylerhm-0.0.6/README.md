# Apollo

Checker complete with diff, token, and epsilon checking.

# Installation

`python3 -m pip install apollo-tylerhm --upgrade`

# Usage

usage: `apollo [-h] [-t | -e EPS] input user_output judge_output`

positional arguments:
  input              input file
  user_output        user output file
  judge_output       judge output file

optional arguments:
  -h, --help         show this help message and exit
  -t, --tok          use token checker
  -e EPS, --eps EPS  use epsilon checker
