# Import the socket module
import signal
import socket
import argparse
import sys
import json
import threading
import queue
import time
import struct
from collections import namedtuple
from typing import Any, Tuple
from ble_rpc_client.log import LOG_W, LOG_E, LOG_I, LOG_D, LOG_PLAIN, LOG_OK
from ble_rpc_client import log, bt_defs
from ble_rpc_client.bt_defs import *
from ble_rpc_client.brpc_calls import *

STATUS_OK           = 0
STATUS_ERR          = 1
RPC_EVT_READY       = 0
RPC_EVT_HCI         = 1
RPC_EVT_ATT_READ    = 2
RPC_EVT_ATT_WRITE   = 3
RPC_EVT_GATT        = 4
RPC_EVT_SM          = 5
RPC_EVT_SM_OOB_REQ  = 6
RPC_EVT_CALLBACK    = 7
RPC_EVT_MEMCPY      = 8
RPC_EVT_UNDEF       = 9
RPC_EVT_PLATFORM    = 10

RPC_FRAME_CALL      = 0
RPC_FRAME_RET       = 1
RPC_FRAME_EVT       = 2
RPC_FRAME_OOB       = 4

RPC_CB_HCI_CMD_COMPLETE     = 0
RPC_CB_HCI_PACKET_HANDLER   = 1
RPC_CB_PLATFORM_IRQ         = 2
RPC_CB_VOID_VOID            = 3

PLATFORM_CB_EVT_HARD_FAULT = 5
PLATFORM_CB_EVT_ASSERTION  = 6
PLATFORM_CB_EVT_HEAP_OOM   = 8
PLATFORM_CB_EVT_EXCEPTION  = 10

comm_queue: queue.Queue = None
msg_queue: queue.Queue = None

RUN: bool = True

class BRPCFrameRet:
    def __init__(self, param: bytearray) -> None:
        t = param.copy()
        b0 = t.pop(0)
        b1 = t.pop(0)
        self.id = b0 + (b1 << 8)
        self.body = bytes(t)

class BRPCFrameEvtReady:
    def __init__(self, param: bytearray) -> None:
        Ver = namedtuple('Version', 'major minor patch')
        self.brpc_ver = param[0]
        self.chip_family = param[1]
        self.ver = Ver._make(struct.unpack('<HBB', bytes(param[2:])))

class BRPCFrameEvtHCI:
    def __init__(self, param: bytearray) -> None:
        self.packet = param.copy()

class BRPCFrameEvtSM:
    def __init__(self, param: bytearray) -> None:
        self.packet = param.copy()

class BRPCFrameEvtAttRead:
    def __init__(self, param: bytearray) -> None:
        self.conn_handle = param[0] + (param[1] << 8)
        self.att_handle  = param[2] + (param[3] << 8)

class BRPCFrameEvtAttWrite:
    def __init__(self, param: bytearray) -> None:
        self.conn_handle = param[0] + (param[1] << 8)
        self.att_handle  = param[2] + (param[3] << 8)
        self.transaction_mode = param[4] + (param[5] << 8)
        self.offset           = param[6] + (param[7] << 8)
        self.buffer           = param[8:]

class BRPCFrameEvtGatt:
    def __init__(self, param: bytearray) -> None:
        self.conn_handle = param[0] + (param[1] << 8)
        self.packet_type = param[2]
        self.packet = param[3:]

class BRPCFrameEvtCallback:
    def __init__(self, param: bytearray) -> None:
        self.type       = param[0]
        self.p_cb       = param[1] + (param[2] << 8) + (param[3] << 16) + (param[4] << 24)
        self.packet     = param[5:]

class BRPCFrameEvtMemCpy:
    def __init__(self, param: bytearray) -> None:
        self.p_dest     = param[0] + (param[1] << 8) + (param[2] << 8) + (param[3] << 8)
        self.packet     = param[4:]

class BRPCFrameEvtUndefFun:
    def __init__(self, param: bytearray) -> None:
        self.fun       = param[0] + (param[1] << 8)

