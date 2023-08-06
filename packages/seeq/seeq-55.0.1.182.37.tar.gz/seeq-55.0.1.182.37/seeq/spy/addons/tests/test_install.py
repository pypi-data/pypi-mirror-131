import pandas as pd
import pytest

from seeq.sdk import *
from seeq.spy import _login
from seeq.spy import addons
from seeq.spy._errors import *
from seeq.spy.addons import _permissions
from seeq.spy.tests import test_common
from seeq.spy.addons.tests import test_common as addons_test_common


def setup_module():
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(True)


def teardown_module():
    # reset default value of AddOnTools/Enabled to False
    test_common.login(admin=True)
    addons_test_common.enable_addon_tools(False)


def create_testing_group():
    user_groups_api = UserGroupsApi(test_common.get_client())
    group_name = 'testers'

    try:
        group = _login.find_group(group_name)
    except RuntimeError:
        group = user_groups_api.create_user_group(body={"name": group_name})

    return group


@pytest.mark.system
def test_addon_support():
    addons_test_common.test_addon_support('install', dict())


@pytest.mark.system
def test_install_one_tool():
    system_api = SystemApi(test_common.get_client())
    items_api = ItemsApi(test_common.get_client())

    def tool_names():
        tools = system_api.get_add_on_tools().add_on_tools
        return [tool.name for tool in tools]

    unique_name_suffix = str(pd.to_datetime("today"))
    new_name = f"test tool_{unique_name_suffix}"
    my_tool = {"Name": new_name,
               "Description": "My new tool",
               "Target URL": "http://www.google.com",
               "Groups": ["Everyone"]}

    df = addons.install(my_tool)
    assert items_api.get_item_and_all_properties(id=df['ID'].values[0])
    permissions = _permissions.get_addon_permissions(df['ID'].values[0], items_api)
    assert 'Everyone' in permissions['Groups']
    assert new_name in tool_names()

    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_install_one_tool_with_existing_query_params():
    items_api = ItemsApi(test_common.get_client())

    unique_name_suffix = str(pd.to_datetime("today"))
    new_name = f"test tool_{unique_name_suffix}"
    my_tool = {"Name": new_name,
               "Description": "My new tool",
               "Target URL": "http://www.google.com?previous=123",
               "Icon": "fa fa-icon"}

    df = addons.install(my_tool, include_workbook_parameters=True)
    tool = items_api.get_item_and_all_properties(id=df['ID'].values[0])
    workbook_params = f'&workbookId={{workbookId}}&worksheetId={{worksheetId}}&workstepId={{' \
                      f'workstepId}}&seeqVersion={{seeqVersion}}'
    target_url = f"{my_tool['Target URL']}{workbook_params}"
    assert target_url == [x for x in tool.properties if x.name == 'Target URL'][0].value

    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_install_one_tool_with_workbook_params():
    items_api = ItemsApi(test_common.get_client())

    unique_name_suffix = str(pd.to_datetime("today"))
    new_name = f"test tool query params_{unique_name_suffix}"
    my_tool = {"Name": new_name,
               "Description": "My new tool",
               "Target URL": "http://www.google.com?",
               "Icon": "fa fa-icon"}

    df = addons.install(my_tool, include_workbook_parameters=True)
    tool = items_api.get_item_and_all_properties(id=df['ID'].values[0])
    workbook_params = f'workbookId={{workbookId}}&worksheetId={{worksheetId}}&workstepId={{' \
                      f'workstepId}}&seeqVersion={{seeqVersion}}'
    target_url = f"{my_tool['Target URL']}{workbook_params}"
    assert target_url == [x for x in tool.properties if x.name == 'Target URL'][0].value

    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_install_multiple_tools():
    system_api = SystemApi(test_common.get_client())
    items_api = ItemsApi(test_common.get_client())
    projects_api = ProjectsApi(test_common.get_client())
    users_api = UsersApi(test_common.get_client())

    user_id = users_api.get_me().id
    sdl_project1 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))
    sdl_project2 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))

    def tool_names():
        tools = system_api.get_add_on_tools().add_on_tools
        return [tool.name for tool in tools]

    unique_name_suffix = str(pd.to_datetime("today"))
    new_tools = [
        {
            "Name": f'My New Tool_{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project1.id}/apps/my_tool.ipynb",
            "Icon": "fa fa-bell"},
        {
            "Name": f'Your New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project2.id}/apps/tool2.ipynb",
            "Icon": "fa fa-bars"}]

    df = addons.install(new_tools, errors='raise')
    for idd in df['ID'].values:
        assert items_api.get_item_and_all_properties(id=idd)

    for tool in new_tools:
        assert tool['Name'] in tool_names()

    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_update_tool_false():
    system_api = SystemApi(test_common.get_client())
    items_api = ItemsApi(test_common.get_client())

    def tool_names():
        tools = system_api.get_add_on_tools().add_on_tools
        return [tool.name for tool in tools]

    unique_name_suffix = str(pd.to_datetime("today"))
    name = f"overwrite false{unique_name_suffix}"
    my_tool = {"Name": name,
               "Description": "My new tool",
               "Target URL": "http://www.google.com",
               "Icon": "fa fa-icon"}

    df = addons.install(my_tool, update_tool=False)
    assert items_api.get_item_and_all_properties(id=df['ID'].values[0])
    assert name in tool_names()
    with pytest.raises(SPyException,
                       match=f'Add-on tool with name "{name}" already exists. '
                             f'You can update the existing tool with `update_tool=True`'):
        addons.install(my_tool, update_tool=False)
    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_update_tools_from_df():
    projects_api = ProjectsApi(test_common.get_client())
    users_api = UsersApi(test_common.get_client())

    user_id = users_api.get_me().id
    sdl_project1 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))
    sdl_project2 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))

    unique_name_suffix = str(pd.to_datetime("today"))
    new_tools = [
        {
            "Name": f'My New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project1.id}/apps/my_tool.ipynb",
            "Icon": "fa fa-bell",
            "Link Type": "window"},
        {
            "Name": f'Your New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project2.id}/apps/tool2.ipynb",
            "Icon": "fa fa-bars",
            "Link Type": "window"}]

    df = addons.install(new_tools)

    searched_tools = addons.search(df)

    for _, tool in searched_tools.iterrows():
        assert tool['Link Type'] == 'window'

    searched_tools["Link Type"] = ['tab'] * len(searched_tools)
    df_installed = addons.install(searched_tools, update_tool=True)

    searched_tools = addons.search(df)

    for _, tool in searched_tools.iterrows():
        assert tool['Link Type'] == 'tab'

    # clean up
    addons.uninstall(df_installed)


