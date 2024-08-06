from ble_rpc_client.brpc import *
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *
import ble_rpc_client.bt_defs
from ble_rpc_client import brpc
from ble_rpc_client.log import LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL
from ble_rpc_client import sig_uuid

def decode_properties(v):
    r = []
    if (v & 0x1):
        r.append("broadcast")
    if (v & 0x2):
        r.append("read")
    if (v & 0x4):
        r.append("writeWithoutResponse")
    if (v & 0x8):
        r.append("write")
    if (v & 0x10):
        r.append("notify")
    if (v & 0x20):
        r.append("indicate")
    if (v & 0x40):
        r.append("authWrite")
    if (v & 0x80):
        r.append("extendedProperties")
    return f"0x{v:04x} (" + ', '.join(r) + ")"

class Descriptor:
    def __init__(self, uuid: bytes | int, handle: int) -> None:
        self.uuid = UUID(uuid)
        self.handle = handle

    def __str__(self) -> str:
        return f"""Descriptor: {self.uuid} HANDLE : {self.handle}"""

class Characteristic:
    def __init__(self, uuid: bytes | int, start_handle: int, value_handle: int, end_handle: int, properties: int) -> None:
        self.uuid = UUID(uuid)
        self.start_handle = start_handle
        self.end_handle = end_handle
        self.value_handle = value_handle
        self.properties = properties
        self.descriptors: list[Descriptor] = []

    def __str__(self) -> str:
        return f"""Characteristic: {self.uuid} [{self.start_handle}-{self.end_handle}], {self.value_handle}, {decode_properties(self.properties)}\n""" + \
                '\n'.join([str(desc) for desc in self.descriptors])

    def to_gatt_client_characteristic(self) -> gatt_client_characteristic:
        return gatt_client_characteristic(self.start_handle, self.value_handle, self.end_handle, self.properties, self.uuid.uuid)

class Service:
    def __init__(self, uuid: bytes | int, start_group_handle: int, end_group_handle: int) -> None:
        self.uuid = UUID(uuid)
        self.start_group_handle = start_group_handle
        self.end_group_handle = end_group_handle
        self.characteristics: list[Characteristic] = []

    def __str__(self) -> str:
        return f"""Service: {self.uuid} [{self.start_group_handle}-{self.end_group_handle}]\n""" + \
                '\n'.join([str(chara) for chara in self.characteristics])

class GattEventQueryComplete:
    def __init__(self, packet) -> None:
        self.handle, self.status = struct.unpack('<HB', packet)

    def __str__(self) -> str:
        return f"GattEventQueryComplete #{self.handle}: {self.status}"

class GattEventServiceQueryResult:
    def __init__(self, packet) -> None:
        self.handle, start_group_handle, end_group_handle, uuid = struct.unpack('<HHH16s', packet)
        self.service = Service(uuid, start_group_handle, end_group_handle)

class GattEventCharacteristicQueryResult:
    def __init__(self, packet) -> None:
        self.handle, start_handle, value_handle, end_handle, properties, uuid = struct.unpack('<HHHHH16s', packet)
        self.characteristic = Characteristic(uuid, start_handle, value_handle, end_handle, properties)

class GattEventCharacteristicValueQueryResult:
    def __init__(self, packet) -> None:
        self.handle, self.value_handle = struct.unpack('<HH', packet[:4])
        self.value = packet[4:]

class GattEventCharacteristicDescriptorQueryResult:
    def __init__(self, packet) -> None:
        self.handle, self.descriptor_handle = struct.unpack('<HH', packet[:4])
        self.value = packet[4:]

class GattEventDescriptorQueryResult:
    def __init__(self, packet) -> None:
        self.handle, handle, uuid = struct.unpack('<HH16s', packet)
        self.descriptor = Descriptor(uuid, handle)

class GattEventNotification:
    def __init__(self, packet) -> None:
        self.handle, = struct.unpack('<H', packet[:2])
        self.value = packet[2:]

    def __str__(self) -> str:
        return f"Notification #{self.handle}: {self.value.hex()}"

class GattEventIndication:
    def __init__(self, packet) -> None:
        self.handle, = struct.unpack('<H', packet[:2])
        self.value = packet[2:]

    def __str__(self) -> str:
        return f"Indication #{self.handle}: {self.value.hex()}"

