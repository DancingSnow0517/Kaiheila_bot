import json
import os.path
from typing import List, Dict

default_config = {
    "token": '',
    'rcon': [],
    'permission': {}
}


class RconServer:
    address: str
    port: int
    password: str

    def __init__(self, address: str, port: int, password: str) -> None:
        self.address = address
        self.port = port
        self.password = password

    def to_dict(self) -> dict:
        return {'address': self.address, 'port': self.port, 'password': self.password}


class Config:
    config_file_path: str
    token: str
    rcon: List[RconServer]
    permission: Dict[str, int]

    def wirte_to_config(self):
        js = {'token': self.token, 'rcon': []}
        for i in self.rcon:
            js['rcon'].append(i.to_dict())
        js['permission'] = self.permission
        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            json.dump(js, f, ensure_ascii=False, indent=4)

    def read_from_json(self):

        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                js = json.load(f)
        else:
            js = default_config
        self.token = js['token']
        for i in js['rcon']:
            self.rcon.append(RconServer(js[i]['address'], js[i]['port'], js[i]['password']))
        self.permission = js['permission']
        self.wirte_to_config()

    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
        self.rcon = []
        self.token = ''
        self.permission = {}