@pytest.mark.system
def test_change_permissions():
    projects_api = ProjectsApi(test_common.get_client())
    users_api = UsersApi(test_common.get_client())
    items_api = ItemsApi(test_common.get_client())
    group = create_testing_group()

    user_id = users_api.get_me().id
    sdl_project1 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))
    sdl_project2 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))
    unique_name_suffix = str(pd.to_datetime("today"))
    new_tools = [
        {
            "Name": f'My New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project1.id}/apps/my_tool.ipynb",
            "Icon": "fa fa-bell",
            "Link Type": "window",
            "Groups": ["testers"]},
        {
            "Name": f'Your New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project2.id}/apps/tool2.ipynb",
            "Icon": "fa fa-bars",
            "Link Type": "window",
            "Groups": ["testers"]}]

    df = addons.install(new_tools)

    search_df = addons.search({"Name": f'My New Tool{unique_name_suffix}'})

    # Pass only the ID to make sure it's not grabbing other properties from the search_df
    idd = search_df['ID'][0]

    # Remove group permissions
    addons.install(pd.Series({"ID": idd, "Groups": []}), update_permissions=True, update_tool=False)

    permissions = _permissions.get_addon_permissions(idd, items_api)
    assert len(permissions['Groups']) == 0
    assert len(permissions["Users"]) == 0

    addons.install({"ID": idd, "Groups": [group.name]}, update_permissions=True)


@pytest.mark.system
def test_update_tools_and_update_permissions_passing_id():
    projects_api = ProjectsApi(test_common.get_client())
    users_api = UsersApi(test_common.get_client())

    user_id = users_api.get_me().id
    sdl_project1 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))
    sdl_project2 = projects_api.create_project(body=dict(name='test project 1', ownerId=user_id))

    unique_name_suffix = str(pd.to_datetime("today"))
    new_tools = [
        {
            "Name": f'My New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project1.id}/apps/my_tool.ipynb",
            "Icon": "fa fa-bell",
            "Link Type": "window",
            "Groups": ["Everyone"]
        },
        {
            "Name": f'Your New Tool{unique_name_suffix}',
            "Description": "this is an awesome tool",
            "Target URL": f"http://www.my.seeq.com/data-lab/{sdl_project2.id}/apps/tool2.ipynb",
            "Icon": "fa fa-bars",
            "Link Type": "window"}]

    df = addons.install(new_tools)

    searched_tools = addons.search(df)

    for _, tool in searched_tools.iterrows():
        assert tool['Link Type'] == 'window'

    searched_tools["Link Type"] = ['tab'] * len(searched_tools)
    searched_tools['Groups'] = [['testers']] * len(searched_tools)
    df_installed = addons.install(searched_tools, update_tool=True, update_permissions=True)

    searched_tools = addons.search(df)

    for _, tool in searched_tools.iterrows():
        assert tool['Link Type'] == 'tab'
        assert 'testers' in tool['Groups']
        assert 'Everyone' not in tool['Groups']

    # clean up
    addons.uninstall(df_installed)