def gatt_client_decode_event(packet: bytes) -> Any:
    code = packet[0]
    param = packet[2:]
    match code:
        case bt_defs.GATT_EVENT_QUERY_COMPLETE:
            return GattEventQueryComplete(param)
        case bt_defs.GATT_EVENT_SERVICE_QUERY_RESULT:
            return GattEventServiceQueryResult(param)
        case bt_defs.GATT_EVENT_CHARACTERISTIC_QUERY_RESULT:
            return GattEventCharacteristicQueryResult(param)
        case bt_defs.GATT_EVENT_ALL_CHARACTERISTIC_DESCRIPTORS_QUERY_RESULT:
            return GattEventDescriptorQueryResult(param)
        case bt_defs.GATT_EVENT_NOTIFICATION:
            return GattEventNotification(param)
        case bt_defs.GATT_EVENT_INDICATION:
            return GattEventIndication(param)
        case bt_defs.GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT:
            return GattEventCharacteristicValueQueryResult(param)
        case bt_defs.GATT_EVENT_CHARACTERISTIC_DESCRIPTOR_QUERY_RESULT:
            return GattEventCharacteristicDescriptorQueryResult(param)
        case other:
            raise Exception(f"gatt_client_code_event: not implemented for {code}")

def gatt_client_util_discover_all(con_handle: hci_con_handle, callback: Callable[[list[Service]], None]) -> int:
    r = []
    pending_service: list[Service] = []
    pending_characteristics: list[Characteristic] = []

    def trigger_action():
        if len(pending_characteristics) > 0:
            gatt_client_discover_characteristic_descriptors(on_descriptor_discovered,
                                                            con_handle,
                                                            characteristic=pending_characteristics[0].to_gatt_client_characteristic())
        else:
            r.append(pending_service[0])
            pending_service.pop(0)
            if len(pending_service) > 0:
                gatt_client_discover_characteristics_for_service(on_characteristics_discovered,
                                                                con_handle,
                                                                start_group_handle=pending_service[0].start_group_handle,
                                                                end_group_handle=pending_service[0].end_group_handle)
            else:
                callback(r)

    def on_descriptor_discovered(packet_type: BTStackPacketType, channel: int, packet: bytes):
        evt = gatt_client_decode_event(packet)
        match evt:
            case GattEventDescriptorQueryResult():
                pending_characteristics[0].descriptors.append(evt.descriptor)
            case GattEventQueryComplete():
                if evt.status != 0:
                    LOG_E(f'gatt_client_discover_characteristic_descriptors: {evt.status}')
                pending_service[0].characteristics.append(pending_characteristics[0])
                pending_characteristics.pop(0)
                trigger_action()

    def on_characteristics_discovered(packet_type: BTStackPacketType, channel: int, packet: bytes):
        evt = gatt_client_decode_event(packet)
        match evt:
            case GattEventCharacteristicQueryResult():
                pending_characteristics.append(evt.characteristic)
            case GattEventQueryComplete():
                if evt.status != 0:
                    LOG_E(f'gatt_client_discover_characteristics_for_service: {evt.status}')
                trigger_action()
            case other:
                LOG_E(f"unexpected evt: {evt}")

    def on_service_discovered(packet_type: BTStackPacketType, channel: int, packet: bytes):
        evt = gatt_client_decode_event(packet)
        match evt:
            case GattEventServiceQueryResult():
                pending_service.append(evt.service)
            case GattEventQueryComplete():
                if evt.status != 0:
                    LOG_E(f'gatt_client_discover_primary_services: {evt.status}')

                if len(pending_service) > 0:
                    gatt_client_discover_characteristics_for_service(on_characteristics_discovered,
                                                                    con_handle,
                                                                    start_group_handle=pending_service[0].start_group_handle,
                                                                    end_group_handle=pending_service[0].end_group_handle)
                else:
                    callback(r)
            case other:
                LOG_E(f"unexpected evt: {evt}")

    return gatt_client_discover_primary_services(on_service_discovered, con_handle)

def gatt_client_util_find_char(services: list[Service], value_handle: int) -> Characteristic | None:
    for s in services:
        for c in s.characteristics:
            if c.value_handle == value_handle:
                return c
    return None

def gatt_client_util_find_char_uuid(services: list[Service], uuid: int | bytes) -> Characteristic | None:
    uuid128 = UUID.normalize(uuid=uuid)
    for s in services:
        for c in s.characteristics:
            if c.uuid.uuid == uuid128:
                return c
    return None

def gatt_client_util_find_config_desc(c: Characteristic) -> Descriptor | None:
    for desc in c.descriptors:
        if desc.uuid.is_sig_uuid(sig_uuid.SIG_UUID_DESCRIP_GATT_CLIENT_CHARACTERISTIC_CONFIGURATION):
            return desc
    return None