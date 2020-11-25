from flask_restful import Resource


def get_current_memory_usage():
    """ Memory usage in kB """
    with open('/proc/self/status') as f:
        mem_usage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    return int(mem_usage.strip())


class GetSystemMem(Resource):
    def get(self):
        mem = get_current_memory_usage()
        return {'networks': mem}
