from enum import IntEnum
import struct
from typing import Any, Callable

BRPC_VERSION = 3

HCI_EVENT_PACKET = 0x04
UUID128_LEN = 16

ATT_DEFERRED_READ = 0xffff

BTSTACK_EVENT_STATE = 0x60
ATT_EVENT_CAN_SEND_NOW = 0xB7
BTSTACK_EVENT_USER_MSG = 0xFF

HCI_EVENT_DISCONNECTION_COMPLETE                   = 0x05
HCI_EVENT_AUTHENTICATION_COMPLETE_EVENT            = 0x06
HCI_EVENT_ENCRYPTION_CHANGE                        = 0x08
HCI_EVENT_READ_REMOTE_VERSION_INFORMATION_COMPLETE = 0x0C
HCI_EVENT_COMMAND_COMPLETE                         = 0x0E
HCI_EVENT_COMMAND_STATUS                           = 0x0F
HCI_EVENT_HARDWARE_ERROR                           = 0x10
HCI_EVENT_NUMBER_OF_COMPLETED_PACKETS              = 0x13
HCI_EVENT_LE_META                                  = 0x3E
L2CAP_EVENT_CHANNEL_OPENED                         = 0x70
L2CAP_EVENT_CHANNEL_CLOSED                         = 0x71
L2CAP_EVENT_INCOMING_CONNECTION                    = 0x72
L2CAP_EVENT_TIMEOUT_CHECK                          = 0x73
L2CAP_EVENT_CONNECTION_PARAMETER_UPDATE_REQUEST    = 0x76
L2CAP_EVENT_CONNECTION_PARAMETER_UPDATE_RESPONSE   = 0x77
L2CAP_EVENT_CAN_SEND_NOW                           = 0x78
L2CAP_EVENT_COMMAND_REJECT_RESPONSE                = 0x79
L2CAP_EVENT_COMPLETED_SDU_PACKET                   = 0x7A
L2CAP_EVENT_FRAGMENT_SDU_PACKET                    = 0x7B
GATT_EVENT_QUERY_COMPLETE                              = 0xA0
GATT_EVENT_SERVICE_QUERY_RESULT                        = 0xA1
GATT_EVENT_CHARACTERISTIC_QUERY_RESULT                 = 0xA2
GATT_EVENT_INCLUDED_SERVICE_QUERY_RESULT               = 0xA3
GATT_EVENT_ALL_CHARACTERISTIC_DESCRIPTORS_QUERY_RESULT = 0xA4
GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT           = 0xA5
GATT_EVENT_LONG_CHARACTERISTIC_VALUE_QUERY_RESULT      = 0xA6
GATT_EVENT_NOTIFICATION                                = 0xA7
GATT_EVENT_INDICATION                                  = 0xA8
GATT_EVENT_CHARACTERISTIC_DESCRIPTOR_QUERY_RESULT      = 0xA9
GATT_EVENT_LONG_CHARACTERISTIC_DESCRIPTOR_QUERY_RESULT = 0xAA
GATT_EVENT_MTU                                     = 0xAB
ATT_EVENT_MTU_EXCHANGE_COMPLETE                    = 0xB5
ATT_EVENT_HANDLE_VALUE_INDICATION_COMPLETE         = 0xB6
ATT_EVENT_CAN_SEND_NOW                             = 0xB7
SM_EVENT_JUST_WORKS_REQUEST                        = 0xD0
SM_EVENT_JUST_WORKS_CANCEL                         = 0xD1
SM_EVENT_PASSKEY_DISPLAY_NUMBER                    = 0xD2
SM_EVENT_PASSKEY_DISPLAY_CANCEL                    = 0xD3
SM_EVENT_PASSKEY_INPUT_NUMBER                      = 0xD4
SM_EVENT_PASSKEY_INPUT_CANCEL                      = 0xD5
SM_EVENT_IDENTITY_RESOLVING_STARTED                = 0xD6
SM_EVENT_IDENTITY_RESOLVING_FAILED                 = 0xD7
SM_EVENT_IDENTITY_RESOLVING_SUCCEEDED              = 0xD8
SM_EVENT_AUTHORIZATION_REQUEST                     = 0xD9
SM_EVENT_AUTHORIZATION_RESULT                      = 0xDA
SM_EVENT_PRIVATE_RANDOM_ADDR_UPDATE                = 0xDB
SM_EVENT_STATE_CHANGED                             = 0xDC
BTSTACK_EVENT_USER_MSG                             = 0xFF

