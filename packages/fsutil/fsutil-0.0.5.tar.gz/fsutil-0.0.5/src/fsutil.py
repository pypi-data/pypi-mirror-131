import os
import shutil
import tarfile
from pathlib import Path


def remove_all_except(path, *excluded_fsobject_names):
    for fs_object_name in os.listdir(path):
        if fs_object_name not in excluded_fsobject_names:
            remove_fsobject(path, fs_object_name)


def remove_fsobject(path, fsobject_name):
    fsobject_path = os.path.join(path, fsobject_name)
    if os.path.isfile(fsobject_path) or os.path.islink(fsobject_path):
        os.unlink(fsobject_path)
    elif os.path.isdir(fsobject_path):
        shutil.rmtree(fsobject_path)


def rename(path, new_name):
    path_parent = Path(path).parent
    new_path = os.path.join(path_parent, 'ProjectData~')
    os.rename(path, new_path)
    return new_path


def make_parent(path, parent_name):
    path = Path(path)
    package_path = os.path.join(path.parent, parent_name)
    new_path = os.path.join(path.parent, parent_name)
    os.mkdir(new_path)
    shutil.move(path, new_path)
    return new_path


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
