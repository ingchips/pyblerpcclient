from ble_rpc_client.brpc import *
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *
from ble_rpc_client import brpc
from ble_rpc_client.log import LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL
from ble_rpc_client import gatt_client_util

import asyncio

class SyncRunner:
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.m = queue.Queue()
        self.RUN = True
        self.thread = threading.Thread(target=lambda : self.run())
        self.thread.start()
        self.create_conn_pending = False

    def abort(self) -> None:
        self.RUN = False

    def run(self) -> None:
        while RUN:
            try:
                f = self.q.get(timeout=0.5)
                f()
            except:
                pass

    def push_function(self, f) -> None:
        self.q.put(f)

    def push_result(self, result) -> None:
        self.m.put(result)

    def wait_result(self, timeout: float | None = None) -> Any:
        return self.m.get(timeout=timeout)

_runner = None

def init():
    global _runner
    if _runner is not None: return

    _runner = SyncRunner()

    def user_packet_handler(packet_type: BTStackPacketType,
                        channel: int,
                        packet: bytes) -> None:

        if packet_type != BTStackPacketType.HCI_EVENT_PACKET:
            return

        event = hci_event_decode(packet)
        match event:
            case HciEventLeMeta():
                meta = event.evt
                match meta:
                    case HciSubEventLeEnhancedConnectionComplete():
                        if _runner.create_conn_pending:
                            _runner.push_result(meta)
                            _runner.create_conn_pending = False

    hci_add_event_handler(user_packet_handler)

def run(fun: Callable[[], None]) -> None:
    init()
    _runner.push_function(fun)

def gatt_client_sync_discover_all(con_handle: hci_con_handle) -> list[gatt_client_util.Service] | None:
    def callback(all):
        _runner.push_result(all)

    if gatt_client_util.gatt_client_util_discover_all(con_handle, callback) != 0:
        return None

    return _runner.wait_result()

def gatt_client_sync_read_value_of_characteristic(con_handle: hci_con_handle,
    characteristic_value_handle: int) -> bytes | None:
    value = None

    def callback(packet_type: BTStackPacketType, channel: int, packet: bytes):
        nonlocal value
        evt = gatt_client_util.gatt_client_decode_event(packet)
        match evt:
            case gatt_client_util.GattEventCharacteristicValueQueryResult():
                value = evt.value
            case gatt_client_util.GattEventQueryComplete():
                if evt.status == 0:
                    _runner.push_result(value)
                else:
                    _runner.push_result(Exception(f"status = {evt.status}"))

    if gatt_client_read_value_of_characteristic_using_value_handle(callback,
                                                                con_handle,
                                                                characteristic_value_handle) != 0:
        return None

    return _runner.wait_result()

def gatt_client_sync_read_characteristic_descriptor(con_handle: hci_con_handle,
    descriptor_handle: int) -> bytes | None:
    value = None

    def callback(packet_type: BTStackPacketType, channel: int, packet: bytes):
        nonlocal value
        evt = gatt_client_util.gatt_client_decode_event(packet)
        match evt:
            case gatt_client_util.GattEventCharacteristicDescriptorQueryResult():
                value = evt.value
            case gatt_client_util.GattEventQueryComplete():
                if evt.status == 0:
                    _runner.push_result(value)
                else:
                    _runner.push_result(Exception(f"status = {evt.status}"))

    if gatt_client_read_characteristic_descriptor_using_descriptor_handle(callback,
                                                                con_handle,
                                                                descriptor_handle) != 0:
        return None

    return _runner.wait_result()

def gatt_client_sync_write_value_of_characteristic(con_handle: hci_con_handle,
    characteristic_value_handle: int, data: bytes) -> int:

    def callback(packet_type: BTStackPacketType, channel: int, packet: bytes):
        evt = gatt_client_util.gatt_client_decode_event(packet)
        match evt:
            case gatt_client_util.GattEventQueryComplete():
                _runner.push_result(evt.status)

    r = gatt_client_write_value_of_characteristic(callback,
                                                 con_handle,
                                                 characteristic_value_handle, data)
    if r != 0: return r

    return _runner.wait_result()

def gatt_client_sync_write_characteristic_descriptor(con_handle: hci_con_handle,
    descriptor_handle: int, data: bytes) -> int:

    def callback(packet_type: BTStackPacketType, channel: int, packet: bytes):
        evt = gatt_client_util.gatt_client_decode_event(packet)
        match evt:
            case gatt_client_util.GattEventQueryComplete():
                _runner.push_result(evt.status)

    r = gatt_client_write_characteristic_descriptor_using_descriptor_handle(callback,
                                                 con_handle,
                                                 descriptor_handle, data)
    if r != 0: return r

    return _runner.wait_result()

def gap_sync_ext_create_connection(filter_policy: initiating_filter_policy,
        own_addr_type: bd_addr_type,
        peer_addr_type: bd_addr_type,
        peer_addr: bd_addr,
        phy_configs: List[initiating_phy_config],
        timeout: float | None = None) -> HciSubEventLeEnhancedConnectionComplete | None:

    assert not _runner.create_conn_pending

    r = gap_ext_create_connection(filter_policy, own_addr_type, peer_addr_type, peer_addr, phy_configs)
    _runner.create_conn_pending = True
    if r != 0:
        _runner.create_conn_pending = False
        return None

    try:
        return _runner.wait_result(timeout)
    except:
        # timeout
        assert gap_create_connection_cancel() == 0
        return _runner.wait_result()

