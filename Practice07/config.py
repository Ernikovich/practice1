from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser() # создаём объект парсера ini-файлов
    parser.read(filename) # читаем файл database.ini

    config = {}
    if parser.has_section(section):  # проверяем, есть ли секция [postgresql]
        params = parser.items(section) # получаем все пары ключ-значение
        for param in params:   # проходим по ним циклом
            config[param[0]] = param[1]# кладём в словарь config
    else:
        raise Exception(f'Section {section} not found in {filename}')
    return config