class BRPCFrameEvtPlatform:
    def __init__(self, param_all: bytearray) -> None:
        t = param_all[0]
        param = param_all[1:]
        if t == PLATFORM_CB_EVT_HARD_FAULT:
            Evt = namedtuple('HardFault', 'r0 r1 r2 r3 r12 lr pc psr')
            self.event = Evt._make(struct.unpack('<IIIIIIII', param))
        elif t == PLATFORM_CB_EVT_ASSERTION:
            # TODO: fix this
            Evt = namedtuple('Assertion', 'line_no p_file_name')
            self.event = Evt._make((struct.unpack_from('<I', param)[0], param[4:-1].decode()))
        elif t == PLATFORM_CB_EVT_HEAP_OOM:
            Evt = namedtuple('HeapOOM', 'tag')
            self.event = Evt._make(struct.unpack('<I', param))
        elif t == PLATFORM_CB_EVT_EXCEPTION:
            Evt = namedtuple('Exception', 'tag')
            self.event = Evt._make(struct.unpack('<I', param))
        else:
            self.event = f"Unhandled BRPCFrameEvtPlatform: type = {t}, param = {param}"

class BRPCFrameInternalRunnable:
    def __init__(self, cb: Callable[[], None]) -> None:
        self.cb = cb

class BRPCReceiver:
    def __init__(self, q: queue.Queue):
        self.acc = bytearray()
        self.q = q

    def handle_evt(self) -> None:
        t = self.acc.pop(0)
        evt = None
        if t == RPC_EVT_READY:
            evt = BRPCFrameEvtReady(self.acc)
        elif t == RPC_EVT_HCI:
            evt = BRPCFrameEvtHCI(self.acc)
        elif t == RPC_EVT_ATT_READ:
            evt = BRPCFrameEvtAttRead(self.acc)
        elif t == RPC_EVT_ATT_WRITE:
            evt = BRPCFrameEvtAttWrite(self.acc)
        elif t == RPC_EVT_GATT:
            evt = BRPCFrameEvtGatt(self.acc)
        elif t == RPC_EVT_SM:
            evt = BRPCFrameEvtSM(self.acc)
        elif t == RPC_EVT_SM_OOB_REQ:
            raise Exception(f'BRPCReceiver: RPC_EVT_SM_OOB_REQ')
        elif t == RPC_EVT_CALLBACK:
            evt = BRPCFrameEvtCallback(self.acc)
        elif t == RPC_EVT_MEMCPY:
            evt = BRPCFrameEvtMemCpy(self.acc)
        elif t == RPC_EVT_UNDEF:
            evt = BRPCFrameEvtUndefFun(self.acc)
        elif t == RPC_EVT_PLATFORM:
            evt = BRPCFrameEvtPlatform(self.acc)
        else:
            raise Exception(f'BRPCReceiver: unknown RPC_EVT {t}')

        self.q.put(evt)

    def rx_byte(self, b: int) -> None:
        self.acc.append(b)
        if len(self.acc) < 2:
            return

        l = self.acc[0] + (self.acc[1] << 8)
        if len(self.acc) < 2 + l:
            return

        if l == 0:
            raise Exception('length == 0')

        # remove length
        self.acc.pop(0)
        self.acc.pop(0)

        t = self.acc.pop(0)
        if t == RPC_FRAME_RET:
            self.q.put(BRPCFrameRet(self.acc))
        elif t == RPC_FRAME_EVT:
            self.handle_evt()
        else:
            raise Exception(f'unknown type: {t}')

        self.acc.clear()

def send_generic_response(type: int, data1: bytes, data2: bytes):
    frame = bytearray()
    l = 1 + len(data1) + len(data2)
    frame.extend([l & 0xff, l >> 8, type])
    frame.extend(data1)
    frame.extend(data2)
    comm_queue.put(bytes(frame))

