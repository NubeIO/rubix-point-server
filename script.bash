DEFAULT="\033[0m"
GREEN="\033[32m"
RED="\033[31m"

COMMAND=""
SERVICE_NAME="nubeio-point-server.service"
USER=""
WORKING_DIR=""
LIB_DIR=""
DATA_DIR=/data/point-server
PORT=1515

DATA_DIR_EDITED=false
SERVICE_NAME_EDITED=false
PORT_EDITED=false

SERVICE_DIR=/lib/systemd/system
SERVICE_DIR_SOFT_LINK=/etc/systemd/system/multi-user.target.wants
SERVICE_TEMPLATE=systemd/nubeio-point-server.template.service

CONFIG_EXAMPLE=settings/config.example.ini
CONFIG=config.ini

LOGGING_EXAMPLE=logging/logging.example.conf
LOGGING=logging/logging.conf

createDirIfNotExist() {
    mkdir -p ${DATA_DIR}
    sudo chown -R ${USER}:${USER} ${DATA_DIR}
}

copyConfigurationIfNotExist() {
    if [ ! -s ${DATA_DIR}/${CONFIG} ]; then
        echo -e "${RED}${CONFIG} file doesn't exist or it is empty. ${GREEN}Creating${DEFAULT}"
        cp ${WORKING_DIR}/${CONFIG_EXAMPLE} ${DATA_DIR}/${CONFIG}
        sudo chmod -R +755 ${DATA_DIR}/${CONFIG}
    fi
}

copyLoggingIfNotExist() {
    if [ ! -s ${DATA_DIR}/${LOGGING} ]; then
        echo -e "${RED}${LOGGING} file doesn't exist or it is empty. ${GREEN}Creating${DEFAULT}"
        cp ${WORKING_DIR}/${LOGGING_EXAMPLE} ${DATA_DIR}/${LOGGING}
        sudo chmod -R +755 ${DATA_DIR}/${LOGGING}
    fi
}

installPythonRequirements() {
  echo -e "${GREEN}Installing requirements in ${LIB_DIR}...${DEFAULT}"
  source ${LIB_DIR}/venv/bin/activate
  pip install -r requirements.txt
  deactivate
}

showServiceNameWarningIfNotEdited() {
    if [ ${SERVICE_NAME_EDITED} == false ]; then
        echo -e "${RED}We are using default service_name=${SERVICE_NAME}!${DEFAULT}"
    fi
}

showWarningIfNotEdited() {
    showServiceNameWarningIfNotEdited
    if [ ${DATA_DIR_EDITED} == false ]; then
        echo -e "${RED}We are using default data_dir=${DATA_DIR}!${DEFAULT}"
    fi
    if [ ${PORT_EDITED} == false ]; then
        echo -e "${RED}We are using default port=${PORT}!${DEFAULT}"
    fi
}

createLinuxService() {
    echo -e "${GREEN}Creating Linux Service...${SERVICE_NAME}"
    sudo cp ${SERVICE_TEMPLATE} ${SERVICE_DIR}/${SERVICE_NAME}
    sed -i -e 's/<user>/'"${USER}"'/' ${SERVICE_DIR}/${SERVICE_NAME}
    sed -i -e 's,<working_dir>,'"${WORKING_DIR}"',' ${SERVICE_DIR}/${SERVICE_NAME}
    sed -i -e 's,<lib_dir>,'"${LIB_DIR}"',' ${SERVICE_DIR}/${SERVICE_NAME}
    sed -i -e 's,<data_dir>,'"${DATA_DIR}"',' ${SERVICE_DIR}/${SERVICE_NAME}
    sed -i -e 's/<port>/'"${PORT}"'/' ${SERVICE_DIR}/${SERVICE_NAME}
}

startNewLinuxService() {
    echo -e "${GREEN}Soft Un-linking Linux Service...${DEFAULT}"
    sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE_NAME}

    echo -e "${GREEN}Soft Linking Linux Service...${DEFAULT}"
    sudo ln -s ${SERVICE_DIR}/${SERVICE} ${SERVICE_DIR_SOFT_LINK}/${SERVICE_NAME}

    echo -e "${GREEN}Hitting daemon-reload...${DEFAULT}"
    sudo systemctl daemon-reload

    echo -e "${GREEN}Enabling Linux Service...${DEFAULT}"
    sudo systemctl enable ${SERVICE_NAME}

    echo -e "${GREEN}Starting Linux Service...${DEFAULT}"
    sudo systemctl restart ${SERVICE_NAME}
}

