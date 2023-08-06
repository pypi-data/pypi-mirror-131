import pandas as pd
import pytest

from seeq.spy import addons
from seeq.spy.tests import test_common
from seeq.spy.addons.tests import test_common as addons_test_common


def setup_module():
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(True)


def teardown_module():
    # reset default value of AddOnTools/Enabled to False
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(False)


@pytest.mark.system
def test_addon_support():
    addons_test_common.test_addon_support('uninstall', pd.DataFrame())


@pytest.mark.system
def test_uninstall_tools():
    unique_name_suffix = str(pd.to_datetime("today"))
    my_tools = [{"Name": f'test tool 1_{unique_name_suffix}',
                 "Description": "test tool 1",
                 "Target URL": "http://www.google.com",
                 "Icon": "fa fa-icon",
                 "Link Type": "tab"},
                {"Name": f'test tool 2_{unique_name_suffix}',
                 "Description": "test tool 2",
                 "Target URL": "http://www.seeq.com",
                 "Icon": "fa fa-icon"}]
    df_tools = addons.install(my_tools)
    search_results = addons.search(df_tools)

    assert len(search_results) == 2
    addons.uninstall(search_results)
    search_results = addons.search(df_tools)

    assert search_results.empty
