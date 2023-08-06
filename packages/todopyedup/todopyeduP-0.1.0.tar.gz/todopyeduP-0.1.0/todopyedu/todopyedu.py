"""
Добавление нужных библиотек:
"""
import subprocess

import os

import datetime
from shutil import copyfile
from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from todopyedu import (DB_READ_ERROR, ID_ERROR, EDITOR_ERROR, DIRECTORY_ERROR, PERMISSION_ERROR,
                 SUCCESS, LIST_EMPTY, INDEX_ERROR, INVALID_DATE)

from todopyedu import database, config

from todopyedu.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    """data class содержит именованный кортеж"""
    todo: Dict[str, Any]
    error: int


class Todoer:
    """ Класс предназначен для работы с to-do записями"""

    def __init__(self, db_path: Path) -> None:
        """
        конструктор использует класс databasehandler из файла database
        :param db_path:
        """
        self._db_handler = DatabaseHandler(db_path)

    @staticmethod
    def _head(todo_list: List[Dict[str, Any]], first_index: int = 0, second_index: int = 0
              ) -> (List[Dict[str, Any]], int):
        """Закрытый метод для получения индексов get_todo_list"""
        if first_index == 0 and second_index == 0:
            return todo_list, SUCCESS
        if first_index != 0 and second_index == 0:
            try:
                todo_list = [todo_list[i] for i in range(first_index)]
            except IndexError:
                return [], INDEX_ERROR
        elif first_index != 0 and second_index != 0:
            try:
                todo_list = [todo_list[i] for i in range(first_index - 1, second_index)]
            except IndexError:
                return [], INDEX_ERROR
        else:
            return [], INDEX_ERROR
        return todo_list, SUCCESS

    @staticmethod
    def _tail(todo_list: List[Dict[str, Any]], first_index: int = 0, second_index: int = 0
              ) -> (List[Dict[str, Any]], int):
        """
        Закрытый метод для получения индексов get_todo_list
        :param todo_list:
        :param first_index:
        :param second_index:
        :return:
        """
        if first_index == 0 and second_index == 0:
            todo_list = todo_list[::-1]
        elif first_index != 0 and second_index == 0:
            try:
                todo_list = [todo_list[i] for i in reversed(range(first_index))]
            except IndexError:
                return [], INDEX_ERROR
        elif (first_index != 0 and second_index != 0 and first_index < second_index
              or first_index == 0 and second_index != 0
              and first_index < second_index):
            try:
                todo_list = [todo_list[i]
                             for i in reversed(range(first_index - 1, second_index))]
            except IndexError:
                return [], INDEX_ERROR
        else:
            return [], INDEX_ERROR
        return todo_list, SUCCESS

    def get_todo_list(self,
                      first_index: int = 0,
                      second_index: int = 0,
                      head: bool = False,
                      tail: bool = False
                      ) -> (List[Dict[str, Any]], int):
        """
        Возвращает текущий лист с to-do записями в зависимости от использования индексов и флагов
        :param first_index
        :param second_index
        :param head
        :param tail
        :return List[Dict[str, Any]], int:
        """
        read = self._db_handler.read_todos()
        todo_list = read.todo_list
        if len(todo_list) == 0:
            return [], LIST_EMPTY
        if head:
            new_list, error = Todoer._head(todo_list, first_index, second_index)
            return new_list, error
        if tail:
            new_list, error = Todoer._tail(todo_list, first_index, second_index)
            return new_list, error
        return todo_list, SUCCESS

    def add(self,
            description: List[str],
            priority: int = 2,
            deadline: bool = False,
            year: str = '0',
            month: str = '0',
            day: str = '0',
            hour: str = '0',
            minutes: str = '0') -> CurrentTodo:
        """
        Добавление записи.Возможность изменять приоритет и дату когда нужно выполнить задачу
        :param self:
        :param description:
        :param priority:
        :param deadline:
        :param year:
        :param month:
        :param day:
        :param hour:
        :param minutes:
        :return: CurrentTodo
        """
        description_text = " ".join(description)
        date_today = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
        if deadline:
            try:
                date_deadline = str(datetime.datetime(
                    int(year), int(month), int(day), int(hour), int(minutes)))
            except ValueError:
                return CurrentTodo({}, INVALID_DATE)
            if date_deadline < date_today:
                return CurrentTodo({}, INVALID_DATE)
            todo = {
                "Description": description_text,
                "Priority": priority,
                "Done": False,
                "Date": date_today,
                "Deadline": date_deadline
            }
        else:
            todo = {
                "Description": description_text,
                "Priority": priority,
                "Done": False,
                "Date": date_today,
                "Deadline": "-"
            }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def set_done(self, todo_id: int, flag: bool) -> CurrentTodo:
        """
        Перевод записи в состояние выполненное
        (при использование флага можно вернуть в состояние невыполненное)
        :param todo_id:
        :return: CurrentTodo
        """
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        if flag:
            todo["Done"] = False
        else:
            todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int, second_todo_id: int = 0) -> CurrentTodo:
        """
        Удаление записи to-do,при использовании 2 индексов удаляется несколько записей
        :param self:
        :param todo_id:
        :param second_todo_id:
        :return:CurrentTodo
        """
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        if second_todo_id != 0:
            if second_todo_id < todo_id or second_todo_id > len(read.todo_list) or todo_id < 0:
                return CurrentTodo({}, ID_ERROR)
            todo = read.todo_list
            todo_dict = dict()
            for i in range(todo_id - 1, second_todo_id):
                todo_dict.setdefault("Description", []).append(todo[i]["Description"])
                todo[i]["Description"] = "-"
            todo = list(filter(
                lambda x: False if todo[todo.index(x)]["Description"] == "-" else True, todo))
            write = self._db_handler.write_todos(todo)
            return CurrentTodo(todo_dict, write.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
            write = self._db_handler.write_todos(read.todo_list)
            return CurrentTodo(todo, write.error)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)

    def remove_all(self) -> CurrentTodo:
        """
        Удаление всех записей
        :param self:
        :return:
        """
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)

    @staticmethod
    def editor(redactor: str) -> int:
        """
        Редактирование файла в котором содержатся записи
        :param redactor:
        :return:int
        """
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        try:
            subprocess.call([redactor, db_path])
            return SUCCESS
        except FileNotFoundError:
            return EDITOR_ERROR

    @staticmethod
    def _access(path: str) -> bool:
        """
        Закрытый  метод ,проверка прав доступа
        :param path:
        :return:bool
        """
        return os.access(path, os.W_OK) & os.access(path, os.R_OK)

    def save(self, save_path: str, flag: bool = False) -> int:
        """
        Сохранение файла в указанный путь,при использовании флага записи в database удаляются
        :param self:
        :param save_path:
        :param flag:
        :return:
        """
        if Todoer._access(save_path) is False:
            return PERMISSION_ERROR
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        try:
            copyfile(db_path, save_path)
            if flag:
                self.remove_all()
        except IsADirectoryError:
            return DIRECTORY_ERROR
        return SUCCESS
