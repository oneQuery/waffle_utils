import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, List, Union

import natsort
import yaml


# save
def save_json(obj: Any, fp: Union[str, Path], create_directory: bool = False):
    """save json file

    Args:
        obj (Any): Any object that can be converted to json format.
        fp (Union[str, Path]): file path.
        create_directory (bool, optional): this determines whether create parent directory or not. Default to False.
    """

    fp = Path(fp)
    if create_directory:
        make_directory(fp.parent)

    with open(fp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def save_yaml(obj: Any, fp: Union[str, Path], create_directory: bool = False):
    """save yaml file

    Args:
        obj (Any): Any object that can be converted to yaml format.
        fp (Union[str, Path]): file path.
        create_directory (bool, optional): this determines whether create parent directory or not. Default to False.
    """

    fp = Path(fp)
    if create_directory:
        make_directory(fp.parent)

    with open(fp, "w") as f:
        yaml.safe_dump(obj, f, indent=4, sort_keys=False)


# load
def load_json(fp: Union[str, Path]) -> dict:
    """load json file

    Args:
        fp (Union[str, Path]): file path.

    Returns:
        dict: dictionary
    """

    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        d = json.load(f)

    return d


def load_yaml(fp: Union[str, Path]) -> dict:
    """load yaml file

    Args:
        fp (Union[str, Path]): file path.

    Returns:
        dict: dictionary
    """

    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        d = yaml.safe_load(f)

    return d


def load_txt(fp: Union[str, Path]) -> str:
    """load txt file

    Args:
        fp (Union[str, Path]): file path.

    Returns:
        str: text
    """

    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        s = f.read()

    return s


# get
def get_files_list(src: Union[str, Path], ext: str = None) -> list:
    """list files in directory

    Args:
        src (Union[str, Path]): directory path.
        ext (str, optional): extension. Defaults to None.

    Returns:
        list: file list
    """

    src = Path(src)
    if not src.is_dir():
        raise ValueError(f"{src} is not directory")

    if ext is None:
        # sort by file name
        return natsort.natsorted(list(src.glob("**/*")))
    else:
        return list(src.glob(f"**/*.{ext}"))


def get_extension(fp: Union[str, Path]) -> Union[str, List[str]]:
    """get extension

    if directory, return all file extensions. if file, return file extension

    Args:
        fp (Union[str, Path]): file path or directory.

    Returns:
        Union[str, List[str]]: extension
    """

    fp = Path(fp)

    # get extension
    if fp.is_dir():
        # return file extensions without dot.
        exts = {p.suffix[1:] for p in fp.glob("**/*") if p.is_file()}
        # if a single extension, return a string.
        if len(exts) == 1:
            return exts.pop()
        else:
            return list(exts)
    elif fp.is_file():
        # return file extension without dot
        return fp.suffix[1:]
    else:
        # Add an else clause with a return statement to handle cases where the path is neither a file nor a directory
        raise ValueError(f"{fp} is neither a file nor a directory")


# copy
def copy_files_to_directory(
    src: Union[list, str, Path],
    dst: Union[str, Path],
    create_directory: bool = False,
):
    """Copy files to directory

    Args:
        src (Union[list, str, Path]): 'file list' or 'file' or 'directory'.
        dst (Union[str, Path]): destination directory.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
        FileNotFoundError: if src is unknown
        ValueError: if dst is not directory format
        FileNotFoundError: if dst is not exists. you can bypass this error with create_directory argument.
    """

    src_list = None
    if isinstance(src, list):
        src_prefix = os.path.commonpath(src)
        src_list = list(map(Path, src))
    elif isinstance(src, str) or isinstance(src, Path):
        src = Path(src)
        if src.is_file():
            src = Path(src)
            src_list = [src]
            src_prefix = src.parent
        elif src.is_dir():
            src = Path(src)
            src_list = src.glob("**/*")
            src_prefix = src

    if src_list is None:
        raise FileNotFoundError(f"unknown source {src}")

    dst = Path(dst)
    if dst.suffix != "":
        raise ValueError(
            f"dst should be directory format. but got {dst.suffix}"
        )
    elif create_directory:
        make_directory(dst)

    if not dst.exists():
        raise FileNotFoundError(
            f"{dst} directory does not exist. please set 'create_directory' argument to be True to make directory."
        )

    for src_file in src_list:
        dst_file = Path(str(src_file).replace(str(src_prefix), str(dst)))
        make_directory(dst_file.parent)
        if src_file.is_file():
            shutil.copy(src_file, dst_file)


def copy_file(
    src: Union[str, Path],
    dst: Union[str, Path],
    create_directory: bool = False,
):
    """Copy file

    Args:
        src (Union[str, Path]): source file path.
        dst (Union[str, Path]): destination file path.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
    """
    dst = Path(dst)

    if create_directory:
        make_directory(dst.parent)

    shutil.copy(src, dst)


# make
def make_directory(src: Union[str, Path]):
    """Create Directory

    Args:
        src (str): directory
    """
    Path(src).mkdir(mode=0o766, parents=True, exist_ok=True)


# remove
def remove_file(src: str):
    """Remove File

    Args:
        src (str): file to remove
    """
    os.remove(src)


def remove_directory(src: Union[str, Path]):
    """Remove Directory

    Args:
        src (str): file to remove
    """
    shutil.rmtree(str(src))


# unzip
def unzip(
    src: Union[str, Path],
    dst: Union[str, Path],
    create_directory: bool = False,
):

    if create_directory:
        make_directory(dst)

    with zipfile.ZipFile(src, "r") as f:
        f.extractall(dst)
