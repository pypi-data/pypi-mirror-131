import re
from setuptools import setup, find_packages

mainfile = open('mamba/__init__.py', 'r', encoding='utf-8').read()
appversion = [v.strip() for v in re.search(r'__version__\s*=\s*\(\s*(\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+)\s*\)', mainfile).group(1).split(',')]

setup(
    name="mamba_toolbox",
    version=".".join(appversion),
    description="Mambalib toolbox",
    author="Danila Matyushev",
    author_email="gribnoysalatik@gmail.com",
    install_requires=['click==7.1.2', 'requests==2.25.1', 'virtualenv==20.2.2'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)