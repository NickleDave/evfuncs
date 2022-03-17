import pathlib

import pytest


HERE = pathlib.Path(__file__).parent
DATA_FOR_TESTS_ROOT = HERE / '..' / 'data_for_tests'


@pytest.fixture
def data_for_tests_root():
    return DATA_FOR_TESTS_ROOT


@pytest.fixture
def gy6or6_032312_subset_root(data_for_tests_root):
    return data_for_tests_root / 'gy6or6_032312_subset'
