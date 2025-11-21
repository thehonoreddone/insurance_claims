import os
from pathlib import Path
import logging  # logging Python’un yerleşik log (günlük kayıt) kütüphanesidir.
# , programın çalışması sırasında meydana gelen olayları (örneğin hata, uyarı, bilgi mesajı vb.) kaydeder.

import pandas as pd
from typing import Optional, Union
from ..error_messages import DataReadingErrorMessages as EM, SUPPORTED_FILE_EXTENSIONS


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

data_reader_functions = {
    ".csv": pd.read_csv,
    ".parquet": pd.read_parquet,
}


class DataLoader:
    """Class for loading insurance claims data from CSV files."""

    def load_data(self, file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
        """Loads data from the CSV file into a pandas DataFrame.

        returns:
            pd.DataFrame: DataFrame containing the loaded data.

        raises:
            TypeError: If file_path is not a string or Path object.
            FileNotFoundError: If the file does not exist at the specified path.
            ValueError: If the file extension is not supported or if the file is empty.
        """

        self._validate_file_path(file_path)

        ext = self._check_if_file_extension_supported(file_path)

        reader_func = data_reader_functions.get(ext)
        data: pd.DataFrame = reader_func(file_path)

        # data = pd.read_csv(file_path)
        if data.empty:
            logger.error(EM.EMPTY_DATA_ERROR.value.format(file_path=file_path))
            raise ValueError(EM.EMPTY_DATA_ERROR.value.format(file_path=file_path))
        return data

    def _validate_file_path(
        self, file_path: Union[str, Path]
    ) -> None:  # load_data'ya değil ayrı bi fonksiyona yazdık çünkü orada mantıken sadece veri yüklenir validate ayrı
        if not isinstance(file_path, (str, Path)):
            logger.error(EM.INVALID_FILE_PATH_TYPE.value.format(type=type(file_path)))
            raise TypeError(
                EM.INVALID_FILE_PATH_TYPE.value.format(type=type(file_path))
            )  # kodda en salakça ne olabilir ornegin bu hata olur ve return none değil hata oldugu için bir tip hatası
        if not Path(file_path).exists():
            logger.error(EM.FILE_NOT_FOUND.value.format(file_path=file_path))
            raise FileNotFoundError(EM.FILE_NOT_FOUND.value.format(file_path=file_path))

    def _check_if_file_extension_supported(self, file_path: Union[str, Path]) -> str:
        ext = Path(file_path).suffix.lower()
        if ext not in SUPPORTED_FILE_EXTENSIONS:
            logger.error(
                EM.EXT_NOT_SUPPORTED.value.format(
                    ext=ext, supported_exts=SUPPORTED_FILE_EXTENSIONS
                )
            )
            raise ValueError(
                EM.EXT_NOT_SUPPORTED.value.format(
                    ext=ext, supported_exts=SUPPORTED_FILE_EXTENSIONS
                )
            )
        return ext
