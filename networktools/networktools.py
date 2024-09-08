import re
from pathlib import Path
from subprocess import check_output

from .models import NetworkInfo


class NetworkTools:
    def __init__(self):
        self.__cached_network_info: NetworkInfo | None = None

    def host_name(self) -> str:
        return str(check_output(["hostname"]).decode("utf-8").strip())

    def ssid(self) -> str:
        return check_output(["sudo", "iwgetid", "-r"]).decode("utf-8").strip()

    def ip_address(self) -> str:
        return check_output(["hostname", "-I"]).decode("utf-8").strip().split(" ")[0]

    def subnet_range(self) -> str:
        ip_splitted = self.ip_address().split(".")
        ip_splitted.pop()
        return ".".join(ip_splitted) + ".0/24"

    def mac_address(self, interface: str) -> str | None:
        interface_path = Path(f"/sys/class/net/{interface}/address")

        if interface_path.exists():
            with open(interface_path) as file:
                for line in file:
                    return line.strip().replace(":", "").upper()

        output = check_output(["ethtool", "-P", interface]).decode("utf-8").strip().split(" ")
        pattern = re.compile(r"^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$", re.IGNORECASE)

        if len(output) > 2 and bool(pattern.match(output[2])):
            return output[2]

        return None

    def ping_test(self, address: str) -> bool:
        try:
            result = check_output(["ping", address, "-c", "5"]).decode("utf-8").replace("\n", " ")
            return "Unreachable" not in result

        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            return False

    def network_info(self, interface: str, use_cache: bool = True) -> NetworkInfo:
        if not use_cache or not self.__cached_network_info:
            info = NetworkInfo(
                host_name=self.host_name(),
                ip_address=self.ip_address(),
                subnet_range=self.subnet_range(),
                ssid=None if "wlan" not in interface else self.ssid(),
                mac=self.mac_address(interface),
            )

            self.__cached_network_info = info

            return info

        return self.__cached_network_info
