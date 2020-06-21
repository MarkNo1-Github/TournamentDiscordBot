from setuptools import setup, find_namespace_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    INSTALL_REQUIRES = True

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

def make_setup(module,include_package_data=False):

    setup(
        name=f'tdbm.{module}',
        author='MarkNo1',
        url='https://github.com/MarkNo1-github/TournamentDiscordBot',
        version='0.0.5',
        license=license,
        description=f'Tdbm {str(module).upper()}',
        long_description=readme,
        package_dir={'': 'lib'},
        packages=find_namespace_packages(where='lib'),
        install_requires=requirements,
        include_package_data=include_package_data,
        python_requires='>=3.6'
    )


make_setup('logger')
make_setup('bot')
make_setup('data')
