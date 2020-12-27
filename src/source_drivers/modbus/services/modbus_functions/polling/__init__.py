modbus_poll_debug_log = 'modbus_poll_debug'


def modbus_poll_debug(logger, msg):
    logger.debug(f'MODBUS DEBUG: {msg}')
