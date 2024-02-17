import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d != 'fastapienv']  # Exclude 'venv' directory
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

# Specify the path to your project directory here
startpath = "C:\\Users\\FarhanMehar\\Documents\\fastapi"
list_files(startpath)
