"""
解析数据 models对象
"""
from .models import EnumInstanceType, Instance, EnumAction, Event, EnumCloud
from dateutil.parser import parse


def utc_datetime_str_to_ts(datetime_str):
    return int(parse(datetime_str).timestamp())


def instance_detail_parser(data, instance_type: EnumInstanceType) -> Instance:
    """
    实例解析,对应一台主机/一台数据库/


    {
        'resourceType': 'compute',
        'resourceName': 'aws-sg-xx-xx-xxx-01',
        'resourceId': 'i-0xx664f73e8689',
        'privateIp': '10.xx.20.91',
        'createdAt': 1635911824,
        'tree': [{'nodeId': 17, 'name': '业务线/二级部门/应用'}],
        'accountId': 17,
        'accountName': 'aws-sg',
        'region': 'ap-southeast-1',
        'cloud': 'aws'
    }

    """

    pk = data['resourceId']
    _cloud = data['cloud']

    if data.get('tree', []):
        try:
            node_id = data['tree'][0]['nodeId']
            node_name = data['tree'][0]['name']
        except:
            node_id = None
            node_name = ''
    else:
        node_id = None
        node_name = ''

    if _cloud == 'huawei':
        cloud = EnumCloud.huawei
    elif _cloud == 'qcloud':
        cloud = EnumCloud.tencent
    elif _cloud == 'aws':
        cloud = EnumCloud.aws
    elif _cloud == 'aliyun':
        cloud = EnumCloud.aliyun
    else:
        cloud = EnumCloud.default

    region = data['region']

    return Instance(private_id=pk, cloud=cloud, region=region, instance_type=instance_type, node_id=node_id,
                    node_name=node_name)


def event_parser(event_data: dict, instance_obj: Instance) -> Event:
    """
    事件解析 数据由list_instance_event提供
     {
        "id":"内部事件id",
        "action":"开机",
        "opTime":"2021-10-03T03:18:15Z",
        "operateOn":"服务器",
        "createdAt":"2021-10-03T03:18:15.555Z",
        "userName":"xxx"
    }
    """
    action_map = {
        '开机': EnumAction.start,
        '调整配置': EnumAction.update,
        '关机': EnumAction.stop,
        '创建': EnumAction.create,
        'stop': EnumAction.stop,
        '回收': EnumAction.delete
    }
    event_id = event_data['id']

    action = action_map.get(event_data['action'], 0)
    event_ts = utc_datetime_str_to_ts(event_data['opTime'])

    instance_obj = instance_obj
    event_obj = Event(event_id=event_id, action=action, event_ts=event_ts, instance=instance_obj)

    return event_obj
