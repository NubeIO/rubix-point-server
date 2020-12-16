DEFAULT="\033[0m"
GREEN="\033[32m"
RED="\033[31m"

USER=""
WORKING_DIR=""
LIB_DIR=""
SERVICE=nubeio-point-server.service
SERVICE_DIR=/lib/systemd/system
SERVICE_DIR_SOFT_LINK=/etc/systemd/system/multi-user.target.wants
DATA_DIR=/data/point-server
CONFIG_EXAMPLE=settings/config.example.ini
CONFIG=config.ini
LOGGING_EXAMPLE=logging/logging.example.conf
LOGGING=logging.conf
COMMAND=""

help() {
    echo "Service commands:"
    echo -e "   ${GREEN}install -u=<user> -dir=<working_dir> -lib_dir=<lib_dir>${DEFAULT} Install the service"
    echo -e "   ${GREEN}disable${DEFAULT}                                                 Disable the service"
    echo -e "   ${GREEN}enable${DEFAULT}                                                  Enable the service"
    echo -e "   ${GREEN}delete${DEFAULT}                                                  Delete the service"
    echo -e "   ${GREEN}restart${DEFAULT}                                                 Restart the service"
    echo
    echo "Service parameters:"
    echo -e "   ${GREEN}-h --help${DEFAULT}                                               Show this help"
    echo -e "   ${GREEN}-u --user=<user>${DEFAULT}                                        Which <user> is starting the service"
    echo -e "   ${GREEN}-dir --working-dir=<working_dir>${DEFAULT}                        Program root dir"
    echo -e "   ${GREEN}-dir --lib_dir-dir=<lib_dir>${DEFAULT}                            Python libs install dir"
}

install() {
    if [[ ${USER} != "" && ${WORKING_DIR} != "" && ${LIB_DIR} != "" ]]
    then
        echo -e "${GREEN}Creating System Service...${DEFAULT}"
        sudo cp systemd/${SERVICE} ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's/<user>/'"${USER}"'/' ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's,<working_dir>,'"${WORKING_DIR}"',' ${SERVICE_DIR}/${SERVICE}
        sed -i -e 's,<lib_dir>,'"${LIB_DIR}"',' ${SERVICE_DIR}/${SERVICE}

        # Create data_dir config.ini and logging.conf if not exist
        mkdir -p ${DATA_DIR}
        if [ ! -s ${DATA_DIR}/${CONFIG} ] ; then
            echo -e "${RED}${CONFIG} file doesn't exist or it is empty. ${GREEN}Creating${DEFAULT}"
            cp ${WORKING_DIR}/${CONFIG_EXAMPLE} ${DATA_DIR}/${CONFIG}
            sudo chmod -R +755 ${DATA_DIR}/${CONFIG}
        fi
        if [ ! -s ${DATA_DIR}/${LOGGING} ] ; then
            echo -e "${RED}${LOGGING} file doesn't exist or it is empty. ${GREEN}Creating${DEFAULT}"
            cp ${WORKING_DIR}/${LOGGING_EXAMPLE} ${DATA_DIR}/${LOGGING}
            sudo chmod -R +755 ${DATA_DIR}/${LOGGING}
        fi
        sudo chown -R ${USER}:${USER} ${DATA_DIR}

        echo -e "${GREEN}Installing requirements in ${LIB_DIR}...${DEFAULT}"
        source ${LIB_DIR}/venv/bin/activate
        pip install -r requirements.txt
        deactivate

        echo -e "${GREEN}Soft Un-linking System Service...${DEFAULT}"
        sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE}

        echo -e "${GREEN}Soft Linking System Service...${DEFAULT}"
        sudo ln -s ${SERVICE_DIR}/${SERVICE} ${SERVICE_DIR_SOFT_LINK}/${SERVICE}

        echo -e "${GREEN}Enabling System Service...${DEFAULT}"
        sudo systemctl daemon-reload
        sudo systemctl enable ${SERVICE}

        echo -e "${GREEN}Starting System Service...${DEFAULT}"
        sudo systemctl restart ${SERVICE}

        echo -e "${GREEN}Service is created and started.${DEFAULT}"
    else
        echo -e ${RED}"-u=<user> -dir=<working_dir> -lib_dir=<lib_dir> these parameters should be on you input (-h, --help for help)${DEFAULT}"
    fi
}

disable() {
    echo -e "${GREEN}Stopping System Service...${DEFAULT}"
    sudo systemctl stop ${SERVICE}
    echo -e "${GREEN}Disabling System Service...${DEFAULT}"
    sudo systemctl disable ${SERVICE}
    echo -e "${GREEN}Service is disabled.${DEFAULT}"
}

enable() {
    echo -e "${GREEN}Enabling System Service...${DEFAULT}"
    sudo systemctl enable ${SERVICE}
    echo -e "${GREEN}Starting System Service...${DEFAULT}"
    sudo systemctl start ${SERVICE}
    echo -e "${GREEN}Service is enabled.${DEFAULT}"
}

delete() {
    echo -e "${GREEN}Stopping System Service...${DEFAULT}"
    sudo systemctl stop ${SERVICE}
    echo -e "${GREEN}Un-linking System Service...${DEFAULT}"
    sudo unlink ${SERVICE_DIR_SOFT_LINK}/${SERVICE}
    echo -e "${GREEN}Removing System Service...${DEFAULT}"
    sudo rm -r ${SERVICE_DIR}/${SERVICE}
    echo -e "${GREEN}Hitting daemon-reload...${DEFAULT}"
    sudo systemctl daemon-reload
    echo -e "${GREEN}Service is deleted.${DEFAULT}"
}

restart() {
    echo -e "${GREEN}Restarting System Service...${DEFAULT}"
    sudo systemctl restart ${SERVICE}
    echo -e "${GREEN}Service is restarted.${DEFAULT}"
}

parseCommand() {
    for i in "$@"
    do
    case ${i} in
    -h|--help)
        help
        exit 0
        ;;
    -u=*|--user=*)
        USER="${i#*=}"
        ;;
    -dir=*|--working-dir=*)
        WORKING_DIR="${i#*=}"
        ;;
    -lib_dir=*)
        LIB_DIR="${i#*=}"
        ;;
    install|start|disable|enable|delete|restart)
        COMMAND=${i}
        ;;
    *)
        echo -e "${RED}Unknown option (-h, --help for help)${DEFAULT}"
        exit 1
        ;;
    esac
    done
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