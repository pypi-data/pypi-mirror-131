import requests
import json
from requests.auth import HTTPDigestAuth


class CASClient(object):

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    @property
    def headers(self):
        return {
            "Content-Type": 'application/json',
            'Accept': 'application/json'
        }

    @property
    def auth(self):
        return HTTPDigestAuth(self.username, self.password)

    def common_request(self, method, endpoint, params={}, body={}, need_loads=True):
        url = self.url + endpoint
        data = json.dumps(body)
        resp = getattr(requests, method)(url, headers=self.headers, auth=self.auth, params=params, data=data)
        if int(resp.status_code) != 200 and int(resp.status_code) != 204:
            raise Exception(resp.text)
        return resp.text if not need_loads else json.loads(resp.text)

    def paging_request(self, method, url, rep_key="", params={}, offset=0, limit=1000):
        ret = []
        params.update({
            "offset": offset,
            "limit": limit
        })
        tmp = self.common_request(method, url, params=params)
        if isinstance(tmp[rep_key], list):
            ret.extend(tmp[rep_key])
        else:
            ret.append(tmp[rep_key])
        index = 1
        while len(tmp) == limit:
            params.update({
                "offset": index * limit + 1
            })
            tmp = self.common_request(method, url, params=params)
            if not tmp:
                break
            if isinstance(tmp[rep_key], list):
                ret.extend(tmp[rep_key])
            else:
                ret.append(tmp[rep_key])
            index += 1
        return ret
