import os, sys
import time

from ble_rpc_client.brpc import *
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *
import ble_rpc_client.bt_defs
from ble_rpc_client import brpc
from ble_rpc_client.log import LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL

the_mtu = 20

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

def setup_non_conn_adv(addr) -> None:
    adv_data = bytes([# 0x01 - «Flags»
                    2, 0x01,
                    0x00,

                    #0x09 - «Complete Local Name»
                    6, 0x09,
                    0x53, 0x68, 0x65, 0x6C, 0x6C,
                    ])
    gap_set_adv_set_random_addr(0, bd_addr(addr))
    gap_set_ext_adv_para(0,
                        adv_event_property.ADV_LEGACY,
                        0x00a1, 0x00a1,            # Primary_Advertising_Interval_Min, Primary_Advertising_Interval_Max
                        adv_channel_bit.PRIMARY_ADV_ALL_CHANNELS,  # Primary_Advertising_Channel_Map
                        bd_addr_type.RANDOM,    # Own_Address_Type
                        bd_addr_type.PUBLIC,    # Peer_Address_Type (ignore)
                        bd_addr(b''),           # Peer_Address      (ignore)
                        adv_filter_policy.ADV_FILTER_ALLOW_ALL,      # Advertising_Filter_Policy
                        0x00,                   # Advertising_Tx_Power
                        phy_type.PHY_1M,        # Primary_Advertising_PHY
                        0,                      # Secondary_Advertising_Max_Skip
                        phy_type.PHY_1M,        # Secondary_Advertising_PHY
                        0x00,                   # Advertising_SID
                        0x00)                   # Scan_Request_Notification_Enable
    gap_set_ext_adv_data(0, adv_data)
    gap_set_ext_scan_response_data(0, b'')
    gap_set_ext_adv_enable(1, [ext_adv_set_en(0, 0, 0)])

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

        case HciEventLeMeta():
            meta = event.evt
            match meta:
                case HciSubEventLeEnhancedConnectionComplete():
                    LOG_OK(f'connected to {meta.peer_addr}')
                    att_set_db(meta.handle, profile_data)
                    gap_read_remote_version(meta.handle)

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

class IUTHandler():
    def __init__(self, tester = None):
        self._iut_address = 'C00000000916'

    def _preinit(self):
        pass

    def _postmmi(self, mmi_function, params):
        pass

    def _init(self, param):
        LOG_PROG("init IUT")
        btstack_push_user_runnable(lambda: platform_reset())

    def _post(self):
        LOG_PROG("stopping IUT")
        btstack_push_user_runnable(lambda: platform_reset())

    def mmi_5(self, args):
        btstack_push_user_runnable(lambda: setup_non_conn_adv(self._iut_address))
        time.sleep(0.5)
        return b'OK'

if __name__ == '__main__':
    import implicitsend_server
    signal.signal(signal.SIGINT, signal_handler)
    brpc.start_detached(setup_profile)
    handler = IUTHandler()
    implicitsend_server.start_server(iut_handler=handler)