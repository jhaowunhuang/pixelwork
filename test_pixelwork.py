import pytest
import os


# @pytest.mark.parametrize('input_file_name', 'sample/input.jpg')
# @pytest.mark.parametrize('output_file_name', 'test_output.jpg')
@pytest.fixture(params=[('input_file_name', 'sample/input.jpg'), ('output_file_name', 'test_output.jpg')])
def test_output_file():
    assert os.path.isfile('./test_output.jpg')  # True
