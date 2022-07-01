import copy
import re
import logging
import pybtex, pybtex.database.input.bibtex


def read_bibtex(bibfilename):
    """
    Reads bibtex data from a file into pybtex data structures.
    """

    bibbytes = open(bibfilename, "rb").read()
    bibstring = None
    for encoding in ["ascii", "utf8", "cp1252"]:
        try:
            bibstring = bibbytes.decode(encoding)
        except UnicodeDecodeError:
            continue
        logging.debug(f"{bibfilename}: using {encoding} encoding")
        break
    else:
        logging.warning("couldn't figure out encoding; using ascii with escapes")
        bibstring = bibbytes.decode("ascii", "backslashreplace")

    if bibstring.startswith("\uFEFF"):
        bibstring = bibstring[1:]  # Unicode BOM

    # for parser in [lambda s: pybtex.database.parse_string(s, 'bibtex'),
    #                fake_parse]:
    try:
        bibdata = pybtex.database.parse_string(bibstring, "bibtex")
    except Exception as e:
        import sys

        print(f"Failed to parse {bibfilename}", file=sys.stderr)
        print(e)
        sys.exit(1)
    return bibdata
