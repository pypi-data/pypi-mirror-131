import os
import textwrap
import time
from typing import Optional

import pandas as pd
import pytest

from seeq import spy
from seeq.sdk import *
from seeq.spy import _common
from seeq.spy import _login
from seeq.spy.workbooks import Analysis

ADMIN_USER_NAME = 'admin@seeq.com'
ADMIN_PASSWORD = 'myadminpassword'

NON_ADMIN_NAME = 'non_admin'
NON_ADMIN_LAST_NAME = 'tester'
NON_ADMIN_USERNAME = f'{NON_ADMIN_NAME}.{NON_ADMIN_LAST_NAME}@seeq.com'
NON_ADMIN_PASSWORD = 'mynonadminpassword'


def login(url=None, private_url=None, admin=False, agent_api_key_user=True):
    if admin:
        if not get_client():
            # We need to be logged in as some user in order to create the admin user
            login(url, private_url, admin=False)
        create_admin_user()
        credentials = [ADMIN_USER_NAME, ADMIN_PASSWORD]
    elif not agent_api_key_user:
        # use this option if an autocomplete identity is needed that is discoverable via _login.find_user(user_name)
        if not get_client():
            # We need to be logged in as some user in order to create another user
            login(url, private_url, admin=False, agent_api_key_user=True)
        add_normal_user(NON_ADMIN_NAME, NON_ADMIN_LAST_NAME, NON_ADMIN_USERNAME, NON_ADMIN_PASSWORD)
        credentials = [NON_ADMIN_USERNAME, NON_ADMIN_PASSWORD]
    else:
        # this will be the default agent_api_key user which is a non-auto complete identity
        key_path = os.path.join(get_test_data_folder(), 'keys', 'agent.key')
        with open(key_path, "r") as f:
            credentials = f.read().splitlines()

    spy.login(credentials[0], credentials[1], url=url, private_url=private_url)

    wait_for_example_data()


def get_user(username) -> Optional[UserOutputV1]:
    users_api = UsersApi(get_client())
    user_output_list = users_api.get_users()
    for user in user_output_list.users:  # type: UserOutputV1
        if user.username == username:
            return user

    return None


def get_group(group_name) -> Optional[IdentityPreviewV1]:
    user_groups_api = UserGroupsApi(get_client())
    user_groups_output_list = user_groups_api.get_user_groups()
    for group in user_groups_output_list.items:  # type: IdentityPreviewV1
        if group.name == group_name:
            return group

    return None


def add_normal_user(first_name, last_name, username, password) -> UserOutputV1:
    user = get_user(username)
    if user:
        return user

    users_api = UsersApi(get_client())
    return users_api.create_user(body=UserInputV1(
        first_name=first_name,
        last_name=last_name,
        email=username,
        username=username,
        password=password
    ))


def create_admin_user():
    user = get_user(ADMIN_USER_NAME)
    if user:
        return user

    admin_reset_properties = os.path.join(get_test_data_folder(), 'configuration', 'admin_reset.properties')
    with open(admin_reset_properties, 'w') as f:
        f.write(textwrap.dedent(f"""
                email = {ADMIN_USER_NAME}
                password = {ADMIN_PASSWORD}
            """))

    timeout = time.time()
    while True:
        if time.time() - timeout > 30:
            raise Exception(f'Timed out creating admin user {ADMIN_USER_NAME}')

        if get_user(ADMIN_USER_NAME):
            break

        time.sleep(0.01)


def set_sdl_datasource_manage_permissions(*, manage: bool):
    # Ensure we are logged in as non-admin
    login(admin=False)
    users_api = UsersApi(get_client())

    non_admin_id = users_api.get_me().id

    # Log in as admin
    login(admin=True)
    user_groups_api = UserGroupsApi(get_client())
    datasources_api = DatasourcesApi(get_client())
    items_api = ItemsApi(get_client())

    sdl_datasource_id = datasources_api.get_datasources(datasource_class=_common.DEFAULT_DATASOURCE_CLASS,
                                                        datasource_id=_common.DEFAULT_DATASOURCE_ID).datasources[0].id
    everyone_id = user_groups_api.get_user_groups(name_search='Everyone').items[0].id

    sdl_datasource_acl = items_api.get_access_control(id=sdl_datasource_id)
    for ace in sdl_datasource_acl.entries:  # type: AceOutputV1
        if ace.identity.id == everyone_id or ace.identity.id == non_admin_id:
            items_api.remove_access_control_entry(id=sdl_datasource_id, ace_id=ace.id)

    ace_input = AceInputV1()
    if manage:
        ace_input.identity_id = everyone_id
        rwm_permissions = PermissionsV1()
        rwm_permissions.read = True
        rwm_permissions.write = True
        rwm_permissions.manage = True
    else:
        ace_input.identity_id = non_admin_id
        rw_permissions = PermissionsV1()
        rw_permissions.read = True
        rw_permissions.write = True
        rw_permissions.manage = False
        ace_input.permissions = rw_permissions

    items_api.add_access_control_entry(id=sdl_datasource_id, body=ace_input)

    # We run tests as non-admin, so log back into non-admin
    login(admin=False)