install() {
    if [[ ${USER} != "" && ${WORKING_DIR} != "" && ${LIB_DIR} != "" ]]; then
        createDirIfNotExist
        copyConfigurationIfNotExist
        installPythonRequirements
        createLinuxService
        startNewLinuxService
        echo -e "${GREEN}Service is created and started.${DEFAULT}"
    else
        echo -e ${RED}"-u=<user> -dir=<working_dir> -lib_dir=<lib_dir> these parameters should be on you input (-h, --help for help)${DEFAULT}"
    fi
}

disable() {
    showServiceNameWarningIfNotEdited
    echo -e "${GREEN}Stopping Linux Service...${DEFAULT}"
    sudo systemctl stop ${SERVICE_NAME}
    echo -e "${GREEN}Disabling Linux Service...${DEFAULT}"
    sudo systemctl disable ${SERVICE_NAME}
    echo -e "${GREEN}Service is disabled.${DEFAULT}"
}

enable() {
    showServiceNameWarningIfNotEdited
    echo -e "${GREEN}Enabling Linux Service...${DEFAULT}"
    sudo systemctl enable ${SERVICE_NAME}
    echo -e "${GREEN}Starting Linux Service...${DEFAULT}"
    sudo systemctl start ${SERVICE_NAME}
    echo -e "${GREEN}Service is enabled.${DEFAULT}"
}

delete() {
    showServiceNameWarningIfNotEdited
    echo -e "${GREEN}Stopping Linux Service...${DEFAULT}"
    sudo systemctl stop ${SERVICE_NAME}
    echo -e "${GREEN}Un-linking Linux Service...${DEFAULT}"
    sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE_NAME}
    echo -e "${GREEN}Removing Linux Service...${DEFAULT}"
    sudo rm -r ${SERVICE_DIR}/${SERVICE_NAME}
    echo -e "${GREEN}Hitting daemon-reload...${DEFAULT}"
    sudo systemctl daemon-reload
    echo -e "${GREEN}Service is deleted.${DEFAULT}"
    # TODO: remove other data and requirements
}

restart() {
    showServiceNameWarningIfNotEdited
    echo -e "${GREEN}Restarting Linux Service...${DEFAULT}"
    sudo systemctl restart ${SERVICE_NAME}
    echo -e "${GREEN}Service is restarted.${DEFAULT}"
}

parseCommand() {
    for i in "$@"; do
        case ${i} in
        -h | --help)
            help
            exit 0
            ;;
        --service-name=*)
            SERVICE_NAME="${i#*=}"
            SERVICE_NAME_EDITED=true
            ;;
        -u=* | --user=*)
            USER="${i#*=}"
            ;;
        -d | --dir=* | --working-dir=*)
            WORKING_DIR="${i#*=}"
            ;;
        --lib-dir=*)
            LIB_DIR="${i#*=}"
            ;;
        --data-dir=*)
            DATA_DIR="${i#*=}"
            DATA_DIR_EDITED=true
            ;;
        -p=* | --port=*)
            PORT="${i#*=}"
            PORT_EDITED=true
            ;;
        install | start | disable | enable | delete | restart)
            COMMAND=${i}
            ;;
        *)
            echo -e "${RED}Unknown options ${i}  (-h, --help for help)${DEFAULT}"
            ;;
        esac
    done
}

help() {
    echo "Service commands:"
    echo -e "   ${GREEN}install --service-name=<service_name> -u=<user> --dir=<working_dir> --lib-dir=<lib_dir> --data-dir=<data_dir>${DEFAULT}         Install and start the service"
    echo -e "   ${GREEN}disable${DEFAULT}                                                                                                               Disable the service"
    echo -e "   ${GREEN}enable${DEFAULT}                                                                                                                Enable the service"
    echo -e "   ${GREEN}delete${DEFAULT}                                                                                                                Delete the service"
    echo -e "   ${GREEN}restart${DEFAULT}                                                                                                               Restart the service"
    echo
    echo "Service parameters:"
    echo -e "   ${GREEN}-h --help${DEFAULT}                                                                                                             Show this help"
    echo -e "   ${GREEN}-u --user=<user>${DEFAULT}                                                                                                      Which <user> is starting the service"
    echo -e "   ${GREEN}--dir --working-dir=<working_dir>${DEFAULT}                                                                                     Project dir"
    echo -e "   ${GREEN}--lib-dir=<lib_dir>${DEFAULT}                                                                                                   Python requirements lib dir"
    echo -e "   ${GREEN}--data-dir=<lib_dir>${DEFAULT}                                                                                                  Config dir"
}

runCommand() {
    case ${COMMAND} in
    install)
        install
        ;;
    start) # for backward compatibility
        install
        ;;
    disable)
        disable
        ;;
    enable)
        enable
        ;;
    delete)
        delete
        ;;
    restart)
        restart
        ;;
    esac
}

parseCommand "$@"
runCommand
exit 0
