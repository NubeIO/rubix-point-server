import enum


class DropletType(enum.Enum):
    """
    cloud: it is created for those whose values will get sync from third party
    edge: it is created for those whose values will be sync from the edge rubix_point_server
    """
    CLOUD = 'cloud'
    EDGE = 'edge'
