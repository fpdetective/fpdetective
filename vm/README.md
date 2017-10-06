You can follow these instructions to set up a VM and use FPDetective independently of the configuration of your operating system:

1. Install the latest version of [Vagrant](http://www.vagrantup.com/) (tested on 1.3.5)
2. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (it's important that this version matches version of Guest Additions installed in Box - currently 4.2)
3. Download (clone) fpdetective if you haven't done yet:
```
git clone https://github.com/fpdetective/fpdetective.git
```
4. Change the working directory to `vm/GUI` or `vm/noGUI` depending on whether you want 
to run VM with desktop environment (GUI) or SSH (noGUI).
5. Run `vagrant up` and wait until the bootstrap script finishes. 
In the first run this will download VM image (~1.5GB) and all necessary binaries 
which may take several minutes.
6. If you're using GUI-less mode, run `vagrant ssh` to SSH into VM and start using FPDetective.

### VM-only use
In case you want to use FPDetective only with the VM, you don't need to clone the whole repository. 
Just check out the `vm` subdirectory by running the following command:
`svn checkout https://github.com/fpdetective/fpdetective/trunk/vm vm`

### Credentials
Virtual Machine
* username = `vagrant` 
* password = `vagrant`

MySQL Database
* username = `root` 
* password = `fpdetective`

Some points that can help you to use this marvellous crawler with GUI,
* Run setup.sh at first. It will install all the reqired libraries and also create run folder.
* If you don't have casperjs installed, you have to do it manually.
* if src/crawler/mitm.py gives some error, install mitmproxy and libmproxy with mitmproxy.