HCI_SUBEVENT_LE_CONNECTION_COMPLETE                 = 0x01
HCI_SUBEVENT_LE_ADVERTISING_REPORT                  = 0x02
HCI_SUBEVENT_LE_CONNECTION_UPDATE_COMPLETE          = 0x03
HCI_SUBEVENT_LE_READ_REMOTE_USED_FEATURES_COMPLETE  = 0x04
HCI_SUBEVENT_LE_LONG_TERM_KEY_REQUEST               = 0x05
HCI_SUBEVENT_LE_REMOTE_CONNECTION_PARAMETER_REQUEST_COMPLETE = 0x06
HCI_SUBEVENT_LE_DATA_LENGTH_CHANGE_EVENT          = 0x07
HCI_SUBEVENT_LE_P256_PUB_KEY_COMPLETE             = 0x08
HCI_SUBEVENT_LE_GENERATE_DHKEY_COMPLETE           = 0x09
HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE      = 0x0A
HCI_SUBEVENT_LE_DIRECT_ADVERTISING_REPORT         = 0x0B
HCI_SUBEVENT_LE_PHY_UPDATE_COMPLETE               = 0X0C
HCI_SUBEVENT_LE_EXTENDED_ADVERTISING_REPORT       = 0X0D
HCI_SUBEVENT_LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED = 0X0E
HCI_SUBEVENT_LE_PERIODIC_ADVERTISING_REPORT       =  0X0F
HCI_SUBEVENT_LE_PERIODIC_ADVERTISING_SYNC_LOST    =  0X10
HCI_SUBEVENT_LE_SCAN_TIMEOUT                      =  0X11
HCI_SUBEVENT_LE_ADVERTISING_SET_TERMINATED        =  0X12
HCI_SUBEVENT_LE_SCAN_REQUEST_RECEIVED             =  0X13
HCI_SUBEVENT_LE_CHANNEL_SELECTION_ALGORITHM       =  0X14
HCI_SUBEVENT_LE_CONNECTIONLESS_IQ_REPORT          =  0x15
HCI_SUBEVENT_LE_CONNECTION_IQ_REPORT              =  0x16
HCI_SUBEVENT_LE_CTE_REQ_FAILED                    =  0x17
HCI_SUBEVENT_LE_PRD_ADV_SYNC_TRANSFER_RCVD        =  0x18
HCI_SUBEVENT_LE_CIS_ESTABLISHED                   =  0x19
HCI_SUBEVENT_LE_CIS_REQUEST                       =  0x1a
HCI_SUBEVENT_LE_CREATE_BIG_COMPLETE               =  0x1b
HCI_SUBEVENT_LE_TERMINATE_BIG_COMPLETE            =  0x1c
HCI_SUBEVENT_LE_BIG_SYNC_ESTABLISHED              =  0x1d
HCI_SUBEVENT_LE_BIG_SYNC_LOST                     =  0x1e
HCI_SUBEVENT_LE_REQUEST_PEER_SCA                  =  0x1F
HCI_SUBEVENT_LE_PATH_LOSS_THRESHOLD               =  0x20
HCI_SUBEVENT_LE_TRANSMIT_POWER_REPORTING          =  0x21
HCI_SUBEVENT_LE_BIGINFO_ADV_REPORT                =  0x22
HCI_SUBEVENT_LE_SUBRATE_CHANGE                    =  0x23
HCI_SUBEVENT_LE_VENDOR_CHANNEL_MAP_UPDATE            =  0xFE
HCI_SUBEVENT_LE_VENDOR_PRO_CONNECTIONLESS_IQ_REPORT  =  0xFF

GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NONE          = b'\x00\x00'
GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION  = b'\x01\x00'
GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_INDICATION    = b'\x02\x00'

