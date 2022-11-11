#!/usr/bin/env python
"""
Check the version poetry is building matches the version from `GITHUB_REF` environment variable.
"""
import os
import re
import subprocess
import sys


def main() -> int:
    version_ref = os.getenv('GITHUB_REF')
    if version_ref:
        version = re.sub('^refs/tags/v*', '', version_ref.lower())
    else:
        exit('✖ "GITHUB_REF" env variables not found')

    project_version = subprocess.check_output(['poetry', 'version', '--short'], encoding='utf-8').strip()

    if project_version == version:
        print(f'✓ GITHUB_REF matches version {project_version!r}')
        return 0
    else:
        print(f'✖ GITHUB_REF version {version!r} does not poetry version {project_version!r}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
