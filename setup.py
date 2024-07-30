from setuptools import setup, find_packages
from config import app_name, app_version

setup(
    name=app_name,
    version=app_version,
    description='Библиотека для автоматизации работы с Честным Знаком через True API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jqxl/py_cz_api',
    author='jqxl',
    author_email='jqxl+git@ya.ru',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'pywin32',
        'PyJWT',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