class HCI_STATE(IntEnum):
    HCI_STATE_OFF = 0
    HCI_STATE_INITIALIZING = 1
    HCI_STATE_WORKING = 2
    HCI_STATE_HALTING = 3
    HCI_STATE_SLEEPING = 4
    HCI_STATE_FALLING_ASLEEP = 5

class ObjectAddressSimulation:
    def __init__(self) -> None:
        self.addr_to_object = {}
        self.object_to_addr = {}
        self.addr_start = 0x8000

    # CAUTION of wrapping although practically impossible
    def make_unique_address(self) -> int:
        k = self.addr_start
        self.addr_start = (k + 1) & 0xffffffff
        return k

    def address_of_object(self, obj: Any) -> int:
        if obj in self.object_to_addr:
            return self.object_to_addr[obj]
        else:
            k = self.make_unique_address()
            self.object_to_addr[obj] = k
            self.addr_to_object[k] = obj
            return k

    def object_of_address(self, addr: int) -> Any:
        if addr in self.addr_to_object:
            return self.addr_to_object[addr]
        else:
            raise Exception(f'object @{addr} is not allocated')

ObjectSim: ObjectAddressSimulation = ObjectAddressSimulation()

class uint8:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<B', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<B', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

class int8:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<b', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<b', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

class uint16:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<H', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<H', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

class int16:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<h', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<h', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

class uint32:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<I', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<I', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

class uint64:
    def __init__(self, v: int) -> None:
        self.v = v

    def encode(self) -> bytes:
        return struct.pack('<I', self.v)

    @staticmethod
    def deserialize(data: bytes) -> int:
        v, = struct.unpack('<Q', data)
        return v

    def __str__(self) -> str:
        return f'{self.v}>'

uintptr = uint32
hci_con_handle = uint16
adv_event_properties = uint8
adv_channel_bits = uint8
adv_event_properties = uint8
periodic_adv_properties = uint8
kvkey = uint8
phy_bittypes = uint8

class BTStackPacketType(IntEnum):
    HCI_COMMAND_DATA_PACKET = 0x01
    HCI_ACL_DATA_PACKET     = 0x02
    HCI_EVENT_PACKET        = 0x04
    L2CAP_EVENT_PACKET      = 0x0A

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

# parameters:
#   packet_type: BTStackPacketType,
#   channel: int,
#   packet: bytes
btstack_packet_handler_t = Callable[[BTStackPacketType | int, int, bytes], None]
user_packet_handler_t = btstack_packet_handler_t

# return_params: bytes, user_data: Any
gap_hci_cmd_complete_cb_t = Callable[[bytes, Any], None]

class adv_channel_bit(IntEnum):
    PRIMARY_ADV_CH_37 = 1
    PRIMARY_ADV_CH_38 = 2
    PRIMARY_ADV_CH_39 = 4
    PRIMARY_ADV_ALL_CHANNELS = 7

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class adv_event_property(IntEnum):
    ADV_CONNECTABLE = 1 << 0
    ADV_SCANNABLE = 1 << 1
    ADV_DIRECT = 1 << 2
    ADV_HIGH_DUTY_DIR_ADV = 1 << 3
    ADV_LEGACY = 1 << 4
    ADV_ANONYMOUS = 1 << 5
    ADV_INC_TX_POWER = 1 << 6

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class adv_filter_policy(IntEnum):
    ADV_FILTER_ALLOW_ALL = 0x00
    ADV_FILTER_ALLOW_SCAN_WLST_CON_ALL = 0x01
    ADV_FILTER_ALLOW_SCAN_ALL_CON_WLST = 0x02
    ADV_FILTER_ALLOW_SCAN_WLST_CON_WLST = 0x03

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class authorization_state: ...

class authorization_state(IntEnum):
    AUTHORIZATION_UNKNOWN = 0
    AUTHORIZATION_PENDING = 1
    AUTHORIZATION_DECLINED = 2
    AUTHORIZATION_GRANTED = 3

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

    @staticmethod
    def deserialize(data: bytes) -> authorization_state:
        id, = struct.unpack('<B', data)
        return authorization_state(id)

