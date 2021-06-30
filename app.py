import os
from distutils.dist import Distribution
from git import Repo

ignore_regexps = [
    r'@minor', r'!minor',
    r'@cosmetic', r'!cosmetic',
    r'@refactor', r'!refactor',
    r'@wip', r'!wip',
    r'^([cC]hg|[fF]ix|[nN]ew)\s*:\s*[p|P]kg:',
    r'^([cC]hg|[fF]ix|[nN]ew)\s*:\s*[d|D]ev:',
    r'^(.{3,3}\s*:)?\s*[fF]irst commit.?\s*$',
    r'^$',  # ignore commits with empty messages
]

section_regexps = [
    ('New', [
        r'^[nN]ew\s*:\s*((dev|use?r|pkg|test|doc)\s*:\s*)?([^\n]*)$',
    ]),
    ('Changes', [
        r'^[cC]hg\s*:\s*((dev|use?r|pkg|test|doc)\s*:\s*)?([^\n]*)$',
    ]),
    ('Fix', [
        r'^[fF]ix\s*:\s*((dev|use?r|pkg|test|doc)\s*:\s*)?([^\n]*)$',
    ]),

    ('Other', None  # Match all lines
     ),

]

subject_process = (strip |
                   ReSub(r'^([cC]hg|[fF]ix|[nN]ew)\s*:\s*((dev|use?r|pkg|test|doc)\s*:\s*)?([^\n@]*)(@[a-z]+\s+)*$',
                         r'\4') |
                   SetIfEmpty('No commit message.') | ucfirst | final_dot)

tag_filter_regexp = r'^[0-9]+\.[0-9]+(\.[0-9]+)?$'

dist = Distribution()
dist.parse_config_files()
unreleased_version_label = dist.get_option_dict('gitchangelog')
unreleased_version_label = unreleased_version_label['unreleased_version_label']
_, unreleased_version_label = unreleased_version_label
repo = Repo('.')
print(f'INFO: Existing tags are {repo.tags}.')

if 'CI' in os.environ and os.environ['CI'] == 'true':
    print(f'INFO: unreleased_version_label is {unreleased_version_label}.')
    print(f'INFO: GITHUB_EVENT_NAME is {os.environ["GITHUB_EVENT_NAME"]}.')
    print(f'INFO: GITHUB_REF is {os.environ["GITHUB_REF"]}.')
    target_tag_exists = False

    for tag in repo.tags:
        if tag.name == unreleased_version_label:
            target_tag_exists = True
            break

    if os.environ['GITHUB_EVENT_NAME'] == 'pull_request':
        print(f'INFO: target tag exists {target_tag_exists}.')
        assert not target_tag_exists, f'Tag {unreleased_version_label} already exists.'


output_engine = mustache('markdown')

include_merge = False

revs = []
