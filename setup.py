from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='tdb',
    author='MarkNo1',
    url='https://github.com/MarkNo1-github/TournamentDiscordBot',
    version='0.0.1',
    license=license,
    description='Manage Tournament in Discord',
    long_description=readme,
    packages=find_packages(exclude=['tests*']),
    entry_points ={'console_scripts': ['tdb = tdb.manager:main']},
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.6'
)
