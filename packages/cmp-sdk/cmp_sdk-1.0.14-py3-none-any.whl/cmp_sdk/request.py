import time
import requests as http_requests
from .models import Instance, Event, NoExistInstance, EnumInstanceType
from .parser import instance_detail_parser, event_parser
from .logger import logger
from .const import SERVER, AUTH_PASSWORD, AUTH_NAME, CRED_TTL, COMPANY_ID, DRY_RUN

from functools import wraps


def dry_run_patch(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):

        if DRY_RUN:
            try:
                method(self, *method_args, **method_kwargs)
            except Exception as e:
                logger.warn(f'ignore method {self} {e}')
            return None, True
        else:
            return method(self, *method_args, **method_kwargs), False

    return _impl


class RequestServerError(Exception):
    pass


class RequestConnError(Exception):
    pass


class ResponseError(Exception):
    def __init__(self, message, error_resp):
        self.error_resp = error_resp
        self.message = message
        super().__init__(self.message)


class CredObject:
    def __init__(self, token, cookie):
        self.token = token
        self.cookie = cookie
        self._create_ts = time.time()

    @property
    def ttl(self):
        return time.time() - self._create_ts


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CredCache(metaclass=Singleton):
    def __init__(self):
        self._cred = self.create_cred()

    @property
    def effective_cred(self) -> CredObject:
        # 获得有效的token
        if self._cred.ttl > CRED_TTL:
            logger.info(f'刷新token')
            self._cred = self.create_cred()

        return self._cred

    def create_cred(self) -> CredObject:
        # 获取登陆所需headers

        if DRY_RUN:
            return CredObject(token='dry_run_token', cookie='dry_run_cookie')
        path = '/api/keystone/user/login'

        try:
            r = http_requests.post(SERVER + path, json={"email": AUTH_NAME,
                                                        "password": AUTH_PASSWORD,
                                                        "code": "",
                                                        "agreementVersion": "",
                                                        "privacyVersion": ""})
            r.raise_for_status()
            resp = r.json()
        except Exception as e:
            raise RequestConnError('网络出错')

        if resp.get('code') != 0:
            raise ResponseError(message=f'调用url:{url}出错', error_resp=resp)

        logger.info(f'call create_cred')

        return CredObject(token=resp['data']['token'], cookie=resp['data']['cookie'])


class Request:
    """

    dry_run_patch修饰的方法返回多个运行状态 (xxx,bool):
        True 是测试，无实际调用
        False 正常调用
    """

    def auth_header(self):
        return dict(Authorization=f'JWT {CredCache().effective_cred.token}')

    def base_api(self, method: str, path: str, query_params: dict = None, post_data: dict = None, resp_type='json',
                 authenticate=True, **kwargs):
        headers = self.auth_header() if authenticate else None

        url = SERVER + path

        ext_info = ''

        if query_params:
            ext_info += f'query:{query_params}'

        if post_data:
            ext_info += f'post_data:{post_data}'

        if DRY_RUN:
            logger.info(f'cmp_sdk:dry run {method}->{url}  detail:{ext_info} ')
            return

        if method.lower() == 'get':
            req = http_requests.get(url, params=query_params, headers=headers)
        elif method.lower() == 'post':
            req = http_requests.post(url, json=post_data, headers=headers)
        elif method.lower() == 'put':
            req = http_requests.put(url, json=post_data, headers=headers)
        elif method.lower() == 'delete':
            req = http_requests.delete(url, json=post_data, headers=headers)
        else:
            raise AssertionError('unknow method')

        if resp_type == 'json':
            resp = req.json()

        if resp.get('code') != 0:
            raise ResponseError(message=f'调用url:{url}出错', error_resp=resp)

        return resp

    @dry_run_patch
    def company(self) -> object:
        path = '/api/v2/accounts/company/list'
        method = 'get'
        return self.base_api(method=method, path=path)

    @dry_run_patch
    def info(self) -> object:
        path = '/api/v2/accounts/info/'
        method = 'get'
        return self.base_api(method=method, path=path)

    @dry_run_patch
    def list_host_instance_event(self, start_ts: int, end_ts: int) -> object:
        items = []
        path = '/api/audit/userOpLog'

        _query_params = {
            'operateOn': '服务器',
            'timestampStart': start_ts,
            'timestampEnd': end_ts,
        }
        for _page in range(1, 100):
            query_params = _query_params.copy()
            query_params.update(dict(page=_page))
            resp = self.base_api(method='get', path=path, query_params=query_params)
            # print(resp)

            results = resp['data']['results']

            for i in results:
                host_instance_pk = i['data']['实例ID']
                host_instance_obj = self.query_host_instance_detail(host_instance_pk)
                event_obj = event_parser(i, instance_obj=host_instance_obj)
                items.append(event_obj)
            # 解析对象

            return items

    @dry_run_patch
    def query_host_instance_detail(self, private_id) -> Instance:

        path = f'/api/resource/globalsearch?resourceType=compute&page=1&resourceId={private_id}'

        resp = self.base_api(method='get', path=path)

        results = resp['data']['results']

        if results:
            result = results[0]

            return instance_detail_parser(result, instance_type=EnumInstanceType.host)
        else:
            return NoExistInstance()

    @dry_run_patch
    def create_node(self, name, unique_id, base_node_id=0) -> object:
        """
        ARGS:
            unique_id(str):
                唯一ID
            name(str):
                服务树名称
            base_node_id(int):
                父级服务树ID
        """

        path = '/api/v2/serviceTree/node/'

        post_params = {
            "NodeId": base_node_id,
            "companyId": COMPANY_ID,
            "description": f"unique_id:{unique_id}",
            "name": name,
            "op": AUTH_NAME,
            "rd": AUTH_NAME
        }

        resp = self.base_api(method='post', path=path, post_data=post_params)
        node_id = resp['data']['id']
        return node_id

    @dry_run_patch
    def update_node(self, node_id, name, unique_id, base_node_id=0) -> object:
        """
        ARGS:
            unique_id(str):
                唯一ID
            name(str):
                服务树名称
            base_node_id(int):
                父级服务树ID
        """

        path = '/api/v2/serviceTree/node/'

        post_params = {
            "NodeId": base_node_id,
            "companyId": COMPANY_ID,
            "description": f"unique_id:{unique_id}",
            "name": name,
            "nodeId": node_id,
            "op": AUTH_NAME,
            "rd": AUTH_NAME,
        }

        resp = self.base_api(method='put', path=path, post_data=post_params)
        node_id = resp['data']['id']
        return node_id

    @dry_run_patch
    def delete_node(self, node_id) -> object:
        path = '/api/v2/serviceTree/node/'
        post_params = {
            "NodeId": node_id
        }
        resp = self.base_api(method='delete', path=path, post_data=post_params)
        if resp.get('msg', 'unknow') == 'ok':
            return 'ok'
        else:
            return resp.get('msg')

    @dry_run_patch
    def query_node_tree(self) -> object:
        path = '/api/keystone/serviceTree?statistics=true'
        resp = self.base_api(method='get', path=path)

        data = resp['data']

        return data

    @dry_run_patch
    def node_detail(self, node_id) -> object:
        path = f'/api/v2/serviceTree/node/?nodeId={node_id}'
        resp = self.base_api(method='get', path=path)
        return resp['data']
