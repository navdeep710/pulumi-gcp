import os

import pulumi


def traverse_dir_recur(root,assets):
    for root, dirs, files in os.walk(root):
        for filename in files:
            location = os.path.join(root, filename)
            print(location)
            asset = pulumi.FileAsset(path=location)
            assets[filename] = asset
        for dirname in dirs:
            asset = pulumi.FileArchive(os.path.join(root, dirname))
            asset[dirname] = asset

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))