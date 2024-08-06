from ble_rpc_client.brpc import *
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *
import ble_rpc_client.bt_defs
from ble_rpc_client import brpc
from ble_rpc_client.log import LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL
import math

from ble_rpc_client.gatt_client_util import *
from ble_rpc_client.btstack_sync import *
from ble_rpc_client import btstack_sync
import asyncio

SIG_UUID_CHARACT_TEMPERATURE_MEASUREMENT = 0x2a1c

def att_read_callback(connection_handle: hci_con_handle | int,
                      att_handle: int,
                      offset: int) -> bytes | int:
    return b''

def att_write_callback(conn_handle: hci_con_handle | int,
                       att_handle: int,
                       transaction_mode: int,
                       offset: int,
                       buffer: bytes) -> None:
    pass

def on_data(packet_type: BTStackPacketType, channel: int, packet: bytes):
    LOG_I(gatt_client_decode_event(packet=packet))

def synced_test() -> None:
    complete = gap_sync_ext_create_connection(initiating_filter_policy.INITIATING_ADVERTISER_FROM_PARAM,
                                      bd_addr_type.RANDOM,
                                      bd_addr_type.RANDOM,
                                      bd_addr('CD:A3:28:11:89:3F'),
                                      [
                                          initiating_phy_config(
                                              phy_type.PHY_1M,
                                              conn_para(
                                                  scan_int=200,
                                                  scan_win=100,
                                                  interval_min=30,
                                                  interval_max=30,
                                                  latency=0,
                                                  supervision_timeout=100,
                                                  min_ce_len=90,
                                                  max_ce_len=90
                                              )
                                            )
                                      ],
                                    5.0)
    if complete.status != 0:
        LOG_E(f"failed to connected to peer: {complete.status}")
        return

    LOG_OK(f'connected to {complete.peer_addr}')
    con_handle = complete.handle

    all = gatt_client_sync_discover_all(con_handle)
    c = gatt_client_util_find_char_uuid(all, SIG_UUID_CHARACT_TEMPERATURE_MEASUREMENT)
    if c is None:
        LOG_E("service not found")
        return

    d = gatt_client_util_find_config_desc(c)
    if d is None:
        LOG_E("descriptor not found")
        return

    gatt_client_listen_for_characteristic_value_updates(on_data, con_handle, c.value_handle)
    assert gatt_client_sync_write_characteristic_descriptor(con_handle, d.handle, GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION) == 0

def user_packet_handler(packet_type: BTStackPacketType,
                        channel: int,
                        packet: bytes) -> None:

    if packet_type != BTStackPacketType.HCI_EVENT_PACKET:
        return

    event = hci_event_decode(packet)
    match event:
        case BtStackEventState():

            if event.state != HCI_STATE.HCI_STATE_WORKING:
                return

            gap_set_random_device_address(bd_addr('CD:12:23:56:78:EF'))

            btstack_sync.run(lambda: synced_test())

        case HciEventCommandComplete():
            LOG_D(f'Command Complete: opcode = {event.opcode}, ret = {event.return_parameters}')
            if (len(event.return_parameters) > 1) and (event.return_parameters[0] != 0):
                LOG_E(f'Command Complete: opcode = {event.opcode}, ret = {event.return_parameters}')

        case HciEventCommandStatus():
            if event.status != 0:
                LOG_E(f'Command status: opcode = {event.opcode}, status = {event.status}')

        case HciEventDisconnectionComplete():
            LOG_PROG(f'disconnected: reason = {event.reason}')

        case AttEventMtuExchangeComplete():
            global the_mtu
            the_mtu = event.mtu - 3
            LOG_I(f'MTU -> {the_mtu}')

        case HciEventReadRemoteVersionInformationComplete():
            LOG_OK(f"""Remote Version: Status = {event.status}
    Connection   = {event.conn_handle}
    Version      = {event.version}
    Manufacturer = {event.manufacturer_name}
    Subversion   = {event.subversion}""")

def setup_profile():
    att_server_init(att_read_callback, att_write_callback)
    hci_add_event_handler(user_packet_handler)
    att_server_register_packet_handler(user_packet_handler)

if __name__ == '__main__':
    brpc.start(setup_profile)