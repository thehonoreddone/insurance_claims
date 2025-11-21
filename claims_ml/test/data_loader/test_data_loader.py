import pytest
import re
from pathlib import Path
from insurance_claims.claims_ml.src.data_loader.data_loader import (
    DataLoader,
    SUPPORTED_FILE_EXTENSIONS,
)
import pandas as pd


@pytest.fixture
def data_loader():
    return DataLoader()  # buradaki DataLoader'ı tüm testlerde kullanacagımız için bu şekilde yazdık ve tek bi yerden yönetebliliriz.


# expected value tests       / yazdıgımız metod veya class neyse bunlara dogru parametreleri girince dogru sonucu veriyor mu bunu test eder


@pytest.mark.parametrize(
    "file_name, expected_data",
    [
        pytest.param(
            "test.csv", "load_csv_data", id="csv"
        ),  
        pytest.param("test.parquet", "load_parquet_data", id="parquet"),
        pytest.param("test_empty.csv", "empty_dataset", id="empty_csv"),
    ],
)
def test_load_data_with_valid_files(
    data_loader: DataLoader, request, test_dataset_path, file_name, expected_data
):
    file_path = test_dataset_path / file_name
    expected_df = request.getfixturevalue(expected_data)

    data = data_loader.load_data(file_path)
    assert isinstance(data, pd.DataFrame)
    pd.testing.assert_frame_equal(data, expected_df)

@pytest.mark.parametrize(
    "file_name",
    [
        pytest.param("test_empty.csv", id="empty_csv"),
    ],
)
def test_load_data_raises_value_error_for_empty_file(
    data_loader: DataLoader, test_dataset_path, file_name):
    file_path= test_dataset_path / file_name
    with pytest.raises(
        ValueError,match=re.escape(
            f"No data: The file at {file_path} is empty.")):
        data_loader.load_data(file_path)

    

# Method Tests 1/ Expected Value
@pytest.mark.parametrize(
    ("extension", "file_name"),
    [
        (".csv", "test.csv"),
        (".parquet", "test.parquet"),
        (".csv", "test.parquet.csv"),
        (
            ".parquet",
            "test.csv.parquet",
        ),  # metodda suffix kullandıgımız için son eki alıp dogru uzantıyı döndürüyor.
        (".csv", "test/file.csv"),
        (".parquet", "test/file.parquet"),
    ],
)  # loop yazmak yerine parametrize kullandık. bu parametreleri benim için dolaş ve test et.
def test_check_if_file_extension_returns_correct_result(
    data_loader: DataLoader, extension, file_name
):
    assert data_loader._check_if_file_extension_supported(file_name) == extension


# Method Tests 1/ Excepted Errors
@pytest.mark.parametrize("file_ext", [".txt", ".xlsx", ".json", ".xml", ".docx"])
def test_check_if_file_extension_throws_value_error_when_unsupported(
    data_loader: DataLoader, file_ext
):
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"File extension '{file_ext}' is not supported. Expected one of ['.csv', '.parquet']."
        ),
    ):
        data_loader._check_if_file_extension_supported(
            f"test{file_ext}"
        )  # test ve kod mesajı da uyumlu olmalı.


@pytest.mark.parametrize("invalid_path_input,error_type,error_message_match_template",
        [
            pytest.param(123, TypeError, "file_path must be a string or Path object.", id="invalid_type"),
        
            pytest.param("non_existent_file.csv", FileNotFoundError, "File not found: non_existent_file.csv", id="file_not_found"),
        
        ]
          )
def test_validate_file_path_raises_exceptions_for_invalid_inputs(data_loader: DataLoader,
                                                                invalid_path_input,
                                                                error_type,
                                                                error_message_match_template,
                                                                test_datasets_path):
    path_to_check=invalid_path_input
    if (
        isinstance(invalid_path_input, str)
        and "non_existent_file" in invalid_path_input
    ):
        path_to_check = test_datasets_path / invalid_path_input
    
    expected_message = error_message_match_template
    if "{path}" in error_message_match_template:
        expected_message = error_message_match_template.format(path=path_to_check)
    
    with pytest.raises(error_type, match=re.escape(expected_message)):
        data_loader._validate_file_path(path_to_check)