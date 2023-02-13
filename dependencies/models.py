from typing import Optional
from dataclasses import dataclass


@dataclass
class NetworkInfo:

    host_name: Optional[str]
    ip_address: Optional[str]
    subnet_range: Optional[str]
    ssid: Optional[str]
    mac: Optional[str]
