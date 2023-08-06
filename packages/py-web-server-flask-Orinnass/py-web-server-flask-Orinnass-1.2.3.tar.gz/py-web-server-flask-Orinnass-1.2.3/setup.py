"""
Пакет установки модуля
"""
from os import environ
from os.path import dirname, abspath, join as join_path
from sys import argv

path_to_module = abspath(dirname(argv[0]))
environ['TEMPLATE_CONFIG'] = f"{join_path(path_to_module, 'tests', 'template_config.json')}"
environ["CONFIG_FILE"] = f"{join_path(path_to_module, 'tests', 'config_with_api_dir.cfg')}"

from setuptools import setup
from setuptools import find_packages
from web_server import __version__, __name_module__


def get_install_requires():
    """
    Метод получения зависимых модулей
    """
    with open('requirements.txt', 'r') as file_req:
        lines_req = file_req.readlines()
        for index, i in enumerate(lines_req):
            if '-e' in i:
                module_name = i.split('#egg=')[1].strip()
                install_command = i.split('-e ')[1].strip()
                lines_req[index] = f'{module_name} @ {install_command}\n'
            else:
                lines_req[index] = lines_req[index].replace('==', '>=')
        return lines_req


setup(
    name=__name_module__,
    version=__version__,
    download_url="https://gitlab.com/Orinnass/python-web-server-flask",
    packages=find_packages(include=('web_server',), exclude=('tests',)),
    package_data={'web_server': ['merge_template.json']},
    install_requires=get_install_requires(),
    python_requires=">=3.10"
)
