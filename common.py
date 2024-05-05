from os import path, listdir


ASSETS_FOLDER = path.join(path.curdir, 'assets')
OUTPUT_FOLDER = path.join(path.curdir, 'output')
DATABASE_FOLDER = path.join(path.curdir, 'database')

IMGS = [path.join(ASSETS_FOLDER, item) for item in listdir(ASSETS_FOLDER)]