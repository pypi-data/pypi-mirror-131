"""
Top-level package for TodoJournal
"""

__app_name__ = 'Todo Journal'
__version__ = '0.0.1'

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
    EDITOR_ERROR,
    DIRECTORY_ERROR,
    PERMISSION_ERROR,
    INDEX_ERROR,
    LIST_EMPTY,
    INVALID_DATE
) = range(13)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
    EDITOR_ERROR: "wrong editor",
    DIRECTORY_ERROR: "Is a directory,Please create a file",
    PERMISSION_ERROR: "Permission denied",
    INDEX_ERROR: "Incorrect index",
    LIST_EMPTY: "List is empty",
    INVALID_DATE: "Incorrect date entered"}
