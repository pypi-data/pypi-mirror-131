"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import List, Optional
from prettytable import PrettyTable

import typer

import datetime

import time
from todopyedu.config import CONFIG_FILE_PATH
from todopyedu import (
    __app_name__, __version__, ERRORS, config, database, todopyedu
)

app = typer.Typer(help="Todo Journal Command Line Interface\n created with the library Typer")


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="to-do databse location?",
            help='Immediately indicates the desired path.All files are created in $HOME',
            is_eager=True
        ),
        text_editor: str = typer.Option(
            database.DEFAULT_TEXT_EDITOR,
            "--editor",
            "-ed",
            prompt="Choose your default editor:",
            help='Directly specifies the default editor'
        )
) -> None:
    """
    Initialize to-do database
    """
    typer.secho(f"The path to the configuraton file:{CONFIG_FILE_PATH}",
                fg=typer.colors.BLUE)
    if db_path != database.DEFAULT_DB_FILE_PATH:
        db_path = str(Path.home().joinpath(db_path))
    app_init_error = config.init_app(db_path, text_editor)
    if app_init_error:
        typer.secho(
            f"Creating config file failed with '{ERRORS[app_init_error]}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f"Creating database failed with '{ERRORS[db_init_error]}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"The to-do database is {db_path}", fg=typer.colors.BLUE
        )
        typer.secho(
            f"Defautlt text editor is {text_editor}", fg=typer.colors.BLUE)


