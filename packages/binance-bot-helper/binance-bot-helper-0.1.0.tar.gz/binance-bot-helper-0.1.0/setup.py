from setuptools import find_packages, setup
setup(
    name='binance-bot-helper',
    packages=find_packages(include=['binance_bot_helper']),
    version='0.1.0',
    description='Binance bot helper functions',
    author='Mariano Billinghurst',
    license='MIT',
    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest','python-binance'],
    test_suite='tests',
)