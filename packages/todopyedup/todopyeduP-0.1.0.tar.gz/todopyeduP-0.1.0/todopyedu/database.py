"""This module provides the RP To-Do database functionality."""

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todopyedu import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, JSON_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)

DEFAULT_TEXT_EDITOR = 'nano'
DEFAULT_EDITORS = ['nano', 'vim', 'vi', 'gedit','mcedit']


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def get_text_editor(config_file: Path) -> Path:
    """Return text editor from config file"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return config_parser["Editor"]["redactor"]


def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    "data class содержит именнованый кортеж"
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    "класс для работы с записями чтение запись"

    def __init__(self, db_path: Path) -> None:
        "конструктор принимающий путь до файла с записями"
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        """
        функция считывающая из файла с записями
        :return-> DBResponse:
        """
        try:
            with self._db_path.open('r') as database:
                try:
                    return DBResponse(json.load(database), SUCCESS)
                except json.JSONDecodeError:  # Здесь ловим невырый json формат
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        """
        Записывает в файл то что хотим добавить
        :param todo_list:
        :return->DBResponse:
        """
        try:
            with self._db_path.open("w", ) as database:
                json.dump(todo_list, database, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)
