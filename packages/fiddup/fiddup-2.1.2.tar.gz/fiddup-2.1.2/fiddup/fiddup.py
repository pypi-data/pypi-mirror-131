import glob
import click
from colorama import Fore, Style
from difflib import SequenceMatcher
from pathlib import Path
from alive_progress import alive_bar
from fiddup.views import (
    prepare_name_table_header,
    prepare_hash_table_header,
    show_table_data,
)
from fiddup.result import FiddupNameResult, FiddupHashResult
from hashlib import sha1


def get_sha_hash(filepath):
    file_hash = sha1()
    with open(filepath, "rb") as _f:
        while True:
            in_bytes = _f.read(65536)
            if not in_bytes:
                break
            file_hash.update(in_bytes)
    return file_hash.hexdigest()


def run_hashmode(verbose, extensions, inpath):
    _file_list = []
    _result_list = []
    _file_count = 0
    table_data = prepare_hash_table_header()

    for ext in extensions:
        # Scan the inpath for the specified extensions
        for file in glob.glob(f"{inpath}\\*.{ext}"):
            ppath = Path(file)
            _file_list.append(str(ppath))
            _file_count += 1
    if verbose:
        click.secho(f"[{Fore.CYAN}Info{Style.RESET_ALL}] Found {_file_count} files.")

    with alive_bar(_file_count) as bar:
        for file in _file_list:
            for cmpfile in _file_list:
                if file != cmpfile:
                    # Get file hash for "file":
                    file_hash = get_sha_hash(file)
                    cmpfile_hash = get_sha_hash(cmpfile)
                    if file_hash == cmpfile_hash:
                        _fu = FiddupHashResult(
                            base_file=file, compared_file=cmpfile, file_hash=file_hash
                        )
                        if _fu not in _result_list:
                            table_data.append(_fu.as_terminaltable_row())
                            _result_list.append(_fu)
            bar()

    show_table_data(table_data)


def run_assistant(verbose, extensions, directory, inpath, threshold):
    _file_list = []
    _result_list = []
    _dir_count = 0
    _file_count = 0
    table_data = prepare_name_table_header()

    if directory:
        # Scan the inpath for entries
        for path in glob.glob(f"{inpath}\\*"):
            ppath = Path(path)
            if ppath.is_dir():
                # Need only last part because it is filename
                _file_list.append(str(*ppath.parts[-1:]))
                _dir_count += 1
        if verbose:
            click.secho(
                f"[{Fore.CYAN}Info{Style.RESET_ALL}] Found {_dir_count} directories."
            )

    for ext in extensions:
        # Scan the inpath for the specified extensions
        for file in glob.glob(f"{inpath}\\*.{ext}"):
            ppath = Path(file)
            # Only filename
            _file_list.append(str(*ppath.parts[-1:]))
            _file_count += 1
    if verbose:
        click.secho(f"[{Fore.CYAN}Info{Style.RESET_ALL}] Found {_file_count} files.")

    with alive_bar(_dir_count + _file_count) as bar:
        for file in _file_list:
            for cmpfile in _file_list:
                if file != cmpfile:
                    _fu = FiddupNameResult(
                        base_file=file,
                        compared_file=cmpfile,
                        similarity=SequenceMatcher(None, file, cmpfile).ratio(),
                    )
                    if _fu.similarity >= threshold:
                        if _fu not in _result_list:
                            table_data.append(_fu.as_terminaltable_row())
                            _result_list.append(_fu)
            bar()

    show_table_data(table_data)
