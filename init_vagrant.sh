PROJ_ROOT_DIR=/vagrant
VAGRANT_HOME=/home/vagrant
VIRTUAL_ENV_DIR=${VAGRANT_HOME}/venv
MANAGEMENT_COMMANDS_PREFIX="python ${PROJ_ROOT_DIR}/manage.py"
VAGRANT_BASH=${VAGRANT_HOME}/.bashrc
DEV_PACKAGES=(
  "python3-pip"
  "python3-virtualenv"
  "libmysqlclient-dev"
)

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y
apt-get install -y ${DEV_PACKAGES[*]}
sudo -u vagrant virtualenv -p /usr/bin/python3 ${VIRTUAL_ENV_DIR}
${VIRTUAL_ENV_DIR}/bin/pip install -r ${PROJ_ROOT_DIR}/requirements.txt

echo "alias runserver=\"${MANAGEMENT_COMMANDS_PREFIX} runserver 0.0.0.0:8000\"" >>${VAGRANT_BASH}
echo "alias makemigrations=\"${MANAGEMENT_COMMANDS_PREFIX} makemigrations\"" >>${VAGRANT_BASH}
echo "alias migrate=\"${MANAGEMENT_COMMANDS_PREFIX} migrate\"" >>${VAGRANT_BASH}

echo "cd ${PROJ_ROOT_DIR}" >>${VAGRANT_BASH}
echo "source ${VIRTUAL_ENV_DIR}/bin/activate" >>${VAGRANT_BASH}
