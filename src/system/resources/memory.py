from rubix_http.resource import RubixResource


def get_current_memory_usage():
    """ Memory usage in kB """
    with open('/proc/self/status') as f:
        mem_usage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    return int(mem_usage.strip())


class GetSystemMem(RubixResource):
    @classmethod
    def get(cls):
        mem = get_current_memory_usage()
        return {'networks': mem}
