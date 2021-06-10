# coding=utf-8
"""Release GitHub Action feature tests."""
import docker
import logging
import os
import shutil

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
from git import Repo

client = docker.from_env()
logging.basicConfig(level=logging.DEBUG)


@scenario('../features/release-action.feature', 'Test the Build Docker Image Against a Number of Scenarios')
def test_test_the_build_docker_image_against_a_number_of_scenarios():
    """Test the Build Docker Image Against a Number of Scenarios."""


@given('the scenario <scenario_name>', target_fixture='container_run')
def the_scenario_scenario_name(scenario_name):
    """the scenario <scenario_name>."""
    return {
        'scenario_name': scenario_name
    }


@when('the docker container is executed')
def the_docker_container_is_executed(container_run):
    """the docker container is executed."""
    scenario_name = container_run['scenario_name']
    directory_name = f'/var/tmp/scenario_{scenario_name}'
    logging.debug(f'scenario: {scenario_name}')

    try:
        shutil.rmtree(directory_name, ignore_errors=True)
    except FileNotFoundError:
        pass

    os.mkdir(directory_name)

    if scenario_name != 'not_a_git_dir':
        repo = Repo.init(directory_name)

    if scenario_name == 'not_a_git_dir':
        pass
    elif scenario_name == 'no_setup_file':
        with open(f'{directory_name}/foo.txt', 'wb') as f:
            f.write(b'foo')
        repo.index.add(repo.untracked_files)
        repo.index.commit('Initial commit.')
    elif scenario_name == '0.1.0':
        lines = ['[gitchangelog]\n', 'unreleased_version_label = 0.1.0']
        with open(f'{directory_name}/setup.cfg', 'w') as f:
            f.writelines(lines)

        repo.index.add(repo.untracked_files)
        repo.index.commit('Initial commit.')
        repo.create_tag('0.1.0')
    elif scenario_name == '0.2.0':
        lines = ['[gitchangelog]\n', 'unreleased_version_label = 0.2.0']
        with open(f'{directory_name}/setup.cfg', 'w') as f:
            f.writelines(lines)

        repo.index.add(repo.untracked_files)
        repo.index.commit('Initial commit.')

    container_run['directory_name'] = directory_name


@then('assert the exit code is <exit_code>')
def assert_the_exit_code_is_exit_code(container_run, exit_code):
    """assert the exit code is <exit_code>."""
    exit_code = int(exit_code)
    directory_name = container_run['directory_name']
    volumes = {
        directory_name: {
            'bind': '/mnt',
            'mode': 'rw'
        }
    }

    try:
        container = client.containers.run('release-action:latest', stderr=True, volumes=volumes)
        rc = 0
    except docker.errors.ContainerError:
        rc = 1

    try:
        message = container
    except NameError:
        message = f'Unexpected return code ({rc}) instead of {exit_code}.'

    assert rc == exit_code, message