class bd_addr:
    def __init__(self, s: str | bytes):
        if isinstance(s, str):
            if ':' in s:
                self.v = bytes([int(x, 16) for x in s.split(':')])
            else:
                self.v = bytes.fromhex(s)
            self.check()
        elif isinstance(s, bytes):
            self.decode(s)

    def check(self):
        if len(self.v) != 6:
            self.v = b'000000'

    def encode(self) -> bytes:
        return self.v

    def decode(self, data: bytes) -> None:
        self.v = data[0:6][::-1]
        self.check()

    @staticmethod
    def deserialize(data: bytes):
        obj = bd_addr()
        obj.decode(data)
        return obj

    @staticmethod
    def deserialize(data: bytes):
        obj = bd_addr()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'bd_addr({self.v.hex(":", 1)})'

class bd_addr_type(IntEnum):
    PUBLIC = 0x00
    RANDOM = 0x01
    RESOVLED_PUB = 0x02
    RESOVLED_RAN = 0x03

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class cte_slot_duration_type(IntEnum):
    CTE_SLOT_DURATION_1US = 1
    CTE_SLOT_DURATION_2US = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class cte_type(IntEnum):
    CTE_AOA = 0
    CTE_AOD_1US = 1
    CTE_AOD_2US = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class ext_adv_set_en:
    def __init__(self, handle: int, duration: int, max_events: int):
        self.handle = handle
        self.duration = duration
        self.max_events = max_events

    def encode(self) -> bytes:
        return struct.pack('<HHH', self.handle, self.duration, self.max_events)

    def decode(self, data: bytes) -> None:
        (self.handle, self.duration, self.max_events) = struct.unpack('<BHB', data)

    @staticmethod
    def deserialize(data: bytes):
        obj = ext_adv_set_en()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'ext_adv_set_en(handle: {self.handle}, duration: {self.duration}, max_events: {self.max_events})'

class gap_random_address_type(IntEnum):
    GAP_RANDOM_ADDRESS_OFF = 0
    GAP_RANDOM_ADDRESS_NON_RESOLVABLE = 1
    GAP_RANDOM_ADDRESS_RESOLVABLE = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class gatt_client_characteristic:
    def __init__(self, start_handle: int, value_handle: int, end_handle: int, properties: int, uuid128: bytes):
        self.start_handle = start_handle
        self.value_handle = value_handle
        self.end_handle = end_handle
        self.properties = properties
        self.uuid128 = uuid128

    def encode(self) -> bytes:
        return struct.pack('<HHHH', self.start_handle, self.value_handle, self.end_handle, self.properties) + self.uuid128

    def decode(self, data: bytes) -> None:
        (self.start_handle, self.value_handle, self.end_handle, self.properties) = struct.unpack('<HHHH', data)
        self.uuid128 = data[struct.calcsize('<HHHH'):struct.calcsize('<HHHH') + UUID128_LEN]

    @staticmethod
    def deserialize(data: bytes):
        obj = gatt_client_characteristic()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'gatt_client_characteristic(start_handle:{self.start_handle}, value_handle:{self.value_handle}, end_handle:{self.end_handle}, properties:{self.properties}, uuid:{self.uuid128})'

class gatt_client_notification:
    def __init__(self):
        self.attribute_handle = 0

    def encode(self) -> bytes:
        return struct.pack('<IIH', 0, 0, self.attribute_handle)

    def decode(self, data: bytes) -> bytes:
        _a, _b, self.attribute_handle = struct.unpack('<IIH', data)

    @staticmethod
    def deserialize(data: bytes):
        r = gatt_client_notification()
        r.decode(data)
        return r

    def __str__(self) -> str:
        return f'gatt_client_notification(attribute_handle: {self.attribute_handle})'

