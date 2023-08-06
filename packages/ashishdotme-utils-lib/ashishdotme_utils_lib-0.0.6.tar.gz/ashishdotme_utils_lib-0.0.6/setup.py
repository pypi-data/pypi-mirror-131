from pathlib import Path

from setuptools import setup

setup(
    name='ashishdotme_utils_lib',
    description='Python library for dashboard',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Ashish Patel',
    author_email='ashishsushilpatel@gmail.com',
    url='https://github.com/ashishdotme/ashishdotme-utils',
    version='0.0.6',
    packages=[
        'ashishdotme_utils_lib',
        'ashishdotme_utils_lib/core',
        'ashishdotme_utils_lib/errors',
        'ashishdotme_utils_lib/sdk'
    ],
    install_requires=['colorama', 'colorlog', 'requests']
)
