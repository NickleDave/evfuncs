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


@pytest.fixture
def notmat_with_single_annotated_segment(data_for_tests_root):
    return data_for_tests_root / 'or60yw70-song-edited-to-have-single-segment' / 'or60yw70_300912_0725.437.cbin.not.mat'