class initiating_filter_policy(IntEnum):
    INITIATING_ADVERTISER_FROM_PARAM = 0
    INITIATING_ADVERTISER_FROM_LIST  = 1

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class phy_type(IntEnum):
    PHY_1M = 0x01
    PHY_2M = 0x02
    PHY_CODED = 0x03

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class conn_para:
    def __init__(self, scan_int: int, scan_win: int,
                 interval_min: int, interval_max: int,
                 latency: int, supervision_timeout: int,
                 min_ce_len: int, max_ce_len: int) -> None:
        self.scan_int = scan_int
        self.scan_win = scan_win
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.latency = latency
        self.supervision_timeout = supervision_timeout
        self.min_ce_len = min_ce_len
        self.max_ce_len = max_ce_len

    def encode(self) -> bytes:
        return struct.pack('<HHHHHHHH', self.scan_int, self.scan_win,
                           self.interval_min, self.interval_max,
                           self.latency,
                           self.supervision_timeout,
                           self.min_ce_len, self.max_ce_len)

    def decode(self, data: bytes) -> None:
        (self.scan_int, self.scan_win,
            self.interval_min, self.interval_max,
            self.latency,
            self.supervision_timeout,
            self.min_ce_len, self.max_ce_len) = struct.unpack('<HHHHHHHH', data)

    @staticmethod
    def deserialize(data: bytes):
        obj = conn_para()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        f_string = f"scan_int: {self.scan_int}"
        f_string += f", scan_win: {self.scan_win}"
        f_string += f", interval_min: {self.interval_min}"
        f_string += f", interval_max: {self.interval_max}"
        f_string += f", latency: {self.latency}"
        f_string += f", supervision_timeout: {self.supervision_timeout}"
        f_string += f", min_ce_len: {self.min_ce_len}"
        f_string += f", max_ce_len: {self.max_ce_len}"
        return f'initiating_phy_config({f_string})'

class initiating_phy_config:
    def __init__(self, phy: phy_type, config: conn_para):
        self.phy = phy
        self.config = config

    def encode(self) -> bytes:
        return struct.pack('<B', self.phy) + b'\0' + self.config.encode()

    def decode(self, data: bytes) -> None:
        self.phy = data[0]
        self.config.decode(data[1:])

    @staticmethod
    def deserialize(data: bytes):
        obj = initiating_phy_config()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'initiating_phy_config(phy: {self.phy}, config: {self.config})'


class io_capability(IntEnum):
    IO_CAPABILITY_UNINITIALIZED = -1
    IO_CAPABILITY_DISPLAY_ONLY = 0
    IO_CAPABILITY_DISPLAY_YES_NO = 1
    IO_CAPABILITY_KEYBOARD_ONLY = 2
    IO_CAPABILITY_NO_INPUT_NO_OUTPUT = 3
    IO_CAPABILITY_KEYBOARD_DISPLAY = 4

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class le_connection_parameter_range:
    def __init__(self, le_conn_interval_min: int, le_conn_interval_max: int,
                 le_conn_latency_min: int, le_conn_latency_max: int,
                 le_supervision_timeout_min: int, le_supervision_timeout_max: int):
        self.le_conn_interval_min = le_conn_interval_min
        self.le_conn_interval_max = le_conn_interval_max
        self.le_conn_latency_min = le_conn_latency_min
        self.le_conn_latency_max = le_conn_latency_max
        self.le_supervision_timeout_min = le_supervision_timeout_min
        self.le_supervision_timeout_max = le_supervision_timeout_max

    def encode(self) -> bytes:
        return struct.pack('<HHHHHH', self.le_conn_interval_min, self.le_conn_interval_max,
                           self.le_conn_latency_min, self.le_conn_latency_max,
                           self.le_supervision_timeout_min, self.le_supervision_timeout_max)

    def decode(self, data: bytes) -> None:
        (self.le_conn_interval_min, self.le_conn_interval_max,
            self.le_conn_latency_min, self.le_conn_latency_max,
            self.le_supervision_timeout_min, self.le_supervision_timeout_max) = struct.unpack('<HHHHHH', data)

    @staticmethod
    def deserialize(data: bytes):
        obj = le_connection_parameter_range()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        f_string = f"le_conn_interval_min: {self.le_conn_interval_min}"
        f_string += f", le_conn_interval_max: {self.le_conn_interval_max}"
        f_string += f", le_conn_latency_min: {self.le_conn_latency_min}"
        f_string += f", le_conn_latency_max: {self.le_conn_latency_max}"
        f_string += f", le_supervision_timeout_min: {self.le_supervision_timeout_min}"
        f_string += f", le_supervision_timeout_max: {self.le_supervision_timeout_max}"
        return f'le_connection_parameter_range({f_string})'


