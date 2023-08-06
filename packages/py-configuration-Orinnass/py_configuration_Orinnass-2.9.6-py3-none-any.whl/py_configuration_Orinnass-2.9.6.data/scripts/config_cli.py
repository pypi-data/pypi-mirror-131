"""
Модуль для работы с конфигурацией из командной строки
"""
from sys import argv
from os import walk
from os.path import exists as path_exists, join as path_join
from json import dumps as json_dump, loads as json_load
import re
import argparse
from config import __version__

global_template: dict | None = None

# TODO: добавить типы переменных


def __dump_json__(file_path, json):
    with open(file_path, 'w') as file:
        file.write(json_dump(json, indent=3))


def __convert_str_to_list(value):
    value = value.strip("][").split(',')
    new_value = []
    for i in value:
        new_value.append(__parse_type_and_value__(i.strip(), start_block='<<', end_block='>>'))
    return new_value


def __parse_type_and_value__(parse_value: str, start_block: str = '<', end_block: str = '>') -> int | str | bool:
    types = {"int": int, "list": __convert_str_to_list, "str": str, "None": str, None: str, "bool": bool}
    parse = re.search(fr"(.*){start_block}(\w+){end_block}", parse_value)
    if parse:
        value = parse.group(1)
        type_value = parse.group(2)
    else:
        value = parse_value
        type_value = None
    return types[type_value](value)


def __wait_confirmation__(message: str) -> bool:
    print(f"{message} (y/n)")
    answer = input()
    if answer.lower() != "yes" and answer.lower() != 'y':
        return False
    return True


def __walk_on_json_path__(path: str, element: dict, root_element: dict) -> dict:
    path = path.split("/")
    link_element = element
    for i in path:
        match i:
            case "#":
                link_element = root_element
            case _:
                link_element = link_element[i]
    return link_element


def __parse_template__(element):
    global global_template
    if element.get("$ref"):
        element = __walk_on_json_path__(element["$ref"], element, global_template)
    if element["type"] == "object":
        config = {}
        for i in element["required"]:
            config[i] = __parse_template__(element["properties"][i])
        return config
    else:
        return element.get("default", "null")


def create_command(params):
    """
    Функция создания конфига из шаблона
    """
    with open(params.template_config) as template_file:
        template = json_load(template_file.read())

    if not params.force and path_exists(params.config_file) and \
            not __wait_confirmation__('Файл конфигурации уже существует, перезаписать его?'):
        return

    global global_template
    global_template = template
    config = __parse_template__(template)

    if params.extra_vars:
        for i in params.extra_vars:
            path, value = i.split("=")
            path = path.split('/')
            value = __parse_type_and_value__(value)
            element = __walk_on_json_path__("/".join(path[:-1]), config, config)
            element[path[-1]] = value

    __dump_json__(params.config_file, config)
    print('Конфигурация создана')


def merge_template(params):
    """
    Функция слияние файлов шаблона
    """
    with open(params.merge_file) as merge_file:
        merge = json_load(merge_file.read())
    with open(params.template_file) as template_file:
        template = json_load(template_file.read())

    blocks = ["properties", "definitions"]
    for block in blocks:
        if merge.get(block):
            merge_properties = merge[block]
            for i in merge_properties.keys():
                if i in template[block] and not __wait_confirmation__(f"{i} уже есть в шаблоне в блоке {block} "
                                                                      f"перезаписать?"):
                    continue
                template[block][i] = merge_properties[i]
    if merge.get("required"):
        for i in merge["required"]:
            if i not in template["required"]:
                template["required"].append(i)

    __dump_json__(params.template_file, template)

    print("Конфигурация объединена")


def merge_all_templates(params):
    """
    Функция поиска всех файлов для шаблона и слияние с шаблоном
    """
    for i in walk(params.dir_find):
        for file in i[2]:
            if file == "merge_template.json":
                merge_file = path_join(i[0], file)
                if params.force or __wait_confirmation__(f"Найден файл для слияние: {merge_file}. Выполняем слияние?"):
                    print(f"Слияние файла: {merge_file}")
                    params.merge_file = merge_file
                    merge_template(params)

    print("Поиск и слияние завершено")


def create_template(params):
    """
    Функция создания базового шаблона
    """
    __dump_json__(params.template_file, {"definitions": {}, "type": "object", "properties": {},
                                         "required": [], "additionalProperties": False})
    print("Конфигурация создана")


methods = {
    "create": create_command,
    "merge-template": merge_template,
    "merge-all-templates": merge_all_templates,
    "create-template": create_template
}


def create_parse():
    """
    Команда создания парсинга аргументов
    """
    parser = argparse.ArgumentParser(add_help=False)

    parent_group = parser.add_argument_group(title="Параметры")
    parent_group.add_argument('--version', action='version', help='Вывести номер версии',
                              version='%(prog)s {}'.format(__version__))
    parent_group.add_argument("--help", "-h", action="help", help="Справка")

    subparsers = parser.add_subparsers(dest="command", title="Возможные команды",
                                       description="Команды, которые должны быть в качестве первого параметра %(prog)s")

    # region create command
    create_command_parser = subparsers.add_parser("create", add_help=False)
    create_command_parser.add_argument('config_file')
    create_command_parser.add_argument("template_config")
    create_command_parser.add_argument("-f", "--force", action="store_true", default=False)
    create_command_parser.add_argument("-e", "--extra-vars", nargs='+')
    # endregion

    # region merge template
    attach_template_parser = subparsers.add_parser('merge-template', add_help=False)
    attach_template_parser.add_argument("merge_file")
    attach_template_parser.add_argument("template_file")
    # endregion

    # region merge all templates
    merge_all_template = subparsers.add_parser("merge-all-templates", add_help=False)
    merge_all_template.add_argument("dir_find")
    merge_all_template.add_argument("template_file")
    merge_all_template.add_argument("-f", "--force", action="store_true", default=False)
    # endregion

    # region create base template
    create_template_parser = subparsers.add_parser("create-template", add_help=False)
    create_template_parser.add_argument("template_file")
    # endregion

    return parser


if __name__ == '__main__':
    main_parser = create_parse()
    parsed_params = main_parser.parse_args(argv[1:])

    methods[parsed_params.command](parsed_params)
