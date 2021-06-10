Feature: Release GitHub Action
  A GitHub action for finishing a release.

  Scenario Outline: Test the Build Docker Image Against a Number of Scenarios
    Given the scenario <scenario_name>
    When the docker container is executed
    Then assert the exit code is <exit_code>
    Examples:
      | scenario_name | exit_code |
      | not_a_git_dir | 1         |
      | no_setup_file | 1         |
      | 0.1.0         | 1         |
      | 0.2.0         | 0         |