@pytest.mark.system
def test_mix_update_tool_and_new_tool():
    items_api = ItemsApi(test_common.get_client())

    unique_name_suffix = str(pd.to_datetime("today"))
    name = f"test previous_tool_{unique_name_suffix}"
    my_tool = {"Name": name,
               "Description": "an awesome tool",
               "Target URL": "http://www.google.com?",
               "Icon": "fa fa-icon"}

    df = addons.install(my_tool, include_workbook_parameters=True, update_tool=True)
    previous_id = df['ID'].values[0]
    tool = items_api.get_item_and_all_properties(id=previous_id)
    assert my_tool['Description'] == [x for x in tool.properties if x.name == 'Description'][0].value

    new_install = [{"Name": name,
                    "Description": "an awesome tool updated",
                    "Target URL": "http://www.google.com?",
                    "Icon": "fa fa-icon"},
                   {"Name": name + '_new',
                    "Description": "this is new",
                    "Target URL": "http://www.google.com?",
                    "Icon": "fa fa-icon"}]

    df = addons.install(new_install, include_workbook_parameters=True, update_tool=True)
    tool = items_api.get_item_and_all_properties(id=previous_id)
    tool2 = items_api.get_item_and_all_properties(id=df['ID'][1])
    assert new_install[0]['Description'] == [x for x in tool.properties if x.name == 'Description'][0].value
    assert new_install[1]['Description'] == [x for x in tool2.properties if x.name == 'Description'][0].value
    assert len(df) == 2
    assert df['Result'][0] == 'Updated'
    assert df['Result'][1] == 'Installed'

    # clean up
    addons.uninstall(df)


@pytest.mark.system
def test_update_duplicated_tool():
    system_api = SystemApi(test_common.get_client())
    unique_name_suffix = str(pd.to_datetime("today"))
    name = f"same name twice_{unique_name_suffix}"

    new_tool_config = dict(
        name=name,
        description="duplicated test",
        iconClass='fa fa-bars',
        targetUrl=f'https://www.seeq.com',
        linkType="window",
        windowDetails="toolbar=0,height=600,width=600",
        sortKey="a",
        # need to cast to bool if coming from pandas as np.bool_
        reuseWindow=True,
    )

    tool1_id = system_api.create_add_on_tool(body=new_tool_config).id
    tool2_id = system_api.create_add_on_tool(body=new_tool_config).id

    my_tool = {"Name": name,
               "Description": "an awesome tool",
               "Target URL": "http://www.google.com?",
               "Icon": "fa fa-icon"}

    # addons.install fails to update if update_tool=False
    with pytest.raises(SPyException,
                       match=f'Add-on tool with name "{name}" already exists. '
                             f'You can update the existing tool with `update_tool=True`'):
        addons.install(my_tool, include_workbook_parameters=True, update_tool=False)

    # addons.install fails to update even with update_tool=True since there are two tools with the same name
    with pytest.raises(SPyException,
                       match=f'There exists 2 tools with the name "{name}". '
                             f'You can supply the ID to avoid ambiguity and modify only the intended tool'):
        addons.install(my_tool, include_workbook_parameters=True, update_tool=True)

    my_tool = {"ID": tool1_id,
               "Name": name,
               "Description": "an awesome tool",
               "Target URL": "http://www.google.com?",
               "Icon": "fa fa-icon"}

    # passing the ID resolves the ambiguity and allows the update
    df = addons.install(my_tool, include_workbook_parameters=True, update_tool=True)

    assert len(df) == 1
    assert df['Result'][0] == 'Updated'

    # clean up
    addons.uninstall(pd.DataFrame([{"ID": tool1_id}, {"ID": tool2_id}]))
