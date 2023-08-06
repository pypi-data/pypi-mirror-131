import json
from typing import List, Any
from .net import ip
from ..helpers.exceptions import InterfaceError

# https://serverfault.com/a/40720
def generate_mac(prefix :str = 'FE:00:00', filters :List[str] = []) -> str:
	for number in range(16**6):
		hex_num = hex(number)[2:].zfill(6)

		if (address := "{}:{}{}:{}{}:{}{}".format(prefix, *hex_num)) not in filters:
			return address

	raise InterfaceError(f"No available addresses with the prefix {prefix}")

def get_bridge_interfaces(name :str) -> Any:
	if (result := ip.link(f"show master {name}", options=['--json'])).exit_code == 0:
		return json.loads(result.decode('UTF-8'))

	return {}