def call_void_fun(id: int, param: bytes):
    call = bytes([id & 0xff, id >> 8])
    send_generic_response(RPC_FRAME_CALL, call, param)

def show_chip_family(family: int) -> str:
    if family == 0:
        return 'ING918XX'
    elif family == 1:
        return 'ING916XX'
    else:
        return f'???({family})'

api_name_dict = {}

def get_fun_name(id: int) -> str:
    global api_name_dict
    if len(api_name_dict) < 1:
        with open('brpc_fun_names.json', 'r') as f:
            api_name_dict = json.load(f)
    return api_name_dict[str(id)]

class ISRInfo:
    def __init__(self, cb: Any, data: Any) -> None:
        self.cb = cb
        self.data = data

class BRPCSimHost:
    def __init__(self, q_msg: queue.Queue, setup_profile: Callable[[], None]) -> None:
        self.q_msg = q_msg
        self.q_cached_msg = queue.Queue()
        self.hci_callback_chain = []
        self.sm_callback_chain = []
        self.read_callback = None
        self.write_callback = None
        self.gatt_callback = None
        self.isr_infos = {}
        self.ver = None
        self.setup_profile = setup_profile

    def address_of_object(self, obj: Any) -> int:
        return ObjectSim.address_of_object(obj)

    def object_of_address(self, addr: int) -> Any:
        return ObjectSim.object_of_address(addr)

    def hci_add_event_handler(self, handler: Callable[[int, int, bytes], None]) -> None:
        self.hci_callback_chain.append(handler)

    def broadcast_hci_event(self, packet_type: int, channel: int, packet: bytes) -> None:
        for f in self.hci_callback_chain:
            f(packet_type, channel, packet)

    def broadcast_sm_event(self, packet_type: int, channel: int, packet: bytes) -> None:
        for f in self.sm_callback_chain:
            f(packet_type, channel, packet)

    def set_isr(self, irq: int, cb: Any, data: Any) -> None:
        isr = ISRInfo(cb, data)
        self.isr_infos[irq] = isr

    def call_irq(self, irq: int) -> None:
        isr = self.isr_infos[irq]
        isr.cb(isr.data)

    def handle_msg_callback(self, msg: BRPCFrameEvtCallback) -> None:

        if msg.type == RPC_CB_HCI_CMD_COMPLETE:
            f = self.object_of_address(msg.p_cb)
            return_params = msg.packet[3:]
            user_data = self.object_of_address(struct.unpack("<I", msg.packet[0:4]))
            f(return_params, user_data)
        elif msg.type == RPC_CB_HCI_PACKET_HANDLER:
            f = self.object_of_address(msg.p_cb)
            packet_type, channel = struct.unpack("<BH", msg.packet[0:3])
            f(packet_type, channel, msg.packet[3:])
        elif msg.type == RPC_CB_PLATFORM_IRQ:
            self.call_irq(msg.p_cb);
        elif msg.type == RPC_CB_VOID_VOID:
            f = self.object_of_address(msg.p_cb)
            f()
        else:
            LOG_E(f"unknown callback type: {msg.type}")

    def get_version(self) -> Any:
        return self.ver

    def wait_fun_ret(self, fun_id: int) -> bytes:
        while True:
            msg = self.q_msg.get()

            if type(msg) == BRPCFrameEvtMemCpy:
                self.handle_msg(msg)
                continue
            elif type(msg) == BRPCFrameEvtPlatform:
                self.handle_msg(msg)
                continue

            if (type(msg) == BRPCFrameRet) and (msg.id == fun_id):
                return msg.body

            self.q_cached_msg.put(msg)

    def handle_msg(self, msg: Any):
        if type(msg) == BRPCFrameEvtReady:
            if msg.brpc_ver == BRPC_VERSION:
                self.ver = msg.ver
                LOG_OK(f"Ready. {show_chip_family(msg.chip_family)} ({msg.ver.major}.{msg.ver.minor}.{msg.ver.patch})")
            else:
                LOG_E(f"BRPC Version not match: {BRPC_VERSION} vs {msg.brpc_ver}")
                raise Exception(f"BRPC Version not match: {BRPC_VERSION} vs {msg.brpc_ver}")

        elif type(msg) == BRPCFrameEvtHCI:
            self.broadcast_hci_event(HCI_EVENT_PACKET, 0, msg.packet)

        elif type(msg) == BRPCFrameEvtAttRead:
            if self.read_callback is None:
                LOG_E("read_callback is missing!")
                return

            value = self.read_callback(msg.conn_handle, msg.att_handle)
            if value is None: return

            att_server_deferred_read_response(msg.conn_handle, msg.att_handle, value)

        elif type(msg) == BRPCFrameEvtAttWrite:
            if self.write_callback is None:
                LOG_E("write_callback is missing!")
                return
            self.write_callback(msg.conn_handle, msg.att_handle, msg.transaction_mode,
                       msg.offset, msg.buffer)

        elif type(msg) == BRPCFrameEvtGatt:
            if self.gatt_callback is None:
                return
            self.gatt_callback(msg.packet_type, msg.conn_handle, msg.packet)

        elif type(msg) == BRPCFrameEvtSM:
            self.broadcast_sm_event(HCI_EVENT_PACKET, 0, msg.packet)

        elif type(msg) == BRPCFrameEvtCallback:
            self.handle_msg_callback(msg)

        elif type(msg) == BRPCFrameEvtMemCpy:
            obj = self.addr_to_object(msg.p_dest)
            obj = msg.packet.copy()

        elif type(msg) == BRPCFrameEvtUndefFun:
            LOG_E(f"undef API: {get_fun_name(msg.fun)}")

        elif type(msg) == BRPCFrameEvtPlatform:
            LOG_E(f"Platform {msg.event}")
            sys.exit(-1)

        elif type(msg) == BRPCFrameRet:
            LOG_E(f"unhandled RET of {get_fun_name(msg.id)}")

        elif type(msg) == BRPCFrameInternalRunnable:
            msg.cb()

        else:
            LOG_E(f"unknown event: {msg}")

    def post_obj(self, obj: Any):
        self.q_msg.put(obj)
        pass

    def brpc_entry(self):
        self.setup_profile()
        platform_reset()
        while RUN:
            while self.q_cached_msg.qsize() > 0:
                self.handle_msg(self.q_cached_msg.get())

            if self.q_msg.qsize() < 1:
                time.sleep(0.005)
                continue

            self.handle_msg(self.q_msg.get())

