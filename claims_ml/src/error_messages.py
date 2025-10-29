from enum import Enum

SUPPORTED_FILE_EXTENSIONS = [".csv", ".parquet"]


class DataReadingErrorMessages(
    Enum
):  # TEK yerden yönetmek istiyoruz prjenin her yerinde oluşabilecek hataları
    INVALID_FILE_PATH_TYPE = "file_path must be a string or Path object."
    EMPTY_DATA_ERROR = "No data: The file at {file_path} is empty."
    PARSING_ERROR = "Parsing error: Could not parse the file at {file_path}."
    UNEXPECTED_ERROR = "An error occurred while loading data: {error}"
    FILE_NOT_FOUND = "File not found: {file_path}"
    EXT_NOT_SUPPORTED = (
        "File extension '{ext}' is not supported. Expected one of {supported_exts}."
    )
