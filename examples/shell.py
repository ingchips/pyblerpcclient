from ble_rpc_client.brpc import *
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *
import ble_rpc_client.bt_defs
from ble_rpc_client import brpc
from ble_rpc_client.log import LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL
import math

profile_data = bytes([
    # Service INGChips Console Service: {43f4b114-ca67-48e8-a46f-9a8ffeb7146a}
    0x18, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x28,
    0x6A, 0x14, 0xB7, 0xFE, 0x8F, 0x9A, 0x6F, 0xA4,
    0xE8, 0x48, 0x67, 0xCA, 0x14, 0xB1, 0xF4, 0x43,
    # Characteristic Generic Input: {bf83f3f1-399a-414d-9035-ce64ceb3ff67}
    0x1B, 0x00, 0x02, 0x00, 0x02, 0x00, 0x03, 0x28,
    0x06, 0x03, 0x00, 0x67, 0xFF, 0xB3, 0xCE, 0x64,
    0xCE, 0x35, 0x90, 0x4D, 0x41, 0x9A, 0x39, 0xF1,
    0xF3, 0x83, 0xBF,
    0x16, 0x00, 0x06, 0x03, 0x03, 0x00,
    0x67, 0xFF, 0xB3, 0xCE, 0x64, 0xCE, 0x35, 0x90,
    0x4D, 0x41, 0x9A, 0x39, 0xF1, 0xF3, 0x83, 0xBF,
    # Characteristic Generic Output: {bf83f3f2-399a-414d-9035-ce64ceb3ff67}
    0x1B, 0x00, 0x02, 0x00, 0x04, 0x00, 0x03, 0x28,
    0x10, 0x05, 0x00, 0x67, 0xFF, 0xB3, 0xCE, 0x64,
    0xCE, 0x35, 0x90, 0x4D, 0x41, 0x9A, 0x39, 0xF2,
    0xF3, 0x83, 0xBF,
    0x16, 0x00, 0x10, 0x02, 0x05, 0x00,
    0x67, 0xFF, 0xB3, 0xCE, 0x64, 0xCE, 0x35, 0x90,
    0x4D, 0x41, 0x9A, 0x39, 0xF2, 0xF3, 0x83, 0xBF,
    # Descriptor Client Characteristic Configuration: 2902
    0x0A, 0x00, 0x0A, 0x01, 0x06, 0x00, 0x02, 0x29,
    0x00, 0x00,

    0x00,0x00
    ])

HANDLE_GENERIC_INPUT                              =   3
HANDLE_GENERIC_OUTPUT                             =   5
HANDLE_GENERIC_OUTPUT_CLIENT_CHAR_CONFIG          =   6

the_mtu = 20

def evaluate_bytes(input_bytes):
    try:
        input = input_bytes[0:-1].decode('utf-8')
        LOG_D(f"evaluate_bytes: {input}")
        result = eval(input)
        result_bytes = str(result).encode('utf-8')
        return result_bytes
    except Exception as e:
        return str(e).encode('utf-8')

def att_read_callback(connection_handle: hci_con_handle | int,
                      att_handle: int,
                      offset: int) -> bytes | int:
    return b''

def att_write_callback(conn_handle: hci_con_handle | int,
                       att_handle: int,
                       transaction_mode: int,
                       offset: int,
                       buffer: bytes) -> None:

    if att_handle ==HANDLE_GENERIC_INPUT:
        result = evaluate_bytes(buffer)
        att_server_notify_long_data(conn_handle, HANDLE_GENERIC_OUTPUT, result, the_mtu)

def setup_adv() -> None:
    adv_data = bytes([# 0x01 - «Flags»
                    2, 0x01,
                    0x06,

                    #0x09 - «Complete Local Name»
                    6, 0x09,
                    0x53, 0x68, 0x65, 0x6C, 0x6C,
                    ])
    gap_set_adv_set_random_addr(0, bd_addr('CD:12:23:56:78:EF'))
    gap_set_ext_adv_para(0,
                        adv_event_property.ADV_CONNECTABLE | adv_event_property.ADV_SCANNABLE | adv_event_property.ADV_LEGACY,
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

            setup_adv()

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

if __name__ == '__main__':
    brpc.start(setup_profile)