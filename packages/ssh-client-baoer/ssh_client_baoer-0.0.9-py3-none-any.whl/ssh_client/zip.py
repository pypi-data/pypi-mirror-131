import zipfile
import tarfile
import os


def zip_extract_to(zip_file, target_dir):
    with zipfile.ZipFile(zip_file) as z:
        z.extractall(target_dir)


def zip_extract(zip_file):
    target_dir = os.path.splitext(zip_file)[0]
    if os.path.isdir(target_dir):
        os.rmdir(target_dir)
    zip_extract_to(zip_file, target_dir)


def tar_extract_to(tar_file, target_dir):
    with tarfile.TarFile(tar_file) as t:
        t.extractall(target_dir)


def tar_extract(tar_file):
    target_dir = os.path.splitext(tar_file)[0]
    if os.path.isdir(target_dir):
        os.rmdir(target_dir)
    tar_extract_to(tar_file, target_dir)
