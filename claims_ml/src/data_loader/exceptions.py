class DataLoaderError(Exception):
    """Base class for exceptions in DataLoader."""

    pass


class DataPathTypeError(DataLoaderError):
    """Exception raised for errors in the input file path type."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
