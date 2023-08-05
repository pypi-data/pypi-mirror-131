import json
import pathlib
from typing import Dict, Any

from ..networking import load_network_info, unload_network_info, get_namespace_info, add_namespace
from ..helpers.exceptions import NamespaceNotFound

def load_conf(config :str) -> Dict[str, Any]:
	config_path = pathlib.Path(config).expanduser().absolute()

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