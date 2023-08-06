from flask import Flask as __Flask, Response as __Response
from config import Configuration
from importlib.util import module_from_spec as __module_from_spec, spec_from_file_location as __spec_from_file_location
from os import listdir
from os.path import join as __path_join
from multiprocessing import Process

__name_module__ = 'py-web-server-flask-Orinnass'
__version__ = '1.2.2'
__web_server__ = __Flask(__name__)

__config = Configuration()
__host_address = __config.web_server['address']
__port = __config.web_server['port']
__enabled = __config.web_server['enabled']
__api_directory = __config.web_server.get('api_directory')
__start_in_other_process = __config.web_server["start_in_other_process"]
__logger = __config.logging.get_logger(__name__)
del __config


def __read_api_directory__():
    __logger.debug('Вызван метод чтения стороннего api')
    if __api_directory:
        __logger.info('Чтение стороннего api')
        __logger.debug(f"{__api_directory=}")
        list_dir = listdir(__api_directory)
        __logger.debug(f"{list_dir=}")
        list_dir = [i for i in list_dir if len(i.split('.')) == 2 and i.split('.')[1] == 'py']
        __logger.debug(f"{list_dir=}")
        for i in list_dir:
            try:
                __logger.debug(f"{i=}")
                spec = __spec_from_file_location(i.split('.')[0], __path_join(__api_directory, i))
                __logger.debug(f"{spec=}")
                module = __module_from_spec(spec)
                __logger.debug(f"{module=}")
                spec.loader.exec_module(module)
                __logger.debug(f"{module=}")
                api = module.__getattribute__('api')
                __logger.debug(f"{api=}")
                __logger.info(f'Регистрация api {api.name}')
                __web_server__.register_blueprint(api)
            except Exception as e:
                __logger.error(str(e), exc_info=True, stack_info=True)
    else:
        __logger.info("Не указана директория со сторонним api")


def __start_web_server():
    __logger.debug('Вызван запуск веб сервера')
    if __enabled:
        __read_api_directory__()

        __logger.info("Запуск сервера")
        __web_server__.run(host=__host_address, port=__port)
    else:
        __logger.info("Веб сервер отключен в конфиге")


@__web_server__.route('/')
def __root_rout():
    return __Response(f"{__name_module__} {__version__}", mimetype='application/text')


@__web_server__.route('/server/get_version')
def __get_version():
    return __Response(__version__, mimetype='application/text')


def start_server():
    if __start_in_other_process:
        web_process = Process(target=__start_web_server, daemon=True)
        web_process.start()
        return web_process
    __start_web_server()
