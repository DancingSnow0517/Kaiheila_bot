import json
import os.path
from typing import List, Dict, Optional, overload, Callable, Any, IO

from mcdreforged.utils.serializer import Serializable
from ruamel import yaml

from .libs.chatbridge.core.config import ClientConfig


class ConfigBase(Serializable):
    __config_file: str = "config.yml"
    __loader: Callable[[ConfigBase, IO], Any] = lambda self, stream: yaml.round_trip_load(stream)
    __dumper: Callable[[ConfigBase, IO], Any] = lambda self, stream: yaml.round_trip_dump(self.serialize(), stream, allow_unicode=True, indent=4)

    @classmethod
    def load(cls, path: str = __config_file):
        if not os.path.exists(path):
            cls.get_default().save()
            return cls.get_default()
        with open(path, "r", encoding="UTF-8") as fp:
            return cls.deserialize(cls.__loader(fp))

    def save(self, path: str = __config_file):
        with open(path, "w", encoding="UTF-8") as fp:
            self.__dumper(fp)


class RconServer(Serializable):
    name: str
    address: str
    port: int
    password: str


class Subscription(Serializable):
    name: str
    dynamic: bool
    live: bool


class SentryConfig(ConfigBase):
    __config_file = "sentry.json"
    __loader = json.load
    __dumper = lambda data, stream: json.dump(data, stream, ensure_ascii=False, indent=4, sort_keys=True)

    sentry_dsn: Optional[str]
    sentry_debug: bool = False
    sentry_release: Optional[str] = None
    sentry_environment: Optional[str] = None
    sentry_server_name: Optional[str] = None
    sentry_sample_rate: float = 1.0
    sentry_max_breadcrumbs: int = 100
    sentry_attach_stacktrace: bool = False
    sentry_send_default_pii: bool = False
    sentry_request_bodies: str = "medium"
    sentry_with_locals: bool = True
    sentry_ca_certs: Optional[str] = None
    sentry_before_send: Optional[Callable[[Any, Any], Optional[Any]]] = None
    sentry_before_breadcrumb: Optional[Callable[[Any, Any], Optional[Any]]] = None
    sentry_transport: Optional[Any] = None
    sentry_http_proxy: Optional[str] = None
    sentry_https_proxy: Optional[str] = None
    sentry_shutdown_timeout: int = 2


class Config(ConfigBase, ClientConfig):
    token: str = ''
    rcon: List[RconServer] = []
    permission: List[str] = []
    bilibili_permission: bool = True
    subscription: Dict[str, Subscription] = {}
    prefixes: List[str] = ['!!', '！！']
    next: int = 0
    delete_pyppeteer: bool = False
    khl_server_id: str = ''
    khl_channel: List[str] = []
    khl_channel_mc_chat: str = ""
    log_level: str = 'DEBUG'
    mcdr_server_path: str = ''
    velocity_rcon: dict = {'address': '127.0.0.1', 'password': 'rcon_password', 'port': 25566}

    @overload
    def add_rcon(self, *, name: str, address: str, port: int, password: str):
        ...

    def add_rcon(self, **kwargs):
        self.rcon.append(**kwargs)
        self.save()

    def get_rcon_list(self) -> List[RconServer]:
        return self.rcon

    def get_velocity_rcon(self) -> RconServer:
        return RconServer(name='velocity', address=self.velocity_rcon['address'], port=self.velocity_rcon['port'], password=self.velocity_rcon['password'])

    @overload
    def add_subscription(self, uid: str, *, name: str, live=True, dynamic=True) -> bool:
        ...

    def add_subscription(self, uid: str, **kwargs) -> bool:
        if uid in self.subscription:
            return False
        self.subscription[uid] = Subscription(**kwargs)
        self.save()
        return True

    def get_subscription(self, uid: str) -> Optional[Subscription]:
        return self.subscription.get(uid)

    def del_subscription(self, uid: str) -> bool:
        if uid in self.subscription:
            del self.subscription[uid]
            self.save()
            return True
        return False

    def updata_subscription(self, uid: str, name: str):
        self.subscription[uid].name = name
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

    def get_live_uid_list(self) -> List[str]:
        ret = []
        for i in self.subscription:
            if self.subscription[i].live:
                ret.append(i)
        return ret
