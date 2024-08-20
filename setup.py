from setuptools import setup
from py_cz_api.config import app_name, app_version

setup(
    name=app_name,
    version=app_version,
    description='Библиотека для автоматизации работы с Честным Знаком через True API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jqxl/py_cz_api',
    download_url='https://codeload.github.com/jqxl/py_cz_api/zip/refs/heads/main',
    author='jqxl',
    author_email='jqxl+git@ya.ru',
    license='GNU General Public License v3.0',
    packages=['py_cz_api'],
    install_requires=[
        'aiohttp',
        'pandas',
        'PyJWT',
    ],
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.10',
)
