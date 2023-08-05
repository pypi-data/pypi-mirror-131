import json
import pathlib
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel
from fastapi import Security, HTTPException
from .app import app
from .security import User, process_user_claim
from ..lib.qemu import write_qemu_service_file, create_qemu_string, verify_qemu_resources, qemu_img
from ..lib.helpers.dupedict import DupeDict, JSON
from ..lib.helpers.syscalls import SysCommand

class NewVirtualMachine(BaseModel):
	namespace: Optional[str] = None
	cpu: str = "host"
	enable_kvm: bool = True
	machine: str = "q35,accel=kvm"
	devices: List[str] = ["intel-iommu"]
	memory: int = 8192 # TODO: Make this value dynamic by reading machine total memory / 4 or something
	drives: List[str] = [
		"if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/x64/OVMF_CODE.fd",
		"if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/x64/OVMF_VARS.fd"
	]
	pcie_root_ports: List[str] = []
	pcie_slave_buses: List[str] = []
	pcie_slave_devices: List[str] = []
	harddrives: List[Dict[str, int]] = []
	cdroms: List[str] = []
	network: List[Dict[str, Union[str, int, bool]]] = []
	graphics: bool = False
	service_location: str = '/etc/systemd/system/'
	config_location: str = '/etc/qemu.d/'

class ResourceLocations(BaseModel):
	service_location: str = '/etc/systemd/system/'
	config_location: str = '/etc/qemu.d/'
	run_as: str = 'root'

