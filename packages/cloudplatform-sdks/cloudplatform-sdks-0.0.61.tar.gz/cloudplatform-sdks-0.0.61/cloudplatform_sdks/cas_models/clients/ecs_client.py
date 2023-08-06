from .client import CASClient


class CASEcsClient(CASClient):
    def __init__(self, *args, **kwargs):
        super(CASEcsClient, self).__init__(*args, **kwargs)

    def validation(self, params=None):
        endpoint = "/cas/casrs/operator/getAuthUrl"
        return self.common_request("get", endpoint)

    def vm_templates(self, params=None):
        endpoint = "/cas/casrs/vmTemplate/vmTemplateList"
        return self.paging_request("get", endpoint, rep_key="domain")

    def host_pools(self, params=None):
        endpoint = "/cas/casrs/hostpool/all"
        return self.common_request("get", endpoint)

    def host_clusters(self, hostpool_id):
        endpoint = "/cas/casrs/hostpool/{}/allChildNode".format(hostpool_id)
        return self.common_request("get", endpoint)

    def hosts(self, params=None):
        hostpool_id = params.get("hpId")
        endpoint = "/cas/casrs/hostpool/host/{}".format(hostpool_id)
        new_params = {
            "hpId": hostpool_id
        }
        return self.paging_request("get", endpoint, rep_key="host", params=new_params)

    def storages(self, host_id):
        endpoint = "/cas/casrs/storage/pool"
        new_params = {
            "hostId": host_id
        }
        return self.common_request("get", endpoint, params=new_params)

    def switchs(self, params=None):
        endpoint = "/cas/casrs/vm/queryVSwtichNameList/{}/{}".format(params.get("destType"), params.get("hostId"))
        return self.common_request("get", endpoint)

    def instances(self, params=None):
        endpoint = "/cas/casrs/vm/vmList"
        new_params = {
            "hostId": params.get("hostId")
        }
        return self.paging_request("get", endpoint, rep_key="domain", params=new_params)

    def create_server(self, body_params=None):
        endpoint = "/cas/casrs/vm/deploy"
        return self.common_request("post", endpoint, body=body_params)

    def delete_server(self, vm_id):
        endpoint = "/cas/casrs/vm/delete/{}".format(vm_id)
        new_params = {
            "id": vm_id
        }
        return self.common_request("delete", endpoint, params=new_params)

    def start_server(self, vm_id):
        endpoint = "/cas/casrs/vm/start/{}".format(vm_id)
        params = {
            "id": vm_id
        }
        return self.common_request("put", endpoint, params=params)

    def stop_server(self, vm_id):
        endpoint = "/cas/casrs/vm/powerOff/{}".format(vm_id)
        params = {
            "id": vm_id
        }
        return self.common_request("put", endpoint, params=params)

    def reboot_server(self, vm_id):
        endpoint = "/cas/casrs/vm/restart/{}".format(vm_id)
        params = {
            "id": vm_id
        }
        return self.common_request("put", endpoint, params=params)

    def modify_server(self, body_params=None):
        endpoint = "/cas/casrs/vm/modify"
        return self.common_request("put", endpoint, body=body_params)

    def describe_server(self, params=None):
        vm_id = params.get("vm_id")
        endpoint = "/cas/casrs/vm/{}".format(vm_id)
        params = {
            "id": vm_id
        }
        return self.common_request("get", endpoint, params=params)

    def volumes(self, params=None):
        endpoint = "/cas/casrs/vm/volume/info"
        return self.common_request("get", endpoint, params=params)

    def show_vswitch(self, params=None):
        endpoint = "/cas/casrs/vswitch/info"
        new_params = {
            "vsId": params.get("vsId")
        }
        return self.common_request("get", endpoint, params=new_params)

    def storage_pool(self, params=None):
        endpoint = "/cas/casrs/storage/pool"
        new_params = {
            "hostId": params.get("hostId")
        }
        return self.common_request("get", endpoint, params=new_params)

    def show_message(self, params=None):
        endpoint = "/cas/casrs/message/{}".format(params.get("msg_id"))
        return self.common_request("get", endpoint)

    def add_storage(self, body_params=None):
        endpoint = "/cas/casrs/storage/volume"
        return self.common_request("post", endpoint, body=body_params, need_loads=False)

    def add_volume(self, body_params=None):
        endpoint = "/cas/casrs/vm/addDevice"
        return self.common_request("put", endpoint, body=body_params)

    def show_profiles(self, params=None):
        endpoint = "/cas/casrs/profile"
        return self.common_request("get", endpoint)







