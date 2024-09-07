from networktools import NetworkTools

nt = NetworkTools()

print(nt.network_info(interface="eth0").model_dump_json(indent=2))