def handle_connection(s: socket, q_comm: queue.Queue, q_msg: queue.Queue):
    s.setblocking(False)
    receiver = BRPCReceiver(q_msg)

    while RUN:
        while q_comm.qsize() > 0:
            msg = q_comm.get()
            s.send(msg)
        data = None
        try:
            data = s.recv(1024)
        except:
            time.sleep(0.01)
            continue

        for b in data:
            receiver.rx_byte(b)
    s.close()

def signal_handler(sig, frame):
    print("signal_handler() is executing -- SIGINT detected!")
    import os
    os._exit(-1)

SimHost: BRPCSimHost = None

def _start(setup_profile: Callable[[], None]):
    global comm_queue
    global msg_queue
    global SimHost

    comm_queue = queue.Queue()
    msg_queue = queue.Queue()
    SimHost = BRPCSimHost(msg_queue, setup_profile)

    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", type=str, default="localhost", help="The IP address of the RPC server")
    parser.add_argument("-port", type=int, default=8888, help="The port number of the RPC server")
    parser.add_argument("-log_level", type=int, default=2, help="Change log level")

    args = parser.parse_args()

    log.LOG_LEVEL = args.log_level

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((args.ip, args.port))

    t0 = threading.Thread(target=handle_connection, args=(s, comm_queue, msg_queue))
    t1 = threading.Thread(target=lambda : SimHost.brpc_entry())

    t0.start()
    t1.start()

    while RUN:
        time.sleep(1)

