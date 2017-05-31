#!/usr/bin/env python2

DOCUMENTATION = '''
---
module: yaourt
auth:
    - "Will Price"
short_description: Install packages from the Arch Linux repositories and AUR
description:
    - Manages packages installable from I(yaourt).
options:
    name:
        required: true
        description:
            - Name of any package in the Arch Linux repositories or AUR
    state:
        required: false
        default: "present"
        choices: ["present", "latest", "absent"]
    update_cache:
        required: false
        default: "no"
        choices: ["yes, "no"]
'''

EXAMPLES = '''

# Install package "git"
- yaourt: name=git

# Update cache and install package "git"
- yaourt: name=git update_cache=yes

# Remove "git" package if it is installed
- yaourt: name=git state=absent

# Update cache and install "git" if it isn't present, if it is, update it if
# possible
- yaourt: name=git state=latest update_cache=yes
'''

RETURN = '''
stdout:
    description: output from yaourt
    returned: success, when needed
    type: string           # This pa
    sample: ""
stderr:
    description: error output from yaourt
    returned: success, when needed
    type: string
    sample: ""
'''


class Yaourt(object):
    def __init__(self, module, path):
        self.module = module
        self.path = path

    def run(self, pkgs, state='present', update_cache=False):
        for pkg in pkgs:
            if update_cache:
                self._update_cache()
            isInstalled = self.query_package(pkg)
            if state == 'present' and not isInstalled:
                self._install(pkg)
            else:
                self._run_yaourt_command(['-R', '--noconfirm', pkg])

    def query_package(self, pkg):
        exit_status, _, _ = self._run_yaourt_command(['-Qi', pkg])
        return (exit_status == 0)

    def _install(self, pkg):
        self._run_yaourt_command(['-S', '--noconfirm', pkg])

    def _update_cache(self):
        self._run_yaourt_command(['-Su'])

    def _run_yaourt_command(self, args):
        return self.module.run_command([self.path] + args)


def main():
    pass

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
