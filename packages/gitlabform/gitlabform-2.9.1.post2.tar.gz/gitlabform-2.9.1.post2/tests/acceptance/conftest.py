import pytest

from tests.acceptance import (
    get_gitlab,
    create_group,
    create_groups,
    delete_groups,
    create_project,
    get_random_name,
    create_users,
    delete_users,
)


@pytest.fixture(scope="session")
def gitlab():
    gl = get_gitlab()
    yield gl  # provide fixture value


@pytest.fixture(scope="class")
def group_and_project(group, project):
    return f"{group}/{project}"


@pytest.fixture(scope="class")
def group():
    group_name = get_random_name()
    create_group(group_name)

    yield group_name

    gl = get_gitlab()
    gl.delete_group(group_name)


@pytest.fixture(scope="class")
def other_group():
    # TODO: deduplicate this - it's a copy and paste from the above fixture
    group_name = get_random_name()
    create_group(group_name)

    yield group_name

    gl = get_gitlab()
    gl.delete_group(group_name)


@pytest.fixture(scope="class")
def sub_group(group):
    gl = get_gitlab()
    parent_id = gl.get_group_id_case_insensitive(group)
    group_name = get_random_name()
    create_group(group_name, parent_id)

    yield group + "/" + group_name

    gl = get_gitlab()
    gl.delete_group(group + "/" + group_name)


@pytest.fixture(scope="class")
def project(group):
    project_name = get_random_name()
    create_project(group, project_name)

    yield project_name

    gl = get_gitlab()
    gl.delete_project(f"{group}/{project_name}")


@pytest.fixture(scope="class")
def other_project(group):
    # TODO: deduplicate this - it's a copy and paste from the above fixture
    project_name = get_random_name()
    create_project(group, project_name)

    yield project_name

    gl = get_gitlab()
    gl.delete_project(f"{group}/{project_name}")


@pytest.fixture(scope="class")
def groups(users):
    no_of_groups = 4

    group_name_base = get_random_name()
    groups = create_groups(group_name_base, no_of_groups)

    yield groups

    delete_groups(group_name_base, no_of_groups)


@pytest.fixture(scope="class")
def users(group):
    no_of_users = 4

    username_base = get_random_name()
    users = create_users(username_base, no_of_users)

    yield users

    delete_users(username_base, no_of_users)


@pytest.fixture(scope="class")
def other_users():
    # TODO: deduplicate this - it's a copy and paste from the above fixture
    no_of_users = 4

    username_base = get_random_name()
    users = create_users(username_base, no_of_users)

    yield users

    delete_users(username_base, no_of_users)