def spawn(fun: Callable[[], None]):
    t = threading.Thread(target=lambda : fun())
    t.start()

def start_detached(setup_profile: Callable[[], None]):
    spawn(lambda : _start(setup_profile))

def start(setup_profile: Callable[[], None]):
    signal.signal(signal.SIGINT, signal_handler)
    _start(setup_profile)

ID_sys_mem_map_add            =  1
ID_sys_persist_mem_new        =  2
ID_sys_persist_mem_append     =  3
ID_sys_persist_mem_free       =  4
ID_sys_alloc_heap_for_conn    =  5
ID_sys_enable_irq             =  6
ID_sys_get_heap_status        =  7
ID_sys_shutdown               =  8
ID_sys_hrng                   =  9
ID_sys_set_timer              =  10
ID_sys_aligned_read_mem       =  11
ID_sys_aligned_write_mem      =  12
ID_att_set_db                 =  0x30
ID_gatt_client_get_mtu        =  0x31
ID_gap_aes_encrypt            =  0x32
ID_sm_private_random_address_generation_get            = 0x33

def call_fun(id: int, param: bytes) -> bytes:
    call = bytes([id & 0xff, id >> 8])
    send_generic_response(RPC_FRAME_CALL, call, param)
    return SimHost.wait_fun_ret(id)

def att_server_init(read_cb: Callable[[int, int], bytes | None | int],
                    write_cb: Callable[[int, int, int, int, bytes], None]):
    SimHost.read_callback = read_cb
    SimHost.write_callback = write_cb

def hci_add_event_handler(handler: btstack_packet_handler_t) -> None:
    SimHost.hci_add_event_handler(handler)

def att_server_register_packet_handler(handler: Any) -> None:
    pass

def remote_mem_map(local_address: int, data: bytes) -> None:
    _param = b''
    _param += struct.pack('<I', local_address)
    _param += data
    call_void_fun(ID_sys_mem_map_add, _param)

def remote_mem_alloc(local_address: int, data: bytes) -> None:
    total_len = len(data)
    first_len = total_len if total_len <= 255 else 255

    _param = struct.pack('<IHH', local_address, total_len, first_len)
    _param += data[0:first_len]
    call_void_fun(ID_sys_persist_mem_new, _param)
    data = data[first_len:]

    while len(data) > 0:
        block_len = len(data) if len(data) <= 255 else 255
        _param = struct.pack('<IH', local_address, block_len)
        _param += data[0:block_len]
        call_void_fun(ID_sys_persist_mem_append, _param)
        data = data[block_len:]

def remote_mem_free(local_address: int) -> None:
    _param = struct.pack('<I', local_address)
    call_void_fun(ID_sys_persist_mem_free, _param)

def alloc_heap_for_conn(local_address: int, size: int, conn_handle: int) -> None:
    _param = struct.pack('<IHH', local_address, size, conn_handle)
    call_void_fun(ID_sys_alloc_heap_for_conn, _param)

def att_set_db(conn_hanale: int, db: bytes) -> None:
    local_addr = ObjectSim.address_of_object(db)
    remote_mem_alloc(local_addr, db)
    _param = struct.pack('<HI', conn_hanale, local_addr)
    call_void_fun(ID_att_set_db, _param)

def platform_set_irq_callback(irq: int, f: Any, user_data: Any) -> None:
    _param = struct.pack('<I', irq)
    SimHost.set_isr(irq, f, user_data)
    call_void_fun(ID_sys_enable_irq, _param)

def platform_get_version() -> tuple:
    return SimHost.get_version()

def platform_get_heap_status() -> tuple:
    _ret = call_fun(ID_sys_get_heap_status, b'')
    T = namedtuple('HeapStatus', 'bytes_free bytes_minimum_ever_free')
    return T._make(struct.unpack('<II', _ret))

