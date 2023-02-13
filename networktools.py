from dataclasses import asdict
from subprocess import check_output
from networktools.dependencies.models import NetworkInfo


class NetworkTools:

    def __init__(self):
        self.__cached_network_info = None

    def host_name(self) -> str:
        return str(check_output(
            ['hostname']).decode('utf-8').strip())

    def ssid(self) -> str:
        return check_output(
            ['sudo', 'iwgetid', '-r']).decode('utf-8').strip()

    def ip_address(self) -> str:
        return check_output(
            ['hostname', '-I']).decode('utf-8').strip()

    def subnet_range(self) -> str:
        ip_splitted = self.ip_address().split('.')
        ip_splitted.pop()
        return ".".join(ip_splitted)+".0/24"

    def mac_address(self) -> str:
        with open('/sys/class/net/wlan0/address', 'r') as file:
            for line in file:
                return line.strip().replace(':', '').upper()

    def ping_test(self, address) -> bool:
        try:
            result = check_output(
                ['ping', address, '-c', '5']).decode('utf-8').replace('\n', ' ')
            return False if "Unreachable" in result else True

        except Exception as e:
            self.logger.warning(f"{type(e).__name__}: {e}")

    def network_info(self, use_cache: bool = True, as_dict: bool = False) -> NetworkInfo:
        if not use_cache or not self.__cached_network_info:
            info = NetworkInfo(host_name=self.host_name(), ip_address=self.ip_address(),
                               subnet_range=self.subnet_range(), ssid=self.ssid(), mac=self.mac_address())

            self.__cached_network_info = info

            if as_dict == True:
                return asdict(info)

            return info

        if as_dict == True:
            return asdict(self.__cached_network_info)

        return self.__cached_network_info
