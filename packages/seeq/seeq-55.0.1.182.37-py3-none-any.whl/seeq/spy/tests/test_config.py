import os
import warnings

import pytest

from seeq.spy._config import get_data_lab_project_url, get_data_lab_project_id

SERVER_URL = 'http://seeq.com'
PROJECT_UUID = '12345678-9ABC-DEF0-1234-56789ABCDEF0'


def setup_environment_variables():
    os.environ['SEEQ_SERVER_URL'] = SERVER_URL
    os.environ['SEEQ_PROJECT_UUID'] = PROJECT_UUID


def setup_module():
    setup_environment_variables()


@pytest.mark.unit
def test_sdl_project_uuid():
    assert get_data_lab_project_id() == PROJECT_UUID


@pytest.mark.unit
def test_sdl_project_url():
    expected_project_url = f'{SERVER_URL}/data-lab/{PROJECT_UUID}'
    assert get_data_lab_project_url() == expected_project_url


@pytest.mark.unit
def test_sdl_project_uuid():
    assert get_data_lab_project_id() == PROJECT_UUID


@pytest.mark.unit
def test_sdl_project_url():
    expected_project_url = f'{SERVER_URL}/data-lab/{PROJECT_UUID}'
    assert get_data_lab_project_url() == expected_project_url


@pytest.mark.unit
def test_warning_as_error_user():
    with pytest.raises(UserWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", UserWarning)


@pytest.mark.unit
def test_warning_as_error_syntax():
    with pytest.raises(SyntaxWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", SyntaxWarning)


@pytest.mark.unit
def test_warning_as_error_runtime():
    with pytest.raises(RuntimeWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", RuntimeWarning)


@pytest.mark.unit
def test_warning_as_error_future():
    with pytest.raises(FutureWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", FutureWarning)


@pytest.mark.unit
def test_warning_as_error_unicode():
    with pytest.raises(UnicodeWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", UnicodeWarning)


@pytest.mark.unit
def test_warning_as_error_bytes():
    with pytest.raises(BytesWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", BytesWarning)


@pytest.mark.unit
def test_warning_as_error_resource():
    with pytest.raises(ResourceWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", ResourceWarning)


@pytest.mark.unit
def test_warning_as_error_import():
    with pytest.raises(ImportWarning):
        warnings.warn("this warning should be thrown as an error by pytest in .py", ImportWarning)
