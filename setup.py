from setuptools import setup, find_namespace_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


# setup(
#     name='tdbm',
#     author='MarkNo1',
#     url='https://github.com/MarkNo1-github/TournamentDiscordBot',
#     version='0.0.4',
#     license=license,
#     description='Manage Tournament in Discord',
#     long_description=readme,
#     packages=find_namespace_packages(include=['tdbm.*']),
#     entry_points ={'console_scripts': ['tdbm = tdbm.manager:main']},
#     install_requires=requirements,
#     include_package_data=True,
#     python_requires='>=3.6'
# )

setup(
    name='tdbm.logger',
    author='MarkNo1',
    url='https://github.com/MarkNo1-github/TournamentDiscordBot',
    version='0.0.5',
    license=license,
    description='Tdbm Logger',
    long_description=readme,
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.6'
)

setup(
    name='tdbm.data',
    author='MarkNo1',
    url='https://github.com/MarkNo1-github/TournamentDiscordBot',
    version='0.0.5',
    license=license,
    description='Tdbm Data',
    long_description=readme,
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.6'
)

setup(
    name='tdbm.bot',
    author='MarkNo1',
    url='https://github.com/MarkNo1-github/TournamentDiscordBot',
    version='0.0.5',
    license=license,
    description='Tdbm Bot',
    long_description=readme,
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.6'
)