class periodic_adv_filter_policy(IntEnum):
    PERIODIC_ADVERTISER_FROM_PARAM = 0
    PERIODIC_ADVERTISER_FROM_LIST  = 1

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class periodic_adv_property(IntEnum):
    PERIODIC_ADV_BIT_INC_TX = 1 << 6

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class periodic_adv_sync_transfer_mode(IntEnum):
    PERIODIC_TRANS_MODE_NULL = 0
    PERIODIC_TRANS_MODE_SEND_EVT_DISABLE_REPORT = 1
    PERIODIC_TRANS_MODE_SEND_EVT_ENABLE_REPORT = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class phy_bittype(IntEnum):
    PHY_1M_BIT    = 1
    PHY_2M_BIT    = 2
    PHY_CODED_BIT = 4

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class phy_option(IntEnum):
    HOST_NO_PREFERRED_CODING = 0
    HOST_PREFER_S2_CODING = 1
    HOST_PREFER_S8_CODING = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class platform_cfg_item(IntEnum):
    PLATFORM_CFG_LOG_HCI = 0
    PLATFORM_CFG_POWER_SAVING = 1
    PLATFORM_CFG_TRACE_MASK = 2
    PLATFORM_CFG_RC32K_EN = 3
    PLATFORM_CFG_OSC32K_EN = 4
    PLATFORM_CFG_32K_CLK = 5,
    PLATFORM_CFG_32K_CLK_ACC = 6
    PLATFORM_CFG_32K_CALI_PERIOD = 7
    PLATFORM_CFG_PS_DBG_0 = 8
    PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION = 9
    PLATFORM_CFG_SLEEP_TIME_REDUCTION = 10
    PLATFORM_CFG_LL_DBG_FLAGS = 11
    PLATFORM_CFG_LL_LEGACY_ADV_INTERVAL = 12
    PLATFORM_CFG_RTOS_ENH_TICK = 13
    PLATFORM_CFG_LL_DELAY_COMPENSATION = 14
    PLATFORM_CFG_24M_OSC_TUNE = 15
    PLATFORM_CFG_ALWAYS_CALL_WAKEUP = 16
    PLATFORM_CFG_PS_DBG_3 = 17
    PLATFORM_CFG_PS_DBG_4 = 18

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class platform_info_item(IntEnum):
    PLATFORM_INFO_OSC32K_STATUS = 0
    PLATFORM_INFO_32K_CALI_VALUE = 1
    PLATFOFM_INFO_IRQ_NUMBER = 50
    PLATFOFM_INFO_NUMBER = 255

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class platform_task_id(IntEnum):
    PLATFORM_TASK_CONTROLLER = 0
    PLATFORM_TASK_HOST = 1
    PLATFORM_TASK_RTOS_TIMER = 2

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class scan_filter_policy(IntEnum):
    # Accept all advertising packets except directed advertising packets not
    # addressed to this device (default).
    SCAN_ACCEPT_EXCEPT_NOT_DIRECTED = 0
    # Accept only advertising packets from devices where the advertiser��s
    # address is in the White List. Directed advertising packets which are not
    # addressed to this device shall be ignored
    SCAN_ACCEPT_WLIST_EXCEPT_NOT_DIRECTED = 1
    # Accept all advertising packets except directed advertising packets
    # where the initiator's identity address does not address this device
    SCAN_ACCEPT_EXCEPT_IDENTITY_NOT_MATCH = 2
    # Accept all advertising packets except:
    # 1.  advertising packets where the advertiser's identity address is not in
    #     the White List; and
    # 2.  directed advertising packets where the initiator's identity address
    #     does not address this device
    SCAN_ACCEPT_WLIST_EXCEPT_IDENTITY_NOT_MATCH = 3

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class scan_type(IntEnum):
    # Passive scan
    SCAN_PASSIVE = 0x00
    # Active scan
    SCAN_ACTIVE = 0x01

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class scan_phy_config:
    def __init__(self, phy: phy_type, scan_type: scan_type, interval: int, window: int):
        self.phy = phy
        self.scan_type = scan_type
        self.interval = interval
        self.window = window

    def encode(self) -> bytes:
        return struct.pack('<BBHH', self.phy, self.scan_type, self.interval, self.window)

    def decode(self, data: bytes) -> None:
        (self.phy, self.scan_type, self.interval, self.window) = struct.unpack('<BBHH', data)

    @staticmethod
    def deserialize(data: bytes):
        obj = scan_phy_config()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'scan_phy_config(phy: {self.phy}, scan_type: {self.scan_type}, interval: {self.interval}, window: {self.window})'


