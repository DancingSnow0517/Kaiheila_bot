import os.path
from typing import List, Dict, Optional

from mcdreforged.utils.serializer import Serializable

from ruamel import yaml


class _Config(Serializable):
    @classmethod
    def load(cls, path: str):
        if not os.path.exists(path):
            cls.get_default().save()
            return cls.get_default()
        with open(path, "r", encoding="UTF-8") as fp:
            return cls.deserialize(yaml.safe_load(fp))

    def save(self, path: str):
        with open(path, "w", encoding="UTF-8") as fp:
            yaml.dump(self.serialize(), fp, allow_unicode=True, indent=4)


class RconServer(_Config):
    address: str
    port: int
    password: str


class Subscription(_Config):
    name: str
    dynamic: bool
    live: bool


class Config(_Config):
    token: str = ''
    rcon: List[dict] = []
    permission: List[str] = []
    bilibili_permission: bool = True
    subscription: Dict[str, dict] = {}
    prefixes: List[str] = ['!!', '！！']
    next: int = 0
    delete_pyppeteer: bool = False
    khl_server_id: str = ''
    khl_channel: List[str] = []

    @classmethod
    def load(cls, path: str = 'config.yml'):
        return super().load(path)

    def save(self, path: str = 'config.yml'):
        return super().save(path)

    def add_rocn(self, address: str, port: int, password: str):
        self.rcon.append({'address': address, 'port': port, 'password': password})

    def get_rcon_list(self) -> List[RconServer]:
        ret = []
        for i in self.rcon:
            ret.append(RconServer(address=i['address'], port=i['port'], password=i['password']))
        return ret

    def add_subscription(self, uid: str, name: str, live=True, dynamic=True) -> bool:
        if uid in self.subscription:
            return False
        self.subscription[uid] = {'name': name, 'live': live, 'dynamic': dynamic}
        self.save()
        return True
        pass

    def get_subscription(self, uid: str) -> Optional[Subscription]:
        if uid in self.subscription:
            return Subscription(
                name=self.subscription[uid]['name'],
                dynamic=self.subscription[uid]['dynamic'],
                live=self.subscription[uid]['live']
            )
        else:
            return None

    def del_subscription(self, uid: str) -> bool:
        if uid in self.subscription:
            del self.subscription[uid]
            self.save()
            return True
        return False

    def updata_subscription(self, uid: str, name: str):
        self.subscription[uid]['name'] = name
        self.save()

    def getnext_subscription_uid(self) -> Optional[str]:
        sub_list = list(self.subscription.keys())
        if not sub_list:
            return None
        if self.next+1 >= len(sub_list):
            self.next = 0
        else:
            self.next += 1
        return sub_list[self.next]
