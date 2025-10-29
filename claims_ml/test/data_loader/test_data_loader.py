import pytest
from pathlib import Path
from insurance_claims.claims_ml.src.data_loader.data_loader import DataLoader


@pytest.fixture
def data_loader():
    return DataLoader()  # buradaki DataLoader'ı tüm testlerde kullanacagımız için bu şekilde yazdık ve tek bi yerden yönetebliliriz.


def test_check_if_file_extension_supported_valid(data_loader: DataLoader):
    ext = data_loader._check_if_file_extension_supported("data.csv")

    with pytest.raises(ValueError):
        data_loader._check_if_file_extension_supported("data.txt")
