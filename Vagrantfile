# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "wholebits/archlinux"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "vmware_fusion" do |v|
    v.gui = true
    v.vmx["ethernet0.pcislotnumber"] = "192"
    v.vmx["ethernet0.virtualDev"] = "vmxnet3"
  end

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true

    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end

  # Update the box to the latest package revisions
  config.vm.provision "shell", inline: <<-SHELL
    mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.orig
    grep -A 1 "United States" /etc/pacman.d/mirrorlist.orig > /etc/pacman.d/mirrorlist.usa
    rankmirrors -n 6 /etc/pacman.d/mirrorlist.usa > /etc/pacman.d/mirrorlist

    pacman -Suy --noconfirm
  SHELL

  # Reboot in the event that GRUB or the kernel where updated
  config.vm.provision "reload"

  # Install the dependencies required for Ansible
  config.vm.provision "shell", inline: <<-SHELL
    pacman -S python2 python2-pip --noconfirm

    function make_symlink() {
      if [ ! -h "$2" ] && [ ! -e "$2" ]; then
        ln -s $1 $2
     fi
    }

    make_symlink "/usr/bin/python2" "/usr/bin/python"
    make_symlink "/usr/bin/python2-config" "/usr/bin/python-config"
  SHELL

  # Install X and i3 ...
  config.vm.provision "ansible" do |ansible|
    ansible.galaxy_role_file = "playbooks/requirements.yml"
    ansible.galaxy_roles_path = "playbooks/.galaxy-roles"
    ansible.playbook = "playbooks/xwindows-i3.yml"
  end

end
