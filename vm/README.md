You can follow these instructions to set up a VM and use FPDetective independently of the configuration of your operating system:

1. Install the latest version of [Vagrant](http://www.vagrantup.com/) (tested on 1.3.5)
2. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (it's important that this version matches version of Guest Additions installed in Box - currently 4.2)
3. Change the working directory to `GUI` or `noGUI` depending on whether you want to run the VM with GUI or via SSH.
4. Run `vagrant up` in this folder and wait until the bootstrap script finishes. In the first run this will download VM image (~1.5GB) which may take several minutes depending on your connection
5. If you're using GUI-less mode, run `vagrant ssh` to SSH into VM and start using FPDetective.

### VM-only use
In case you want to use FPDetective only with the VM, you don't need to clone the project. Just check out the `vm` subdirectory:
`svn checkout https://github.com/fpdetective/fpdetective/trunk/vm vm`

### Credentials
Virtual Machine
* username = `vagrant` 
* password = `vagrant`

MySQL Database
* username = `root` 
* password = `fpdetective`
