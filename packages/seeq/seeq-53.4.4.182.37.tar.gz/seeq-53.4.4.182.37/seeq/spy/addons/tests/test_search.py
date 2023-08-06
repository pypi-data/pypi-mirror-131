import pandas as pd
import pytest

from seeq.sdk import *
from seeq.spy import _login
from seeq.spy import addons
from seeq.spy.tests import test_common
from seeq.spy.addons.tests import test_common as addons_test_common


def setup_module():
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(True)
    test_common.login(agent_api_key_user=False)


def teardown_module():
    # reset default value of AddOnTools/Enabled to False
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(False)


def _create_test_tools(suffix_=''):
    my_tools = [{"Name": f'test tool 1_{suffix_}',
                 "Description": f"test tool 1{suffix_}",
                 "Target URL": "http://www.google.com",
                 "Icon": "fa fa-icon",
                 "Link Type": "tab",
                 "Users": [_login.user.username]},
                {"Name": f'test tool 2_{suffix_}',
                 "Description": f"test tool 2{suffix_}",
                 "Target URL": "http://www.seeq.com",
                 "Icon": "fa fa-icon",
                 "Users": [_login.user.username]
                 }]
    # searching for tools doesn't require admin access but creating tools does
    test_common.login(admin=True)
    tools = addons.install(my_tools)
    # log back in as a non-admin, non-agent_api_key user
    test_common.login(agent_api_key_user=False)
    return tools


def _uninstall_test_tools(ids):
    test_common.login(admin=True)
    for idd in ids:
        system_api = SystemApi(test_common.get_client())
        system_api.delete_add_on_tool(id=idd)
    # log back in as a non-admin, non-agent_api_key user
    test_common.login(admin=False, agent_api_key_user=False)


@pytest.mark.system
def test_addon_support():
    addons_test_common.test_addon_support('search', dict())


@pytest.mark.system
def test_search_all_installed_tools():
    system_api = SystemApi(test_common.get_client())
    tools = system_api.get_add_on_tools().add_on_tools

    query = {'Name': '*'}
    search_results = addons.search(query)

    assert len(tools) == len(search_results)
    assert isinstance(search_results.status.df, pd.DataFrame)
    assert search_results.kwargs['query'] == query


@pytest.mark.system
def test_search_with_wildcard_plus_another_prop():
    unique_name_suffix = str(pd.to_datetime("today"))
    df_tools = _create_test_tools(suffix_=unique_name_suffix)

    query = {'Name': '*', "Description": f"2{unique_name_suffix}"}
    search_results = addons.search(query)

    assert len(search_results) == 1
    # clean up
    _uninstall_test_tools(df_tools['ID'].values)


@pytest.mark.system
def test_search_with_wildcard_plus_id():
    unique_name_suffix = str(pd.to_datetime("today"))
    df_tools = _create_test_tools(suffix_=unique_name_suffix)

    query = {'Name': '*', "ID": df_tools['ID'].values[0]}
    search_results = addons.search(query)

    assert len(search_results) == 1

    # clean up
    _uninstall_test_tools(df_tools['ID'].values)


@pytest.mark.system
def test_search_by_id():
    unique_name_suffix = str(pd.to_datetime("today"))
    df_tools = _create_test_tools(suffix_=unique_name_suffix)
    idd = df_tools['ID'][0]
    search_results = addons.search({"ID": idd})
    assert len(search_results) == 1
    # clean up
    _uninstall_test_tools(df_tools['ID'].values)


@pytest.mark.system
def test_search_with_df():
    unique_name_suffix = str(pd.to_datetime("today"))
    df_tools = _create_test_tools(suffix_=unique_name_suffix)
    my_items = pd.DataFrame(
        {'Name': [f'test tool 1_{unique_name_suffix}', f'test tool 2_{unique_name_suffix}'],
         'Link Type': 'window'})
    search_results = addons.search(my_items)
    assert len(search_results) == 1
    assert search_results['Link Type'][0] == 'window'

    # clean up
    _uninstall_test_tools(df_tools['ID'].values)


@pytest.mark.system
def test_search_with_multiple_props():
    unique_name_suffix = str(pd.to_datetime("today"))
    df_tools = _create_test_tools(suffix_=unique_name_suffix)

    search = addons.search({"Name": "test tool", "Description": "test tool"})
    assert len(search) >= 2

    search_results_no_match = addons.search(
        pd.DataFrame([{"Name": f'test tool', "Description": "test tool"}]))
    search_results_match = addons.search(pd.DataFrame([{"Name": f'test tool 1_{unique_name_suffix}',
                                                        "Description": f"test tool 1{unique_name_suffix}"},
                                                       {"Name": f'test tool 2_{unique_name_suffix}',
                                                        "Description": f"test tool 2{unique_name_suffix}"}]))
    assert len(search_results_match) - len(search_results_no_match) == 2

    # clean up
    _uninstall_test_tools(df_tools['ID'].values)
