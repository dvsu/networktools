from pydantic import BaseModel


class NetworkInfo(BaseModel):
    host_name: str | None
    ip_address: str | None
    subnet_range: str | None
    ssid: str | None
    mac: str | None