def platform_shutdown(duration_cycles: int, p_retention_data: int, data_size: int) -> None:
    _param = struct.pack('<III', duration_cycles, p_retention_data, data_size)
    call_void_fun(ID_sys_shutdown, _param)

def platform_hrng(len: int) -> bytes:
    return call_fun(ID_sys_hrng, struct.pack('<I', len))

def platform_set_timer(callback, delay: int) -> None:
    addr = ObjectSim.address_of_object(callback)
    _param = struct.pack('<II', addr, delay)
    call_void_fun(ID_sys_set_timer, _param)

def sys_aligned_read_mem(addr: int, len: int) -> bytes:
    _param = struct.pack('<II', addr, len)
    return call_fun(ID_sys_aligned_read_mem, _param)

def sys_aligned_read(addr: int) -> int:
    _r = sys_aligned_read_mem(addr, 4)
    return struct.unpack('<I', _r)

def sys_aligned_write_mem(addr: int, data: bytes) -> None:
    _param = struct.pack('<I', addr)
    _param += data
    call_void_fun(ID_sys_aligned_write_mem, _param)

def sys_aligned_write(addr: int, value: int):
    _param = struct.pack('<II', addr, value)
    call_void_fun(ID_sys_aligned_write_mem, _param)

def gatt_client_get_mtu(conn_handle: int) -> tuple:
    _r = call_fun(ID_gatt_client_get_mtu, struct.pack('<H', conn_handle))
    T = namedtuple('MTU', 'err_code mtu')
    return T._make(struct.unpack('<BH', _r))

def gatt_client_register_handler(handler: btstack_packet_handler_t) -> None:
    SimHost.gatt_client_handler = handler

def btstack_push_user_runnable(fun: Callable[[], None]) -> int:
    o = BRPCFrameInternalRunnable(fun)
    SimHost.post_obj(o)

def platform_get_current_task() -> int:
    raise "not implemented: platform_get_current_task()"

def uuid_has_bluetooth_prefix(uuid128: bytes) -> bool:
    bluetooth_base_uuid = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00,
    0x80, 0x00, 0x00, 0x80, 0x5F, 0x9B, 0x34, 0xFB])
    return uuid128[4:] == bluetooth_base_uuid[4:]

def sm_register_oob_data_callback(get_oob_data_callback: Callable[[int, bd_addr], bytes]) -> None:
    raise "not implemented: sm_register_oob_data_callback()"

def sm_private_random_address_generation_get() -> bd_addr:
    return bd_addr.deserialize(call_fun(ID_sm_private_random_address_generation_get, b''))

def printf_hexdump(data: bytes) -> None:
    print(data.hex())

def hci_event_packet_get_type(data: bytes) -> int:
    return data[0]

def btstack_event_state_get_state(event: bytes) -> int:
    return event[2]

def hci_event_le_meta_get_subevent_code(event: bytes) -> int:
    return event[2]

def decode_hci_event(packet: bytes, fmt: str, EvtTuple: Any) -> Tuple:
    return EvtTuple._make(struct.unpack(fmt, packet[2:]))

def hci_event_command_complete_get_num_hci_command_packets(event: bytes) -> int:
    return event[2]

def hci_event_command_complete_get_command_opcode(event: bytes) -> int:
    return struct.unpack('<H', event[3:5])[0]

def hci_event_command_complete_get_return_parameters(event: bytes) -> int:
    return event[5:]

def hci_event_le_meta_get_subevent_code(event: bytes) -> int:
    return event[2]

def att_server_notify_long_data(con_handle: hci_con_handle | int,
        attribute_handle: uint16 | int,
        value: bytes, mtu: int) -> int:
    for i in range(0, len(value), mtu):
        r = att_server_notify(con_handle, attribute_handle,
                              value[i:i + mtu])
        if r != 0:
            LOG_E(f'{r}')
            return r
    return 0

class BtStackEventState:
    def __init__(self, packet: bytes) -> None:
        self.state = btstack_event_state_get_state(packet)

