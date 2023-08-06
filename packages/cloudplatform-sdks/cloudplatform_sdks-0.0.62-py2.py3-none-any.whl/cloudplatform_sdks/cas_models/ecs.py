from .clients import cas_ecs_client


class CASEcs:
    STATE_AVAILABLE = 'ACTIVE'
    STATE_STARTED = 'started'
    STATE_STOPPED = 'SHUTOFF'
    JOB_STATE_SUCCESS = 'SUCCESS'
    JOB_STATE_FAIL = 'FAIL'
    PORT_STATE_AVAILABLE = 'ACTIVE'

    def __init__(self, object):
        self.object = object

    @property
    def id(self):
        return self.object.get("id")

    @property
    def name(self):
        return self.object.get("name")

    @property
    def status(self):
        return self.object.get("status")

    @property
    def uuid(self):
        return self.object.get("uuid")

    @property
    def cpu(self):
        return self.object.get("cpu")

    @property
    def memory(self):
        return self.object.get("memory")

    @property
    def availability_zone(self):
        return self.object.get("hostId")

    @property
    def addresses(self):
        return self.object.get("network")

    @property
    def volumes(self):
        return self.object.get("storage")
    
    def start(self):
        return cas_ecs_client.start_server(self.id)

    def stop(self):
        return cas_ecs_client.stop_server(self.id)

    def reboot(self):
        return cas_ecs_client.reboot_server(self.id)

    @classmethod
    def resize(cls, params=None):
        return cas_ecs_client.modify_server(body_params=params)

    @classmethod
    def config_net(cls, params=None):
        return cas_ecs_client.modify_server(body_params=params)

    @classmethod
    def get(cls, instance_id=None):
        params = {
            "vm_id": instance_id
        }
        resp = cas_ecs_client.describe_server(params)
        if not resp:
            return
        return cls(resp)

    @classmethod
    def create(cls, params=None):
        create_response = cas_ecs_client.create_server(body_params=params)
        if not create_response:
            return
        return create_response.get("msgId")

    def delete(self):
        return cas_ecs_client.delete_server(self.id)

    @classmethod
    def show_vs(cls, params=None):
        return cas_ecs_client.show_vswitch(body_params=params)

    @classmethod
    def show_template(cls, template_id=None):
        templates = cas_ecs_client.vm_templates()
        for each in templates:
            if each["id"] == template_id:
                return each
        return {}

    @classmethod
    def show_message(cls, msg_id=None):
        return cas_ecs_client.show_message({"msg_id": msg_id})

    @classmethod
    def create_storage(cls, params=None):
        return cas_ecs_client.add_storage(body_params=params)

    @classmethod
    def create_volume(cls, params=None):
        return cas_ecs_client.add_volume(body_params=params)

    @classmethod
    def storage_pools(cls, params=None):
        return cas_ecs_client.storages(params.get("host_id")).get("storagePool")





