import pytest


@pytest.fixture
def cbins(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*.cbin'))


@pytest.fixture
def notmats(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*.not.mat'))


@pytest.fixture
def rec_files(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*.rec'))


@pytest.fixture
def filtsong_mat_files(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*filtsong*.mat'))


@pytest.fixture
def smooth_data_mat_files(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*smooth_data*.mat'))


@pytest.fixture
def segment_mats(gy6or6_032312_subset_root):
    return sorted(gy6or6_032312_subset_root.glob('*unedited_SegmentNotes_output.mat'))
