---------------------------------
Instructions for setting up VM
---------------------------------
1. Install the latest version of Vagrant
2. Install VirtualBox (version should match that of Guest Additions installed in the box - currently 4.2)
3. Change directory to `vm/gui` to use the VM with GUI or `vm/nogui` to use it over SSH.
4. Run `vagrant up` in this folder and wait until the bootstrap script is finished.
5. In case you're using the GUI-less mode, you can run `vagrant ssh` in order to SSH to VM and start using FPDetective.

Only checkout VM
---------------------------------
In case you only want to use the VM, you can just checkout this part of the repository by
   `svn checkout https://github.com/fpdetective/fpdetective/trunk/vm vm`

Credentials
---------------------------------
VM session: username = vagrant password = vagrant
DB: username = root password = fpdetective
