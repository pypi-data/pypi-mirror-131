import json
import socket
import psutil
import sys
import pwd
import getpass
import logging
from typing import Dict, List, Any, Optional, Union, Iterator

from ..helpers.logger import log
from ..helpers.syscalls import SysCommand
from ..helpers.exceptions import NamespaceNotFound, NamespaceError, UnsupportedHardware, InterfaceNotFound, InterfaceError

if sys.platform == 'linux':
	from select import epoll as epoll
	from select import EPOLLIN as EPOLLIN
	from select import EPOLLHUP as EPOLLHUP
else:
	import select
	EPOLLIN = 0
	EPOLLHUP = 0

	class epoll():
		""" #!if windows
		Create a epoll() implementation that simulates the epoll() behavior.
		This so that the rest of the code doesn't need to worry weither we're using select() or epoll().
		"""
		def __init__(self) -> None:
			self.sockets: Dict[str, Any] = {}
			self.monitoring: Dict[int, Any] = {}

		def unregister(self, fileno :int, *args :List[Any], **kwargs :Dict[str, Any]) -> None:
			try:
				del(self.monitoring[fileno])
			except:
				pass

		def register(self, fileno :int, *args :int, **kwargs :Dict[str, Any]) -> None:
			self.monitoring[fileno] = True

		def poll(self, timeout: float = 0.05, *args :str, **kwargs :Dict[str, Any]) -> List[Any]:
			try:
				return [[fileno, 1] for fileno in select.select(list(self.monitoring.keys()), [], [], timeout)[0]]
			except OSError:
				return []

class ip:
	@staticmethod
	def link(*args :str, options :List[str] = []) -> SysCommand:
		return SysCommand(f"ip {''.join(options)} link {' '.join(args)}")

	@staticmethod
	def netns(*args :str) -> SysCommand:
		return SysCommand(f"ip netns {' '.join(args)}")

	@staticmethod
	def tuntap(*args :str) -> SysCommand:
		return SysCommand(f"ip tuntap {' '.join(args)}")

def add_namespace(namespace :str) -> bool:
	if (output := ip.netns(f"add {namespace}")).exit_code != 0:
		raise NamespaceError(f"Could not create namespace {namespace}: {output}")

	return True

def del_namespace(namespace :str) -> bool:
	if (output := ip.netns(f"del {namespace}")).exit_code != 0:
		raise NamespaceError(f"Could not delete namespace {namespace}: {output}")

	return True

def run_namespace(namespace :str, *args :str) -> bool:
	if (output := ip.netns(f"exec {namespace}", *args)).exit_code != 0:
		raise NamespaceError(f"Could not execute in namespace {namespace}: {output}")

	return True

def add_bridge(ifname :str, namespace :Optional[str] = None) -> bool:
	if namespace:
		if ip.netns(f"exec {namespace} ip link add name {ifname} type bridge").exit_code == 0:
			return bool(ip.netns(f"exec {namespace} ip link set dev {ifname} up").exit_code == 0)
	else:
		if ip.link(f"add name {ifname} type bridge").exit_code == 0:
			return bool(ip.link(f"set dev {ifname} up").exit_code == 0)
	return False

def add_if_to_bridge(bridge :str, ifname :str, namespace :Optional[str] = None) -> bool:
	if namespace:
		return bool(ip.netns(f"exec {namespace} ip link set dev {ifname} master {bridge}").exit_code == 0)
	else:
		return bool(ip.link(f"set dev {ifname} master {bridge}").exit_code == 0)

def ifup(ifname :str) -> bool:
	return bool(ip.link(f"set {ifname} up").exit_code == 0)

def ifdown(ifname :str) -> bool:
	return bool(ip.link(f"set {ifname} down").exit_code == 0)

def get_namespace_info(namespace :Optional[str] = None) -> Dict[str, Any]:
	if (output := SysCommand("ip -oneline -color=never -j netns list")).exit_code == 0:
		if namespace:
			try:
				for info in json.loads(str(output.decode())):
					if info.get('name') == namespace:
						return dict(info)
				raise NamespaceNotFound(f"Could not locate namespace {namespace} in output: {output}")
			except json.decoder.JSONDecodeError:
				raise NamespaceError(f"Could not locate namespace {namespace} in output: {output}")
		else:
			return dict(json.loads(str(output)))
	elif output.exit_code == 256:
		raise NamespaceNotFound(f"Could not locate namespace {namespace} in output: {output}")
	else:
		raise ValueError(f"Could not execute namespace info grabber: {output.exit_code} {output}")

def get_interface_info(ifname :str) -> Iterator[Dict[str, Union[int, None, str]]]:
	if info := psutil.net_if_addrs().get(ifname):
		for obj in info:
			yield {
				"family": {socket.AF_INET: "IPv4", socket.AF_INET6: "IPv6", psutil.AF_LINK: "MAC"}.get(obj[0]),
				"address": obj[1],
				"netmask": obj[2],
				"broadcast": obj[3],
				"point_to_point": obj[4]
			}
	else:
		raise InterfaceNotFound(f"Could not locate interface {ifname}.")

def create_interface(ifname :str, iftype :str, pair_name :Optional[str] = None) -> None:
	if iftype == 'tap':
		user_info = pwd.getpwnam(getpass.getuser())

		if not (output := ip.tuntap(f"add mode tap one_queue vnet_hdr user {user_info.pw_uid} group {user_info.pw_gid} name {ifname}")).exit_code == 0:
			raise InterfaceError(f"Could not add tap interface {ifname}: [{output.exit_code}] {output}")

	elif iftype == 'veth':
		if pair_name is None:
			pair_name = f"{ifname}_ns"
		try:
			list(get_interface_info(f"{ifname}"))
		except InterfaceNotFound:
			if (handle := ip.link(f"add {ifname} type veth peer name {pair_name}")).exit_code != 0:
				raise InterfaceError(f"Could not create veth pair: {handle}")

	elif iftype == 'phys':
		list(get_interface_info(ifname))

	else:
		raise UnsupportedHardware(f"Unknown interface type {iftype}")

def load_network_info(interfaces :List[Dict[str, Any]] = []) -> None:
	for interface in interfaces:
		print(interface)
		if not (ifname := interface.get('name')):
			raise InterfaceError(f"Loading interfaces require the interface information to have a name key with a str value.")

		if (iftype := interface.get('type')):
			create_interface(ifname, iftype, pair_name=interface.get('veth_pair'))

		if namespace := interface.get('namespace'):
			try:
				get_namespace_info(interface['namespace'])
			except (NamespaceNotFound, NamespaceError):
				add_namespace(interface['namespace'])

			ip.link(f"set {ifname} netns {interface['namespace']}")

		if interface.get('bridge'):
			add_bridge(f"{interface['bridge']}", namespace=namespace)
			add_if_to_bridge(f"{interface['bridge']}", f"{interface['name']}", namespace=namespace)

def unload_network_info(interfaces :List[Dict[str, Any]] = []) -> None:
	from .interfaces import get_bridge_interfaces
	
	for interface in interfaces:
		if (namespace := interface.get('namespace')):
			try:
				get_namespace_info(namespace)
				del_namespace(namespace)
			except (NamespaceNotFound, NamespaceError):
				pass
		else:
			if not interface.get('name'):
				raise InterfaceError(f"Loading interfaces require the interface information to have a name key with a str value.")

			ip.link(f"del {interface.get('name')}")

			if (bridge := interface.get('bridge')):
				if len(get_bridge_interfaces(bridge)) == 0:
					ip.link(f"del {bridge}")
				else:
					log(f"Bridge {bridge} was not empty, leaving it alone.", level=logging.INFO)