class sm_persistent:
    def __init__(self, er: bytes, ir: bytes, identity_addr: bd_addr, identity_addr_type: bd_addr_type):
        self.er = er
        self.ir = ir
        self.identity_addr = identity_addr
        self.identity_addr_type = identity_addr_type

    def encode(self) -> bytes:
        return bytes(self.er) + bytes(self.ir) + self.identity_addr.encode() + struct.pack('<B', self.identity_addr_type)

    def decode(self, data: bytes) -> None:
        self.er = data[:16]
        self.ir = data[16:32]
        self.identity_addr.decode(data[32:32+6])
        self.identity_addr_type = data[32 + 6]

    @staticmethod
    def deserialize(data: bytes):
        obj = sm_persistent()
        obj.decode(data)
        return obj

    def __str__(self) -> str:
        return f'sm_persistent(er:{self.er.hex(16)},ir:{self.ir.hex(16)},identity_addr:{str(self.identity_addr)},identity_addr_type:{self.identity_addr_type})'

class unified_phy_type(IntEnum):
    UNIFIED_PHY_1M = 0x01
    UNIFIED_PHY_2M = 0x02
    UNIFIED_PHY_CODED_S8 = 0x03
    UNIFIED_PHY_CODED_S2 = 0x04

    def encode(self) -> bytes:
        return struct.pack('<B', self.value)

class UUID:

    SIG_BASE_UUID = bytes([0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x00, 0x80, 0x5F, 0x9B, 0x34, 0xFB])

    def __init__(self, uuid) -> None:
        self.uuid = uuid

    def is_sig_uuid(self, uuid: int) -> bool:
        if isinstance(self.uuid, bytes):
            if UUID.has_bluetooth_prefix(self.uuid):
                v = (self.uuid[2] << 8) + self.uuid[3]
                return v == uuid

        return False

    @staticmethod
    def normalize(uuid: int | bytes) -> bytes:
        if isinstance(uuid, bytes):
            return uuid
        else:
            r = [0, 0, 0, 0] + list(UUID.SIG_BASE_UUID)
            r[0] = (uuid >> 24) & 0xff
            r[1] = (uuid >> 16) & 0xff
            r[2] = (uuid >> 8) & 0xff
            r[3] = uuid & 0xff
            return bytes(r)

    @staticmethod
    def has_bluetooth_prefix(uuid128: bytes) -> bool:
        if len(uuid128) == 16:
            return uuid128[4:] == UUID.SIG_BASE_UUID
        return False

    def __str__(self) -> str:
        if isinstance(self.uuid, bytes):
            if UUID.has_bluetooth_prefix(self.uuid):
                v = (self.uuid[2] << 8) + self.uuid[3]
                return f"0x{v:04x}"
            else:
                uuid = self.uuid
                return f"{uuid[0]:02x}{uuid[1]:02x}{uuid[2]:02x}{uuid[3]:02x}-{uuid[4]:02x}{uuid[5]:02x}-{uuid[6]:02x}{uuid[7]:02x}-{uuid[8]:02x}{uuid[9]:02x}-{uuid[10]:02x}{uuid[11]:02x}{uuid[12]:02x}{uuid[13]:02x}{uuid[14]:02x}{uuid[15]:02x}"
        else:
            return f"0x{self.uuid:04x}"
