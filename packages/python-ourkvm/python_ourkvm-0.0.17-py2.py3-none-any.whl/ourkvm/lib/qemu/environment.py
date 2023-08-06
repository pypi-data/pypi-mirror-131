import json
import pathlib
from typing import Dict, Any

from ..networking import load_network_info, unload_network_info, get_namespace_info, add_namespace, generate_mac
from ..helpers.exceptions import NamespaceNotFound, ConfigurationError

def load_conf(config :str) -> Dict[str, Any]:
	config_path = pathlib.Path(config).expanduser().absolute()

	if not config_path.exists():
		raise ConfigurationError(f"Could not locate configuration {config}")

	with config_path.open('r') as fh:
		configuration = json.load(fh)

	return dict(configuration)

def load_environment(config :str) -> None:
	configuration = load_conf(config)

	if namespace := configuration.get('namespace'):
		try:
			get_namespace_info(namespace)
		except NamespaceNotFound:
			add_namespace(namespace)

	if interfaces := configuration.get('interfaces'):
		load_network_info(interfaces=interfaces)

def dismantle_environment(config :str) -> None:
	configuration = load_conf(config)

	if configuration.get('interfaces'):
		unload_network_info(interfaces=configuration['interfaces'])

def load_network_cards_from_env(config :str) -> str:
	configuration = load_conf(config)

	result = ''

	network_id = 0
	if interfaces := configuration.get('interfaces'):
		interface_on_network = 0
		for interface in interfaces:
			if interface.get('attach'):
				if not (mac := interface.get('mac')):
					mac = generate_mac(filters=[])

				result += f" -device virtio-net-pci,mac={mac},id=network{network_id},netdev=network{network_id}.{interface_on_network},status=on,bus=pcie.0" # ,bootindex=2
				result += f" -netdev {interface['type']},ifname={interface['name']},id=network{network_id}.{interface_on_network},script=no,downscript=no"
				interface_on_network += 1

		# network_id += 1

	return result