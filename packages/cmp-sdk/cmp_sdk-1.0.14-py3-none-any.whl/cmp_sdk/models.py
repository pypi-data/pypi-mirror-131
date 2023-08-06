from enum import Enum, unique


@unique
class EnumAction(Enum):
    # 操作动作
    create = 1
    delete = 2
    stop = 3
    start = 4
    restart = 5
    update = 6


@unique
class EnumInstanceType(Enum):
    # 资源类型
    host = 1
    mysql = 2
    mongo = 3
    redis = 4
    kafka = 5


@unique
class EnumCloud(Enum):
    # 资源类型
    ucloud = 1
    huawei = 2
    aliyun = 3
    aws = 4
    tencent = 5
    default = 0


class Instance:
    # 实例,如一台主机，一个mysql，一个redis。。。
    private_id = None
    cloud = None
    instance_type = None
    region = None
    zone = None

    def __init__(self, private_id, cloud: EnumCloud, instance_type: EnumInstanceType, region: str = None, node_id=None,
                 node_name=None):
        self.private_id = private_id
        self.cloud = cloud
        self.instance_type = instance_type
        self.region = region
        self.node_id = node_id
        self.node_name = node_name


class NoExistInstance(Instance):
    def __init__(self, **kwargs):
        pass


class Event:
    # 事件，描述某个人对某个实例做了什么
    def __init__(self, event_id: str, action: str, event_ts: int, instance: Instance,
                 opt_username: str = ''):
        self.action = action
        self.event_ts = event_ts
        self.instance = Instance
        self.action = action
        self.event_id = event_id
        self.instance = instance

    @property
    def instance_type(self):
        return self.instance.instance_type
