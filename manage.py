import os
import argparse
from string import Template


__version__ = '0.0.1'


# Loading Template Extension
with open(os.path.join('./', '.extension_template')) as fd:
    code = Template(fd.read())


# Command to create new Extension
def new_extension(Extension: str):
    extension_path = os.path.join('./','cogs',f'{Extension}'+ '.py')
    if os.path.exists(extension_path):
        print(f"Extension {Extension} already exist")
        return None
    else:
        with open(extension_path, 'w') as fd:
            fd.write(code.substitute(Extension=Extension))

def remove_extension(Extension: str):
    extension_path = os.path.join('./','cogs',f'{Extension}'+ '.py')
    if os.path.exists(extension_path):
        os.remove(extension_path)
        print(f"Extension {Extension} removed")
    else:
        print(f"Extension {Extension} does not exist!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= f"Bot manager version {__version__}.")
    parser.add_argument('--new',  nargs='?', default='None', type=str)
    parser.add_argument('--delete',  nargs='?', default='None', type=str)
    config = parser.parse_args()

    if config.new != 'None':
        new_extension(config.new)

    if config.delete != 'None':
        remove_extension(config.delete)