class HciEventCommandComplete:
    def __init__(self, packet: bytes) -> None:
        self.num_hci_command_packets = hci_event_command_complete_get_num_hci_command_packets(packet)
        self.opcode = hci_event_command_complete_get_command_opcode(packet)
        self.return_parameters = hci_event_command_complete_get_return_parameters(packet)

class HciEventCommandStatus:
    def __init__(self, packet: bytes) -> None:
        self.status, self.num_hci_command_packets, self.opcode = struct.unpack('<BBH', packet[2:])

class HciEventDisconnectionComplete:
    def __init__(self, packet: bytes) -> None:
        self.status, self.conn_handle, self.reason = struct.unpack('<BHB', packet[2:])

class HciEventReadRemoteVersionInformationComplete:
    def __init__(self, packet: bytes) -> None:
        self.status, self.conn_handle, self.version, self.manufacturer_name, self.subversion = struct.unpack('<BHBHH', packet[2:])

class HciSubEventLeEnhancedConnectionComplete:
    def __init__(self, packet: bytes) -> None:
        self.status,    \
        self.handle,    \
        self.role,      \
        self.peer_addr_type,    \
        self.peer_addr,         \
        self.local_resolv_priv_addr,    \
        self.peer_resolv_priv_addr,     \
        self.interval,                  \
        self.latency,                   \
        self.sup_timeout,               \
        self.clk_accuracy = struct.unpack('<BHBB6s6s6sHHHb', packet)
        self.peer_addr_type = bd_addr_type(self.peer_addr_type)
        self.peer_addr = bd_addr(self.peer_addr)
        self.local_resolv_priv_addr = bd_addr(self.local_resolv_priv_addr)
        self.peer_resolv_priv_addr = bd_addr(self.peer_resolv_priv_addr)

class HciEventLeMeta:
    def __init__(self, packet: bytes) -> None:
        evt = packet[3:]
        match hci_event_le_meta_get_subevent_code(packet):
            case bt_defs.HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE:
                self.evt = HciSubEventLeEnhancedConnectionComplete(evt)
            case _:
                self.evt = evt

def _parse_tuple(packet: bytes, T: namedtuple, fmt: str) -> tuple:
    return T._make(struct.unpack(fmt, packet))

class HciEventNumberOfCompletedPackets:
    def __init__(self, packet: bytes) -> None:
        self.complete_packets = []
        T = namedtuple('event_conn_packets', 'conn_handle num_of_packets')
        n = packet[2]
        d = packet[3:]
        for i in range(n):
            self.complete_packets.append(_parse_tuple(d[0:4], T, '<HH'))
            d = packet[4:]

class AttEventMtuExchangeComplete:
    def __init__(self, packet: bytes) -> None:
        self.handle, self.mtu = struct.unpack_from('<HH', packet, 2)

def hci_event_decode(packet: bytes) -> Any:
    match hci_event_packet_get_type(packet):
        case bt_defs.BTSTACK_EVENT_STATE:
            return BtStackEventState(packet)
        case bt_defs.HCI_EVENT_COMMAND_COMPLETE:
            return HciEventCommandComplete(packet)
        case bt_defs.HCI_EVENT_COMMAND_STATUS:
            return HciEventCommandStatus(packet)
        case bt_defs.HCI_EVENT_DISCONNECTION_COMPLETE:
            return HciEventDisconnectionComplete(packet)
        case bt_defs.HCI_EVENT_READ_REMOTE_VERSION_INFORMATION_COMPLETE:
            return HciEventReadRemoteVersionInformationComplete(packet)
        case bt_defs.HCI_EVENT_NUMBER_OF_COMPLETED_PACKETS:
            return HciEventNumberOfCompletedPackets(packet)
        case bt_defs.HCI_EVENT_LE_META:
            return HciEventLeMeta(packet)
        case bt_defs.ATT_EVENT_MTU_EXCHANGE_COMPLETE:
            return AttEventMtuExchangeComplete(packet)
        case other:
            return packet