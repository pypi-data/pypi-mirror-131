from setuptools import setup

setup(
    name='ethernetscan',
    version='0.0.1',
    packages=['ethernetscan'],
    url='https://github.com/ipconfiger/etherscan',
    license='GNU General Public License v3.0',
    author='Alexander.Li',
    author_email='superpowerlee@gmail.com',
    description='Scan Ethernet',
    install_requires=[
        'ping3>=3.0.2'
    ],
    entry_points={
        'console_scripts': ['escan=ethernetscan.main:main'],
    },
)
