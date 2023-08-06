import os
from pathlib import Path

from .. import api

description = """
Find all filenames matching a specified pattern recursively.

This command will recursively find all the filenames matching a specified
pattern and then return their absolute paths.
"""

epilog = f"""
[Example] Find VCF files in the current directory:
  $ fuc {api.common._script_name()} "*.vcf"

[Example] Find specific VCF files:
  $ fuc {api.common._script_name()} "*.vcf.*"

[Example] Find zipped VCF files in a specific directory:
  $ fuc {api.common._script_name()} "*.vcf.gz" --dir ~/test_dir
"""

def create_parser(subparsers):
    parser = api.common._add_parser(
        subparsers,
        api.common._script_name(),
        description=description,
        epilog=epilog,
        help='Find all filenames matching a specified pattern recursively.',
    )
    parser.add_argument(
        'pattern',
        help='Filename pattern.'
    )
    parser.add_argument(
        '--dir',
        metavar='PATH',
        default=os.getcwd(),
        help='Directory to search in (default: current directory).'
    )

def main(args):
    for path in Path(args.dir).rglob(args.pattern):
        print(path.absolute())
