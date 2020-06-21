from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()



def get_package_name():
    return 'tdbm'

def produce_module_dot(name):
    return f'{get_package_name()}.{name}'

def produce_module_slash(name):
    return f'{get_package_name()}/{name}'

def produce_import_module(name):
    return {produce_module_dot(name):
                produce_module_slash(name)}

def produce_packages_dirs():
    packages_dirs = {get_package_name() : get_package_name()}
    packages_dirs.update(produce_import_module('bot'))
    packages_dirs.update(produce_import_module('data'))
    packages_dirs.update(produce_import_module('logger'))
    packages_dirs.update(produce_import_module('manager'))
    return packages_dirs

def produce_packages():
    return [get_package_name(),
            produce_module_dot('manager'),
            produce_module_dot('logger'),
            produce_module_dot('data'),
            produce_module_dot('bot')]


setup(
    name='tdbm',
    author='MarkNo1',
    url='https://github.com/MarkNo1-github/TournamentDiscordBot',
    version='0.0.4',
    license=license,
    description='Manage Tournament in Discord',
    long_description=readme,
    package_dir=produce_packages_dirs(),
    packages=produce_packages(),
    entry_points ={'console_scripts': ['tdbm = tdbm.manager:main']},
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.6'
)
#
# setup(name="tdbm.logger",
#       version="0.0.1",
#       package_dir={'': 'src'},
#       packages= ['tdbm/logger'])
# setup(name="tdbm.data",
#       version="0.0.1",
#       package_dir={'': 'src'},
#       packages= ['tdbm/data'])
# setup(name="tdbm.bot",
#       version="0.0.1",
#       package_dir={'': 'src'},
#       packages=['tdbm/bot'])
#

#
#
# setup(
#     name='tdbm.logger',
#     author='MarkNo1',
#     url='https://github.com/MarkNo1-github/TournamentDiscordBot',
#     version='0.0.5',
#     license=license,
#     description='Tdbm Logger',
#     long_description=readme,
#     package_dir={'': 'src'},
#     packages=find_namespace_packages(where='src'),
#     install_requires=requirements,
#     include_package_data=True,
#     python_requires='>=3.6'
# )
#
# setup(
#     name='tdbm.data',
#     author='MarkNo1',
#     url='https://github.com/MarkNo1-github/TournamentDiscordBot',
#     version='0.0.5',
#     license=license,
#     description='Tdbm Data',
#     long_description=readme,
#     package_dir={'': 'src'},
#     packages=find_namespace_packages(where='src'),
#     install_requires=requirements,
#     include_package_data=True,
#     python_requires='>=3.6'
# )
#
# setup(
#     name='tdbm.bot',
#     author='MarkNo1',
#     url='https://github.com/MarkNo1-github/TournamentDiscordBot',
#     version='0.0.5',
#     license=license,
#     description='Tdbm Bot',
#     long_description=readme,
#     package_dir={'': 'src'},
#     packages=find_namespace_packages(where='src'),
#     install_requires=requirements,
#     include_package_data=True,
#     python_requires='>=3.6'
# )