def get_todo() -> todopyedu.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please run "todopyedu init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit()
    if db_path.exists():
        return todopyedu.Todoer(db_path)
    else:
        typer.secho(
            'Database not found.Please run "src init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit()


@app.command()
def add(description: List[str] = typer.Argument(...),
        priority: int = typer.Option(2, "--priority", "-p", min=1, max=3, help="set priority"),
        date: bool = typer.Option(None, "--date", "-d", help="add data for deadline (Y,M,D,H,M)")
        ) -> None:
    """
    Adding todos description and priority and date
    """
    todoer = get_todo()
    if date:
        year = typer.prompt("Enter year")
        month = typer.prompt("Enter month")
        day = typer.prompt("Enter day")
        hour = typer.prompt("Enter hour")
        minutes = typer.prompt("Enter minutes")
        todo, error = todoer.add(description, priority, date, year, month, day, hour, minutes)
    else:
        todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        if date:
            typer.secho(
                f"""to-do: "{todo['Description']}" was added """
                f"""with priority: {priority}"""
                f""" with deadline: {year}-{month}-{day}  {hour}:{minutes}""",
                fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                f"""to-do: "{todo['Description']}" was added """
                f"""with priority: {priority}""",
                fg=typer.colors.GREEN
            )


@app.command(name="list")
def list_all(
        head: bool = typer.Option(
            False,
            "--head",
            "-h",
            help="Direct output if specified indices are output up to this value",
            show_default=False,
            is_eager=True
        ),
        tail: bool = typer.Option(
            False,
            "--tail",
            "-t",
            help="Reverse output if indices are specified are output before this value",
            show_default=False
        ),
        first_index: int = typer.Argument(
            0,
            help='Needed for direct withdrawal,',
            show_default=False
        ),
        second_index: int = typer.Argument(
            0,
            help='if there are two indices, some of the records are taken',
            show_default=False
        )
) -> None:
    """List all to-do's"""
    todoer = get_todo()
    todo_list, error = todoer.get_todo_list(first_index, second_index, head, tail)
    if error:
        typer.secho(
            f"The list could not be displayed:'{ERRORS[error]}'",
            fg=typer.colors.RED)
        raise typer.Exit(1)
    table = PrettyTable()
    table.field_names = ["ID", "Priority", "Done", "Description", "Date", "Deadline"]
    for id, todo in enumerate(todo_list, start=1):
        desc, priority, done, date, deadline = todo.values()
        table.add_rows([[id, priority, done, desc, date, deadline]])
    typer.secho(table, fg=typer.colors.BLUE)


@app.command(name="complete")
def set_done(
        todo_id: int = typer.Argument(...),
        flag: bool = typer.Option(
            None,
            "-f",
            "--false",
            help='Task True -> False'
        )
) -> None:
    """Complete a to-do by setting it as done using its TODO_ID."""
    todoer = get_todo()
    todo, error = todoer.set_done(todo_id, flag)
    if error:
        typer.secho(
            f'Completing to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        if flag:
            typer.secho(
                f""" to-do # { todo_id} "{todo['Description']}" completed->not completed"""
            )
        else:
            typer.secho(
                f"""to-do # {todo_id} "{todo['Description']}" completed!""",
                fg=typer.colors.GREEN,
            )


@app.command()
def remove(
        todo_id: int = typer.Argument(...),
        second_todo_id: int = typer.Argument(0, help='for to delete multiple entries at once'),
        force: bool = typer.Option(
            False,
            "--force",
            "-f",
            help="Force deletion without confirmation",
        ),

) -> None:
    """Remove a to-do using its TODO_ID"""
    todoer = get_todo()
    todo, error = todoer.remove(todo_id, second_todo_id)
    if error:
        typer.secho(
            f'Removing to-do # {todo_id} failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    def _remove():
        if second_todo_id != 0:
            for i in range(todo_id - 1, second_todo_id):
                typer.secho(f"""to-do # {i+1} : '{todo["Description"][i]}'was removed""",
                            fg=typer.colors.GREEN, )
            with typer.progressbar(length=100, label="Processing")as progress:
                for _ in progress:
                    time.sleep(0.01)
        else:
            typer.secho(
                f"""to-do # {todo_id}: '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )

    if force:
        _remove()
    else:
        text = ' '
        if second_todo_id != 0:
            for i in range(todo_id - 1, second_todo_id):
                text += f"""Delete to-do # {i+1} : '{todo["Description"][i]}' \n """
            text += '?'
        else:
            text = f"Delete to-do # {todo_id}: {todo['Description']}?"
        delete = typer.confirm(text)
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")


@app.command(name="clear")
def remove_all(
        force: bool = typer.Option(
            ...,
            prompt="Delete all to-dos?",
            help="Force deletion without confirmation",
        ),
) -> None:
    """Remove all to-dos"""
    todoer = get_todo()
    if force:
        error = todoer.remove_all().error
        if error:
            typer.secho(
                f' Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            with typer.progressbar(length=100, label="Processing")as progress:
                for _ in progress:
                    time.sleep(0.01)
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        typer.echo("Operation canceled")


@app.command()
def save(
        path: str = typer.Argument(
            ...,
            help='Where to save to-do database file',
        ),
        no_saving: Optional[bool] = typer.Option(
            None,
            "--without-save",
            "-ws",
            help='using this flag will delete all entries in to-do database file'
        ),
) -> None:
    """ Saving to-do database file in any file"""
    todoer = get_todo()
    error = todoer.save(path, no_saving)
    if error:
        typer.secho(
            f"file could not be saved: '{ERRORS[error]}'",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        with typer.progressbar(length=100, label="Processing")as progress:
            for _ in progress:
                time.sleep(0.01)

        typer.secho(
            f"File successfully saved to file {path}",
            fg=typer.colors.GREEN
        )


@app.command(name="deadline")
def deadline(
        in_time: bool = typer.Option(False, "--intime", "-in", help="Displaying records that have not expired yet"),
        not_in_time: bool = typer.Option(False, "--nottime", "-not",
                                         help="Displays records that have violated the deadline"),
        delete: bool = typer.Option(False, "--delete", "-d", help="Removing outstanding tasks that are overdue")
) -> None:
    """ deleting expired entries and also their conclusion"""
    todoer = get_todo()
    todo_list, error = todoer.get_todo_list()
    if delete + not_in_time + in_time != 1:
        typer.secho("You can use only one flag", fg=typer.colors.RED)
        raise typer.Exit(1)
    if error:
        typer.secho(
            f"The list could not be displayed:'{ERRORS[error]}'",
            fg=typer.colors.RED)
        raise typer.Exit(1)
    date_today = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
    table = PrettyTable()
    table.field_names = ["ID", "Priority", "Done", "Description", "Date", "Deadline"]
    delete_list = list()
    counter_in = 0
    counter_not = 0
    for id, todo in enumerate(todo_list, start=1):
        desc, priority, done, date, deadline = todo.values()
        if deadline == "-":
            id += 1
            continue
        if in_time and date_today < deadline:
            table.add_rows([[id, priority, done, desc, date, deadline]])
            counter_in += 1
        if not_in_time or delete and deadline < date_today and done is False:
            table.add_rows([[id, priority, done, desc, date, deadline]])
            delete_list.append(id)
            counter_not += 1
    if delete and counter_not == 0:
        typer.secho("No entries", fg=typer.colors.RED)
        raise typer.Exit(1)
    elif not_in_time and counter_not == 0:
        typer.secho("No entries", fg=typer.colors.RED)
        raise typer.Exit(1)
    elif not_in_time and counter_not > 0:
        typer.secho(table, fg=typer.colors.BLUE)
        raise typer.Exit()
    if delete and counter_not > 0:
        typer.secho(table, fg=typer.colors.BLUE)
    elif in_time and counter_in == 0:
        typer.secho("No entries", fg=typer.colors.RED)
        raise typer.Exit(1)
    elif in_time and counter_in > 0:
        typer.secho(table, fg=typer.colors.BLUE)
        raise typer.Exit()
    if delete:
        confirm = typer.confirm("Delete to-do's?")
        if confirm is False:
            typer.echo("Operation canceled")
            raise typer.Exit(1)
        confirm_delete_list = list()
        for i in delete_list:
            if typer.confirm(f"""Remove to-do # {i}?"""):
                confirm_delete_list.append(i)
        if len(confirm_delete_list) == 0:
            typer.secho(
                "There are no entries that have passed the deadline",
                fg=typer.colors.BLUE
            )
            raise typer.Exit(1)
        confirm_delete_list = reversed(confirm_delete_list)
        with typer.progressbar(confirm_delete_list, label="Processing")as progress:
            for i in progress:
                todoer.remove(i)
                time.sleep(0.01)
        typer.secho(
            f"Entries successfully deleted",
            fg=typer.colors.GREEN
        )
        raise typer.Exit()


@app.command(name="length")
def length():
    """Number of records"""
    todoer = get_todo()
    todo_list, error = todoer.get_todo_list()
    if error:
        typer.secho(
            f"The list could not be displayed:'{ERRORS[error]}'",
            fg=typer.colors.RED)
        raise typer.Exit(1)
    table = PrettyTable()
    table.field_names = ["ID", "Priority", "Done", "Description", "Date", "Deadline"]
    buf = list()
    for id, todo in enumerate(todo_list, start=1):
        desc, priority, done, date, deadline = todo.values()
        buf = [id, priority, done, desc, date, deadline]
    table.add_rows([buf])
    typer.secho(f"Number of records is {len(todo_list)} \nLast added entry:",
                fg=typer.colors.BLUE)
    typer.secho(table, fg=typer.colors.BLUE)


@app.command(name="search")
def search(
        desc: bool = typer.Option(False, "--desc", "-d", help='Search by Description'),
        done: bool = typer.Option(False, "--done", "-do", help='Search by done'),
        id: bool = typer.Option(False, "--indetif", "-id", help='Search by id'),
        priority: bool = typer.Option(False, "--prior", "-p", help='Search by priority'),
        element: str = typer.Argument(...)
) -> None:
    "Search to-do's in database file"
    todoer = get_todo()
    todo_list, error = todoer.get_todo_list()
    if error:
        typer.secho(
            f"The list could not be displayed:'{ERRORS[error]}'",
            fg=typer.colors.RED)
        raise typer.Exit(1)
    table = PrettyTable()
    table.field_names = ["ID", "Priority", "Done", "Description", "Date", "Deadline"]
    counter = 0
    if desc + done + id + priority != 1:
        typer.secho("You can use only one flag", fg=typer.colors.RED)
        raise typer.Exit()
    if desc:
        for ident, todo in enumerate(todo_list, start=1):
            descript, prior, doned, dated, deadlines = todo.values()
            buf = [ident, prior, doned, descript, dated, deadlines]
            if element == descript:
                table.add_rows([buf])
                counter += 1
    if done:
        if element != "False" and element != "True":
            typer.secho("Incorrect argument", fg=typer.colors.RED)
            raise typer.Exit()
        for ident, todo in enumerate(todo_list):
            descript, prior, doned, dated, deadlines = todo.values()
            buf = [ident, prior, doned, descript, dated, deadlines]
            if element == "False" and doned is False:
                table.add_rows([buf])
                counter += 1
            elif element == "True" and doned is True:
                table.add_rows([buf])
                counter += 1
    if id:
        if element.isdigit() is False:
            typer.secho("Incorrect argument", fg=typer.colors.RED)
        for ident, todo in enumerate(todo_list, start=1):
            descript, prior, doned, dated, deadlines = todo.values()
            buf = [ident, prior, doned, descript, dated, deadlines]
            if int(element) == ident:
                table.add_rows([buf])
                counter += 1

    if priority:
        if element.isdigit() is False or int(element) < 1 or int(element) > 3:
            typer.secho("Incorrect argument", fg=typer.colors.RED)
        for ident, todo in enumerate(todo_list, start=1):
            descript, prior, doned, dated, deadlines = todo.values()
            buf = [ident, prior, doned, descript, dated, deadlines]
            if int(element) == prior:
                table.add_rows([buf])
                counter += 1
    if counter == 0:
        typer.secho("No matches found", fg=typer.colors.BLUE)
        raise typer.Exit(1)
    with typer.progressbar(length=counter, label="Processing")as progress:
        for _ in progress:
            time.sleep(0.01)
    typer.secho("Search result:", fg=typer.colors.GREEN)
    typer.secho(table, fg=typer.colors.BLUE)
    raise typer.Exit()


def _edit(redactor: bool) -> None:
    if redactor:
        default_text_editor = database.get_text_editor(config.CONFIG_FILE_PATH)
        text_editor = typer.prompt("Press enter if standard editor will be used or type another default:",
                                   default_text_editor)
        todoer = get_todo()
        error = todoer.editor(text_editor)
        if error:
            typer.secho(f"Trying to open a file with {text_editor} Error: '{ERRORS[error]}'",
                        fg=typer.colors.RED)
            raise typer.Exit(1)
        else:
            typer.secho(f"The file was edited successfully using the editor: {text_editor}",
                        fg=typer.colors.GREEN)
            raise typer.Exit()


def _version_callback(value: bool) -> None:
    if value:
        typer.secho(f"{__app_name__},v{__version__}", fg=typer.colors.BLUE)
        raise typer.Exit()


def _path_callback(path: bool) -> None:
    if path:
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        typer.secho(
            f"Current to-do path:{db_path}",
            fg=typer.colors.BLUE
        )
        raise typer.Exit()


def _redactor_callback(editor: bool) -> None:
    if editor:
        db_edit = database.get_text_editor(config.CONFIG_FILE_PATH)
        typer.secho(
            f"Current to-do text editor:{db_edit}",
            fg=typer.colors.BLUE
        )
        raise typer.Exit()


def _delete(delete: bool) -> None:
    if delete:
        method = typer.confirm("Remove items in reverse order?")
        todoer = get_todo()
        todo, error = todoer.get_todo_list()
        if len(todo) == 0:
            typer.secho(
                "There are no entries in to-do database file",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        delete_list = list()
        if method:
            for i in range(len(todo), 0, -1):
                if typer.confirm(f"""Remove to-do # {i} : '{todo[i-1]["Description"]}' ?"""):
                    delete_list.append(i)
        else:
            for i in range(1, len(todo) + 1):
                if typer.confirm(f"""Remove to-do # {i} : '{todo[i-1]["Description"]}' ?"""):
                    delete_list.append(i)
        if len(delete_list) == 0:
            typer.secho(
                "No changes",
                fg=typer.colors.BLUE
            )
            raise typer.Exit()
        if method is False:
            delete_list = reversed(delete_list)
        with typer.progressbar(delete_list, label="Processing")as progress:
            for i in progress:
                todoer.remove(i)
                time.sleep(0.01)
        typer.secho(
            f"Entries successfully deleted",
            fg=typer.colors.GREEN
        )
        raise typer.Exit()


def _docs(docs: bool) -> None:
    if docs:
        typer.echo("Opening Typer's docs")
        typer.launch("https://typer.tiangolo.com")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
        editor: Optional[bool] = typer.Option(
            None,
            "--edit",
            "-e",
            help="Edit to-do file with help text editor",
            callback=_edit,
        ),
        path: Optional[bool] = typer.Option(
            None,
            "--path",
            "-p",
            help='Show current path to-do json file',
            callback=_path_callback,
        ),
        redactor: Optional[bool] = typer.Option(
            None,
            "--redactor",
            "-r",
            help="Show current text editor",
            callback=_redactor_callback
        ),
        delete: Optional[bool] = typer.Option(
            None,
            "--delete",
            "-d",
            help="Sequential deletion",
            callback=_delete
        ),
        docs: Optional[bool] = typer.Option(
            None,
            "--docs",
            "-do",
            help="Go to the library website Typer",
            callback=_docs
        ),
) -> None:
    return
