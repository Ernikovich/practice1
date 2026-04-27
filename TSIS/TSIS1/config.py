from configparser import ConfigParser
# Это встроенный модуль Python для работы с .ini файлами.


def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()  #создаётся объект
    parser.read(filename)  # он читает файл database.ini

    config = {} # сюда будут записаны параметры подключения
    if parser.has_section(section):  
        params = parser.items(section) 
        for param in params:   
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}')
    return config


# param = ('host', 'localhost')
# param[0] → 'host'       # ключ
# param[1] → 'localhost'  # значение