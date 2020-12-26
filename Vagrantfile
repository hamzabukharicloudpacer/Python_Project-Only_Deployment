# All Vagrant configuration is done below.

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/focal64"

  config.vm.network "forwarded_port", guest: 8000, host: 8080

  config.vm.provision "shell", path: "init_vagrant.sh"

end