@app.put("/qemu/machine/{name}", tags=["qemu"])
def create_machine_configuration(name :str, info :NewVirtualMachine, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> Dict[str, Any]:
	"""
	This API can be used to create new virtual machine configuration.
	This API endpoint will create harddrive resources specified in `--harddrives`.
	This endpoint also creates the `.service` and `.cfg` files under `--service_location` and `--config_location` paths.
	"""

	service_path = (pathlib.Path(info.service_location) / f"{name}.service").expanduser().absolute()
	qemu_config_path = (pathlib.Path(info.config_location) / f"{name}.cfg").expanduser().absolute()

	if not qemu_config_path.parent.exists():
		qemu_config_path.parent.mkdir(parents=True)

	if service_path.exists():
		raise HTTPException(status_code=409, detail=f"A service file for the machine {name} already exists: {service_path}")

	if qemu_config_path.exists():
		raise HTTPException(status_code=409, detail=f"A environment configuration file for the machine {name} already exists: {qemu_config_path}")

	base_hardware = DupeDict()
	base_hardware["cpu"] = info.cpu
	base_hardware["enable-kvm"] = info.enable_kvm
	base_hardware["machine"] = info.machine
	for device in info.devices:
		base_hardware["device"] = device
	base_hardware["m"] = info.memory
	for drive in info.drives:
		base_hardware["drive"] = drive

	pcie_buses = DupeDict() # There's already a default pcie.0 bus builtin to qemu.

	pcie_root_ports = DupeDict()
	for device in info.pcie_root_ports:
		pcie_root_ports["device"] = device

	pcie_slave_buses = DupeDict()
	for device in info.pcie_slave_buses:
		pcie_slave_buses["device"] = device

	pcie_slave_devices = DupeDict()
	for device in info.pcie_slave_devices:
		pcie_slave_devices["device"] = device

	scsi_index = 0
	boot_index = 0
	if info.harddrives:
		for drive_index, harddrive_info in enumerate(info.harddrives):
			image_name, size = harddrive_info
			image_format = pathlib.Path(image_name).suffix[1:]
			image_path = pathlib.Path(image_name).expanduser().absolute()

			if not image_path.exists():
				if (output := qemu_img(f"create -f {image_format} {image_path} {size}")).exit_code != 0:
					raise HTTPException(status_code=510, detail=f"Could not create test image {image_path}: {output}")

			pcie_root_ports["device"] = f"virtio-scsi-pci,bus=pcie.0,id=scsi{scsi_index}"
			pcie_slave_buses["device"] = f"scsi-hd,drive=hdd{drive_index},bus=scsi{scsi_index}.0,id=scsi{scsi_index}.0,bootindex={boot_index}"
			pcie_slave_devices["drive"] = f"file={image_path},if=none,format={image_format},discard=unmap,aio=native,cache=none,id=hdd{drive_index}"

			scsi_index += 1
			boot_index += 1

	if info.cdroms:
		for drive_index, image_name in enumerate(info.cdroms):
			image_path = pathlib.Path(image_name).expanduser().absolute()

			if not image_path.exists():
				raise HTTPException(status_code=510, detail=f"Could not locate ISO image {image_path}")

			pcie_root_ports["device"] = f"virtio-scsi-pci,bus=pcie.0,id=scsi{scsi_index}"
			pcie_slave_buses["device"] = f"scsi-cd,drive=cdrom{drive_index},bus=scsi{scsi_index}.0,id=scsi{scsi_index}.0,bootindex={boot_index}"
			pcie_slave_devices["drive"] = f"file={image_path},media=cdrom,if=none,format=raw,cache=none,id=cdrom{drive_index}"

			scsi_index += 1
			boot_index += 1

	qemu_string = create_qemu_string(name, info.namespace, base_hardware, pcie_buses, pcie_root_ports, pcie_slave_buses, pcie_slave_devices, graphics=info.graphics)
	verify_qemu_resources(name, base_hardware, pcie_buses, pcie_root_ports, pcie_slave_buses, pcie_slave_devices)

	with qemu_config_path.open('w') as config:
		config.write(json.dumps({
			"name": name,
			"namespace": info.namespace,
			"base_hardware": base_hardware,
			"pcie_buses": pcie_buses,
			"pcie_root_ports": pcie_root_ports,
			"pcie_slave_buses": pcie_slave_buses,
			"pcie_slave_devices": pcie_slave_devices,
			"interfaces": info.network
		}, cls=JSON))

	write_qemu_service_file(service_path, name, qemu_config_path, qemu_string, namespace=info.namespace)

	struct = {
		"name": name,
		"namespace": info.namespace,
		"base_hardware": base_hardware,
		"pcie_buses": pcie_buses,
		"pcie_root_ports": pcie_root_ports,
		"pcie_slave_buses": pcie_slave_buses,
		"pcie_slave_devices": pcie_slave_devices
	}
	result = {}
	for key, val in json.loads(json.dumps(struct, cls=JSON)).items():
		result[str(key)] = val

	return result


@app.put("/qemu/machine/{name}/string", tags=["qemu"])
def create_qemu_string_from_struct(name :str, info :NewVirtualMachine, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> str:
	"""
	This API can be used to create new virtual machines.
	This API will not create machine resources, but simply returns a QEMU string that can be called.
	"""

	base_hardware = DupeDict()
	base_hardware["cpu"] = info.cpu
	base_hardware["enable-kvm"] = info.enable_kvm
	base_hardware["machine"] = info.machine
	for device in info.devices:
		base_hardware["device"] = device
	base_hardware["m"] = info.memory
	for drive in info.drives:
		base_hardware["drive"] = drive

	pcie_buses = DupeDict() # There's already a default pcie.0 bus builtin to qemu.

	pcie_root_ports = DupeDict()
	for device in info.pcie_root_ports:
		pcie_root_ports["device"] = device

	pcie_slave_buses = DupeDict()
	for device in info.pcie_slave_buses:
		pcie_slave_buses["device"] = device

	pcie_slave_devices = DupeDict()
	for device in info.pcie_slave_devices:
		pcie_slave_devices["device"] = device

	return create_qemu_string(name, info.namespace, base_hardware, pcie_buses, pcie_root_ports, pcie_slave_buses, pcie_slave_devices)

@app.post("/qemu/machine/{name}/start", tags=["qemu"])
def start_qemu_machine(name :str, locations :ResourceLocations, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> None:
	"""
	This endpoint starts a qemu instance using a previously created service file with the given name.
	"""

	if locations.run_as == 'root':
		SysCommand(f"systemctl start {name}.service")
	else:
		SysCommand(f"systemctl --user start {name}.service")

@app.post("/qemu/machine/{name}/stop", tags=["qemu"])
def stop_qemu_machine(name :str, locations :ResourceLocations, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> None:
	"""
	This endpoint stops a qemu instance using a previously created service file with the given name.
	"""

	if locations.run_as == 'root':
		SysCommand(f"systemctl stop {name}.service")
	else:
		SysCommand(f"systemctl --user stop {name}.service")

@app.get("/qemu/machine/{name}/status", tags=["qemu"])
def status_qemu_machine(name :str, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> Dict[str, str]:
	"""
	This endpoint gets the service status of the machine.
	If the machine is missing or dead, it will return inactive.
	"""

	return {'status': str(SysCommand(f"systemctl -o json is-active postgresql {name}.service").decode())}

@app.patch("/qemu/machine/{name}/snapshot", tags=["qemu"])
def snapshot_qemu_machine(name :str, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> None:
	"""
	This endpoint enables you to take a snapshot of a machine's current state.
	If it's running the memory and all devices will be snapshotted using the builtin qemu snapshot tool.
	If the machine is at rest and the disk volumes are of format qcow2 (or stored on a btrfs/zfs storage) those
	will be snapshotted manually instead.
	"""

	raise HTTPException(status_code=501, detail="Not yet implemented")

@app.patch("/qemu/machine/{name}/migrate", tags=["qemu"])
def migrate_qemu_machine(name :str, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> None:
	"""
	This endpoint enables you to migrate the machine to a different cluster.
	"""

	raise HTTPException(status_code=501, detail="Not yet implemented")

@app.post("/qemu/machine/{name}/export", tags=["qemu"])
def export_qemu_machine(name :str, current_user: User = Security(process_user_claim, scopes=["qemu*"])) -> None:
	"""
	This endpoint enables you to export either the configuration or to do a full export including devices.
	"""

	raise HTTPException(status_code=501, detail="Not yet implemented")