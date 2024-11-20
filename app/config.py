import json
import os
from typing import Optional

class Config:
    def __init__(self, config_path: Optional[str] = 'local.settings.json'):
        # Load from environment variables if available
        self.dbkey: str = os.getenv('DBKEY') or self._load_from_file(config_path, 'Values', 'dbkey')
        self.DBURI: str = os.getenv('DBURI') or self._load_from_file(config_path, 'Values', 'DBURI')
        self.DBName: str = os.getenv('DBNAME') or self._load_from_file(config_path, 'Values', 'DBName')
        self.jwt_key: str = os.getenv('JWTKEY') or self._load_from_file(config_path, 'JwtSettings', 'Key')
        self.jwt_issuer: str = os.getenv('JWTISSUER') or self._load_from_file(config_path, 'JwtSettings', 'Issuer')
        self.jwt_audience: str = os.getenv('JWTAUDIENCE') or self._load_from_file(config_path, 'JwtSettings', 'Audience')

    def _load_from_file(self, config_path: str, section: str, key: str) -> str:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"{config_path} not found and no environment variable provided for {key}.")
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config[section][key]

config = Config()
