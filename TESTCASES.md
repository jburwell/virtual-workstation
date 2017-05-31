packer pkg=git state=present

pacman -Qi git
    no:
        yaourt -S --noconfirm git
    yes:
        pass

packer pkg=git state=present update_cache=yes

yaourt -Su
pacman -Qi git
    no:
        yaourt -S --noconfirm git
    yes:
        pass


packer pkg=git state=absent

pacman -Qi git
    no:
        pass
    yes:
        pacman -R git


packer pkg=['git', 'nano'] state=present

pacman -Qi git
pacman -Qi nano
get list of targets to install
if len(targets.not_installed) > 0:
    yaourt -S *targets


packer pkg=['git', 'nano'] state=present update_cache=yes

yaourt -Su
pacman -Qi git
pacman -Qi nano
get map of targets to package status
if len(targets.not_installed) > 0:
    yaourt -S *targets

packer pkg=['git', 'nano'] state=absent

pacman -Qi git
pacman -Qi nano
get map of targets to package status
if len(targets.installed) > 0:
    yaourt -S *targets