def get_client():
    return _login.client


def get_test_data_folder():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'sq-run-data-dir'))


def wait_for(boolean_function):
    start = time.time()
    while True:
        if boolean_function():
            break

        if time.time() - start > 240:
            return False

        time.sleep(1.0)

    return True


def wait_for_example_data():
    if not wait_for(is_example_data_indexed):
        raise Exception("Timed out waiting for Example Data to finish indexing")


def is_example_data_indexed():
    # noinspection PyBroadException
    try:
        agents_api = AgentsApi(_login.client)
        agent_status = agents_api.get_agent_status()
        for agents in agent_status:
            if 'JVM Agent' in agents.id:
                if agents.status != 'CONNECTED':
                    return False

                for connection in agents.connections:
                    if 'Example Data' in connection.name and \
                            connection.status == 'CONNECTED' and \
                            connection.sync_status == 'SYNC_SUCCESS':
                        return True

    except BaseException:
        return False

    return False


def create_worksheet_for_url_tests():
    search_results = spy.search({
        'Name': 'Temperature',
        'Path': 'Example >> Cooling Tower 1 >> Area A'
    })

    display_items = pd.DataFrame([{
        'Type': 'Signal',
        'Name': 'Temperature Minus 5',
        'Formula': '$a - 5',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }, {
        'Type': 'Condition',
        'Name': 'Cold',
        'Formula': '$a.validValues().valueSearch(isLessThan(80))',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }, {
        'Type': 'Scalar',
        'Name': 'Constant',
        'Formula': '5',
    }])

    push_df = spy.push(metadata=display_items, workbook=None)

    workbook = Analysis({
        'Name': 'test_items_from_URL'
    })

    worksheet = workbook.worksheet('search from URL')
    worksheet.display_range = {
        'Start': '2019-01-01T00:00Z',
        'End': '2019-01-02T00:00Z'
    }
    worksheet.display_items = push_df

    spy.workbooks.push(workbook)

    return workbook


@pytest.mark.unit
def test_escape_regex():
    assert _common.escape_regex(r'mydata\trees') == r'mydata\\trees'
    assert _common.escape_regex(r'Hello There') == r'Hello There'
    assert _common.escape_regex(r'Hello\ There') == r'Hello\\ There'
    assert _common.escape_regex(r' Hello There ') == r' Hello There '
    assert _common.escape_regex('\\ Hello   There  \\') == '\\\\ Hello   There  \\\\'
    assert _common.escape_regex(r'\ Hello <>! There') == r'\\ Hello <>! There'


@pytest.mark.unit
def test_is_guid():
    assert _common.is_guid('2b17adfd-3308-4c03-bdfb-bf4419bf7b3a') is True
    assert _common.is_guid('test 2b17adfd-3308-4c03-bdfb-bf4419bf7b3a') is False
    assert _common.is_guid('2b17adfd-3308-4c03-bdfb-bf4419bf7b3a test') is False
    assert _common.is_guid('2G17adfd-3308-4c03-bdfb-bf4419bf7b3a') is False
    assert _common.is_guid('2b17adfd-3308-4c03-bdfb') is False
    assert _common.is_guid('Hello world') is False
    assert _common.is_guid('') is False
    assert _common.is_guid(123) is False


@pytest.mark.unit
def test_string_to_formula_literal():
    with pytest.raises(ValueError):
        _common.string_to_formula_literal(1)

    assert _common.string_to_formula_literal("mark") == "'mark'"
    assert _common.string_to_formula_literal("'''") == r"'\'\'\''"
    assert _common.string_to_formula_literal(r"\path\to\thing") == r"'\\path\\to\\thing'"
