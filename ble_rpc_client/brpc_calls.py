# machine generated code. DO NOT modify!
from ble_rpc_client.bt_defs import *
from ble_rpc_client import log, brpc
from typing import List

def platform_reset():
    log.LOG_D("platform_reset...")
    _param = b''
    
    brpc.call_void_fun(1001, _param)

def platform_switch_app(app_addr: uint32 | int):
    log.LOG_D("platform_switch_app...")
    _param = b''
    _app_addr = (app_addr if isinstance(app_addr, uint32) else uint32(app_addr)).encode()
    _param += _app_addr
    brpc.call_void_fun(1002, _param)

def platform_write_persistent_reg(value: uint8 | int):
    log.LOG_D("platform_write_persistent_reg...")
    _param = b''
    _value = (value if isinstance(value, uint8) else uint8(value)).encode()
    _param += _value
    brpc.call_void_fun(1003, _param)

def platform_read_persistent_reg() -> uint8 | int:
    log.LOG_D("platform_read_persistent_reg...")
    _param = b''
    
    _ret = brpc.call_fun(1004, _param)
    return uint8.deserialize(_ret)

def platform_config(item: platform_cfg_item,
        flag: uint32 | int):
    log.LOG_D("platform_config...")
    _param = b''
    _item = item.encode()
    _param += _item
    _flag = (flag if isinstance(flag, uint32) else uint32(flag)).encode()
    _param += _flag
    brpc.call_void_fun(1005, _param)

def platform_read_info(item: platform_info_item) -> uint32 | int:
    log.LOG_D("platform_read_info...")
    _param = b''
    _item = item.encode()
    _param += _item
    _ret = brpc.call_fun(1006, _param)
    return uint32.deserialize(_ret)

def platform_calibrate_rt_clk() -> uint32 | int:
    log.LOG_D("platform_calibrate_rt_clk...")
    _param = b''
    
    _ret = brpc.call_fun(1007, _param)
    return uint32.deserialize(_ret)

def platform_rt_rc_tune(value: uint16 | int):
    log.LOG_D("platform_rt_rc_tune...")
    _param = b''
    _value = (value if isinstance(value, uint16) else uint16(value)).encode()
    _param += _value
    brpc.call_void_fun(1008, _param)

def platform_rt_rc_auto_tune() -> uint16 | int:
    log.LOG_D("platform_rt_rc_auto_tune...")
    _param = b''
    
    _ret = brpc.call_fun(1009, _param)
    return uint16.deserialize(_ret)

def platform_rand() -> int:
    log.LOG_D("platform_rand...")
    _param = b''
    
    _ret = brpc.call_fun(1010, _param)
    return struct.unpack('<i', _ret)[0]

def platform_get_us_time() -> uint64:
    log.LOG_D("platform_get_us_time...")
    _param = b''
    
    _ret = brpc.call_fun(1011, _param)
    return uint64.deserialize(_ret)

def platform_set_rf_clk_source(source: uint8 | int):
    log.LOG_D("platform_set_rf_clk_source...")
    _param = b''
    _source = (source if isinstance(source, uint8) else uint8(source)).encode()
    _param += _source
    brpc.call_void_fun(1012, _param)

def platform_get_task_handle(id: platform_task_id) -> uintptr | int:
    log.LOG_D("platform_get_task_handle...")
    _param = b''
    _id = id.encode()
    _param += _id
    _ret = brpc.call_fun(1013, _param)
    return uintptr.deserialize(_ret)

def gap_set_random_device_address(address: bd_addr) -> uint8 | int:
    log.LOG_D("gap_set_random_device_address...")
    _param = b''
    _address = address.encode()
    _val_address = _address
    _address = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_address, _val_address)
    _address = struct.pack('<I', _address)
    _param += _address
    _ret = brpc.call_fun(1014, _param)
    return uint8.deserialize(_ret)

def gap_disconnect(handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gap_disconnect...")
    _param = b''
    _handle = (handle if isinstance(handle, hci_con_handle) else hci_con_handle(handle)).encode()
    _param += _handle
    _ret = brpc.call_fun(1015, _param)
    return uint8.deserialize(_ret)

def gap_disconnect_all():
    log.LOG_D("gap_disconnect_all...")
    _param = b''
    
    brpc.call_void_fun(1016, _param)

def gap_add_whitelist(address: bd_addr,
        addtype: bd_addr_type) -> uint8 | int:
    log.LOG_D("gap_add_whitelist...")
    _param = b''
    _address = address.encode()
    _val_address = _address
    _address = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_address, _val_address)
    _address = struct.pack('<I', _address)
    _param += _address
    _addtype = addtype.encode()
    _param += _addtype
    _ret = brpc.call_fun(1017, _param)
    return uint8.deserialize(_ret)

def gap_remove_whitelist(address: bd_addr,
        addtype: bd_addr_type) -> uint8 | int:
    log.LOG_D("gap_remove_whitelist...")
    _param = b''
    _address = address.encode()
    _val_address = _address
    _address = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_address, _val_address)
    _address = struct.pack('<I', _address)
    _param += _address
    _addtype = addtype.encode()
    _param += _addtype
    _ret = brpc.call_fun(1018, _param)
    return uint8.deserialize(_ret)

def gap_clear_white_lists() -> uint8 | int:
    log.LOG_D("gap_clear_white_lists...")
    _param = b''
    
    _ret = brpc.call_fun(1019, _param)
    return uint8.deserialize(_ret)

def gap_read_rssi(handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gap_read_rssi...")
    _param = b''
    _handle = (handle if isinstance(handle, hci_con_handle) else hci_con_handle(handle)).encode()
    _param += _handle
    _ret = brpc.call_fun(1020, _param)
    return uint8.deserialize(_ret)

def gap_read_remote_used_features(handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gap_read_remote_used_features...")
    _param = b''
    _handle = (handle if isinstance(handle, hci_con_handle) else hci_con_handle(handle)).encode()
    _param += _handle
    _ret = brpc.call_fun(1021, _param)
    return uint8.deserialize(_ret)

def gap_read_remote_version(handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gap_read_remote_version...")
    _param = b''
    _handle = (handle if isinstance(handle, hci_con_handle) else hci_con_handle(handle)).encode()
    _param += _handle
    _ret = brpc.call_fun(1022, _param)
    return uint8.deserialize(_ret)

def gap_le_read_channel_map(handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gap_le_read_channel_map...")
    _param = b''
    _handle = (handle if isinstance(handle, hci_con_handle) else hci_con_handle(handle)).encode()
    _param += _handle
    _ret = brpc.call_fun(1023, _param)
    return uint8.deserialize(_ret)

def gap_read_phy(con_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_read_phy...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, uint16) else uint16(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1024, _param)
    return uint8.deserialize(_ret)

def gap_set_def_phy(all_phys: uint8 | int,
        tx_phys: phy_bittypes | int,
        rx_phys: phy_bittypes | int) -> uint8 | int:
    log.LOG_D("gap_set_def_phy...")
    _param = b''
    _all_phys = (all_phys if isinstance(all_phys, uint8) else uint8(all_phys)).encode()
    _param += _all_phys
    _tx_phys = (tx_phys if isinstance(tx_phys, phy_bittypes) else phy_bittypes(tx_phys)).encode()
    _param += _tx_phys
    _rx_phys = (rx_phys if isinstance(rx_phys, phy_bittypes) else phy_bittypes(rx_phys)).encode()
    _param += _rx_phys
    _ret = brpc.call_fun(1025, _param)
    return uint8.deserialize(_ret)

def gap_set_phy(con_handle: uint16 | int,
        all_phys: uint8 | int,
        tx_phys: phy_bittypes | int,
        rx_phys: phy_bittypes | int,
        phy_opt: phy_option) -> uint8 | int:
    log.LOG_D("gap_set_phy...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, uint16) else uint16(con_handle)).encode()
    _param += _con_handle
    _all_phys = (all_phys if isinstance(all_phys, uint8) else uint8(all_phys)).encode()
    _param += _all_phys
    _tx_phys = (tx_phys if isinstance(tx_phys, phy_bittypes) else phy_bittypes(tx_phys)).encode()
    _param += _tx_phys
    _rx_phys = (rx_phys if isinstance(rx_phys, phy_bittypes) else phy_bittypes(rx_phys)).encode()
    _param += _rx_phys
    _phy_opt = phy_opt.encode()
    _param += _phy_opt
    _ret = brpc.call_fun(1026, _param)
    return uint8.deserialize(_ret)

def gap_set_adv_set_random_addr(adv_handle: uint8 | int,
        random_addr: bd_addr) -> uint8 | int:
    log.LOG_D("gap_set_adv_set_random_addr...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _random_addr = random_addr.encode()
    _val_random_addr = _random_addr
    _random_addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_random_addr, _val_random_addr)
    _random_addr = struct.pack('<I', _random_addr)
    _param += _random_addr
    _ret = brpc.call_fun(1027, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_scan_para(own_addr_type: bd_addr_type,
        filter: scan_filter_policy,
        configs: List[scan_phy_config]) -> uint8 | int:
    log.LOG_D("gap_set_ext_scan_para...")
    _param = b''
    _own_addr_type = own_addr_type.encode()
    _param += _own_addr_type
    _filter = filter.encode()
    _param += _filter
    _param += struct.pack('<B', len(configs))
    _configs = b''.join([x.encode() for x in configs])
    _val_configs = _configs
    _configs = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_configs, _val_configs)
    _configs = struct.pack('<I', _configs)
    _param += _configs
    _ret = brpc.call_fun(1028, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_scan_response_data(adv_handle: uint8 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gap_set_ext_scan_response_data...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1029, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_scan_enable(enable: uint8 | int,
        filter: uint8 | int,
        duration: uint16 | int,
        period: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_set_ext_scan_enable...")
    _param = b''
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _filter = (filter if isinstance(filter, uint8) else uint8(filter)).encode()
    _param += _filter
    _duration = (duration if isinstance(duration, uint16) else uint16(duration)).encode()
    _param += _duration
    _period = (period if isinstance(period, uint16) else uint16(period)).encode()
    _param += _period
    _ret = brpc.call_fun(1030, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_adv_enable(enable: uint8 | int,
        adv_sets: List[ext_adv_set_en]) -> uint8 | int:
    log.LOG_D("gap_set_ext_adv_enable...")
    _param = b''
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _param += struct.pack('<B', len(adv_sets))
    _adv_sets = b''.join([x.encode() for x in adv_sets])
    _val_adv_sets = _adv_sets
    _adv_sets = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_adv_sets, _val_adv_sets)
    _adv_sets = struct.pack('<I', _adv_sets)
    _param += _adv_sets
    _ret = brpc.call_fun(1031, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_adv_para(adv_handle: uint8 | int,
        properties: adv_event_properties | int,
        interval_min: uint32 | int,
        interval_max: uint32 | int,
        primary_adv_channel_map: adv_channel_bits | int,
        own_addr_type: bd_addr_type,
        peer_addr_type: bd_addr_type,
        peer_addr: bd_addr,
        adv_filter_policy: adv_filter_policy,
        tx_power: int8 | int,
        primary_adv_phy: phy_type,
        secondary_adv_max_skip: uint8 | int,
        secondary_adv_phy: phy_type,
        sid: uint8 | int,
        scan_req_notification_enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_ext_adv_para...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _properties = (properties if isinstance(properties, adv_event_properties) else adv_event_properties(properties)).encode()
    _param += _properties
    _interval_min = (interval_min if isinstance(interval_min, uint32) else uint32(interval_min)).encode()
    _param += _interval_min
    _interval_max = (interval_max if isinstance(interval_max, uint32) else uint32(interval_max)).encode()
    _param += _interval_max
    _primary_adv_channel_map = (primary_adv_channel_map if isinstance(primary_adv_channel_map, adv_channel_bits) else adv_channel_bits(primary_adv_channel_map)).encode()
    _param += _primary_adv_channel_map
    _own_addr_type = own_addr_type.encode()
    _param += _own_addr_type
    _peer_addr_type = peer_addr_type.encode()
    _param += _peer_addr_type
    _peer_addr = peer_addr.encode()
    _val_peer_addr = _peer_addr
    _peer_addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_peer_addr, _val_peer_addr)
    _peer_addr = struct.pack('<I', _peer_addr)
    _param += _peer_addr
    _adv_filter_policy = adv_filter_policy.encode()
    _param += _adv_filter_policy
    _tx_power = (tx_power if isinstance(tx_power, int8) else int8(tx_power)).encode()
    _param += _tx_power
    _primary_adv_phy = primary_adv_phy.encode()
    _param += _primary_adv_phy
    _secondary_adv_max_skip = (secondary_adv_max_skip if isinstance(secondary_adv_max_skip, uint8) else uint8(secondary_adv_max_skip)).encode()
    _param += _secondary_adv_max_skip
    _secondary_adv_phy = secondary_adv_phy.encode()
    _param += _secondary_adv_phy
    _sid = (sid if isinstance(sid, uint8) else uint8(sid)).encode()
    _param += _sid
    _scan_req_notification_enable = (scan_req_notification_enable if isinstance(scan_req_notification_enable, uint8) else uint8(scan_req_notification_enable)).encode()
    _param += _scan_req_notification_enable
    _ret = brpc.call_fun(1032, _param)
    return uint8.deserialize(_ret)

def gap_set_ext_adv_data(adv_handle: uint8 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gap_set_ext_adv_data...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1033, _param)
    return uint8.deserialize(_ret)

def gap_set_periodic_adv_data(adv_handle: uint8 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gap_set_periodic_adv_data...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1034, _param)
    return uint8.deserialize(_ret)

def gap_set_periodic_adv_enable(enable: uint8 | int,
        adv_handle: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_periodic_adv_enable...")
    _param = b''
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _ret = brpc.call_fun(1035, _param)
    return uint8.deserialize(_ret)

def gap_set_periodic_adv_para(adv_handle: uint8 | int,
        interval_min: uint16 | int,
        interval_max: uint16 | int,
        properties: periodic_adv_properties | int) -> uint8 | int:
    log.LOG_D("gap_set_periodic_adv_para...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _interval_min = (interval_min if isinstance(interval_min, uint16) else uint16(interval_min)).encode()
    _param += _interval_min
    _interval_max = (interval_max if isinstance(interval_max, uint16) else uint16(interval_max)).encode()
    _param += _interval_max
    _properties = (properties if isinstance(properties, periodic_adv_properties) else periodic_adv_properties(properties)).encode()
    _param += _properties
    _ret = brpc.call_fun(1036, _param)
    return uint8.deserialize(_ret)

def gap_clr_adv_set() -> uint8 | int:
    log.LOG_D("gap_clr_adv_set...")
    _param = b''
    
    _ret = brpc.call_fun(1037, _param)
    return uint8.deserialize(_ret)

def gap_rmv_adv_set(adv_handle: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_rmv_adv_set...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _ret = brpc.call_fun(1038, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_create_sync(filter_policy: periodic_adv_filter_policy,
        adv_sid: uint8 | int,
        addr_type: bd_addr_type,
        addr: bd_addr,
        skip: uint16 | int,
        sync_timeout: uint16 | int,
        sync_cte_type: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_periodic_adv_create_sync...")
    _param = b''
    _filter_policy = filter_policy.encode()
    _param += _filter_policy
    _adv_sid = (adv_sid if isinstance(adv_sid, uint8) else uint8(adv_sid)).encode()
    _param += _adv_sid
    _addr_type = addr_type.encode()
    _param += _addr_type
    _addr = addr.encode()
    _val_addr = _addr
    _addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_addr, _val_addr)
    _addr = struct.pack('<I', _addr)
    _param += _addr
    _skip = (skip if isinstance(skip, uint16) else uint16(skip)).encode()
    _param += _skip
    _sync_timeout = (sync_timeout if isinstance(sync_timeout, uint16) else uint16(sync_timeout)).encode()
    _param += _sync_timeout
    _sync_cte_type = (sync_cte_type if isinstance(sync_cte_type, uint8) else uint8(sync_cte_type)).encode()
    _param += _sync_cte_type
    _ret = brpc.call_fun(1039, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_create_sync_cancel() -> uint8 | int:
    log.LOG_D("gap_periodic_adv_create_sync_cancel...")
    _param = b''
    
    _ret = brpc.call_fun(1040, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_term_sync(sync_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_periodic_adv_term_sync...")
    _param = b''
    _sync_handle = (sync_handle if isinstance(sync_handle, uint16) else uint16(sync_handle)).encode()
    _param += _sync_handle
    _ret = brpc.call_fun(1041, _param)
    return uint8.deserialize(_ret)

def gap_add_dev_to_periodic_list(addr_type: uint8 | int,
        addr: bd_addr,
        sid: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_add_dev_to_periodic_list...")
    _param = b''
    _addr_type = (addr_type if isinstance(addr_type, uint8) else uint8(addr_type)).encode()
    _param += _addr_type
    _addr = addr.encode()
    _val_addr = _addr
    _addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_addr, _val_addr)
    _addr = struct.pack('<I', _addr)
    _param += _addr
    _sid = (sid if isinstance(sid, uint8) else uint8(sid)).encode()
    _param += _sid
    _ret = brpc.call_fun(1042, _param)
    return uint8.deserialize(_ret)

def gap_rmv_dev_from_periodic_list(addr_type: uint8 | int,
        addr: bd_addr,
        sid: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_rmv_dev_from_periodic_list...")
    _param = b''
    _addr_type = (addr_type if isinstance(addr_type, uint8) else uint8(addr_type)).encode()
    _param += _addr_type
    _addr = addr.encode()
    _val_addr = _addr
    _addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_addr, _val_addr)
    _addr = struct.pack('<I', _addr)
    _param += _addr
    _sid = (sid if isinstance(sid, uint8) else uint8(sid)).encode()
    _param += _sid
    _ret = brpc.call_fun(1043, _param)
    return uint8.deserialize(_ret)

def gap_clr_periodic_adv_list() -> uint8 | int:
    log.LOG_D("gap_clr_periodic_adv_list...")
    _param = b''
    
    _ret = brpc.call_fun(1044, _param)
    return uint8.deserialize(_ret)

def gap_read_periodic_adv_list_size() -> uint8 | int:
    log.LOG_D("gap_read_periodic_adv_list_size...")
    _param = b''
    
    _ret = brpc.call_fun(1045, _param)
    return uint8.deserialize(_ret)

def gap_ext_create_connection(filter_policy: initiating_filter_policy,
        own_addr_type: bd_addr_type,
        peer_addr_type: bd_addr_type,
        peer_addr: bd_addr,
        phy_configs: List[initiating_phy_config]) -> uint8 | int:
    log.LOG_D("gap_ext_create_connection...")
    _param = b''
    _filter_policy = filter_policy.encode()
    _param += _filter_policy
    _own_addr_type = own_addr_type.encode()
    _param += _own_addr_type
    _peer_addr_type = peer_addr_type.encode()
    _param += _peer_addr_type
    _peer_addr = peer_addr.encode()
    _val_peer_addr = _peer_addr
    _peer_addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_peer_addr, _val_peer_addr)
    _peer_addr = struct.pack('<I', _peer_addr)
    _param += _peer_addr
    _param += struct.pack('<B', len(phy_configs))
    _phy_configs = b''.join([x.encode() for x in phy_configs])
    _val_phy_configs = _phy_configs
    _phy_configs = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_phy_configs, _val_phy_configs)
    _phy_configs = struct.pack('<I', _phy_configs)
    _param += _phy_configs
    _ret = brpc.call_fun(1046, _param)
    return uint8.deserialize(_ret)

def gap_create_connection_cancel() -> uint8 | int:
    log.LOG_D("gap_create_connection_cancel...")
    _param = b''
    
    _ret = brpc.call_fun(1047, _param)
    return uint8.deserialize(_ret)

def gap_set_data_length(connection_handle: uint16 | int,
        tx_octets: uint16 | int,
        tx_time: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_set_data_length...")
    _param = b''
    _connection_handle = (connection_handle if isinstance(connection_handle, uint16) else uint16(connection_handle)).encode()
    _param += _connection_handle
    _tx_octets = (tx_octets if isinstance(tx_octets, uint16) else uint16(tx_octets)).encode()
    _param += _tx_octets
    _tx_time = (tx_time if isinstance(tx_time, uint16) else uint16(tx_time)).encode()
    _param += _tx_time
    _ret = brpc.call_fun(1048, _param)
    return uint8.deserialize(_ret)

def gap_set_connectionless_cte_tx_param(adv_handle: uint8 | int,
        cte_len: uint8 | int,
        cte_type: cte_type,
        cte_count: uint8 | int,
        antenna_ids: bytes) -> uint8 | int:
    log.LOG_D("gap_set_connectionless_cte_tx_param...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _cte_len = (cte_len if isinstance(cte_len, uint8) else uint8(cte_len)).encode()
    _param += _cte_len
    _cte_type = cte_type.encode()
    _param += _cte_type
    _cte_count = (cte_count if isinstance(cte_count, uint8) else uint8(cte_count)).encode()
    _param += _cte_count
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _ret = brpc.call_fun(1049, _param)
    return uint8.deserialize(_ret)

def gap_set_connectionless_cte_tx_enable(adv_handle: uint8 | int,
        cte_enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_connectionless_cte_tx_enable...")
    _param = b''
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _cte_enable = (cte_enable if isinstance(cte_enable, uint8) else uint8(cte_enable)).encode()
    _param += _cte_enable
    _ret = brpc.call_fun(1050, _param)
    return uint8.deserialize(_ret)

def gap_set_connectionless_iq_sampling_enable(sync_handle: uint16 | int,
        sampling_enable: uint8 | int,
        slot_durations: cte_slot_duration_type,
        max_sampled_ctes: uint8 | int,
        antenna_ids: bytes) -> uint8 | int:
    log.LOG_D("gap_set_connectionless_iq_sampling_enable...")
    _param = b''
    _sync_handle = (sync_handle if isinstance(sync_handle, uint16) else uint16(sync_handle)).encode()
    _param += _sync_handle
    _sampling_enable = (sampling_enable if isinstance(sampling_enable, uint8) else uint8(sampling_enable)).encode()
    _param += _sampling_enable
    _slot_durations = slot_durations.encode()
    _param += _slot_durations
    _max_sampled_ctes = (max_sampled_ctes if isinstance(max_sampled_ctes, uint8) else uint8(max_sampled_ctes)).encode()
    _param += _max_sampled_ctes
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _ret = brpc.call_fun(1051, _param)
    return uint8.deserialize(_ret)

def gap_set_connection_cte_rx_param(conn_handle: hci_con_handle | int,
        sampling_enable: uint8 | int,
        slot_durations: cte_slot_duration_type,
        antenna_ids: bytes) -> uint8 | int:
    log.LOG_D("gap_set_connection_cte_rx_param...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _sampling_enable = (sampling_enable if isinstance(sampling_enable, uint8) else uint8(sampling_enable)).encode()
    _param += _sampling_enable
    _slot_durations = slot_durations.encode()
    _param += _slot_durations
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _ret = brpc.call_fun(1052, _param)
    return uint8.deserialize(_ret)

def gap_set_connection_cte_tx_param(conn_handle: hci_con_handle | int,
        cte_types: uint8 | int,
        antenna_ids: bytes) -> uint8 | int:
    log.LOG_D("gap_set_connection_cte_tx_param...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _cte_types = (cte_types if isinstance(cte_types, uint8) else uint8(cte_types)).encode()
    _param += _cte_types
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _ret = brpc.call_fun(1053, _param)
    return uint8.deserialize(_ret)

def gap_set_connection_cte_request_enable(conn_handle: hci_con_handle | int,
        enable: uint8 | int,
        requested_cte_interval: uint16 | int,
        requested_cte_length: uint8 | int,
        requested_cte_type: cte_type) -> uint8 | int:
    log.LOG_D("gap_set_connection_cte_request_enable...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _requested_cte_interval = (requested_cte_interval if isinstance(requested_cte_interval, uint16) else uint16(requested_cte_interval)).encode()
    _param += _requested_cte_interval
    _requested_cte_length = (requested_cte_length if isinstance(requested_cte_length, uint8) else uint8(requested_cte_length)).encode()
    _param += _requested_cte_length
    _requested_cte_type = requested_cte_type.encode()
    _param += _requested_cte_type
    _ret = brpc.call_fun(1054, _param)
    return uint8.deserialize(_ret)

def gap_set_connection_cte_response_enable(conn_handle: hci_con_handle | int,
        enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_connection_cte_response_enable...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _ret = brpc.call_fun(1055, _param)
    return uint8.deserialize(_ret)

def gap_read_antenna_info() -> uint8 | int:
    log.LOG_D("gap_read_antenna_info...")
    _param = b''
    
    _ret = brpc.call_fun(1056, _param)
    return uint8.deserialize(_ret)

def gap_set_periodic_adv_rx_enable(sync_handle: uint16 | int,
        enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_periodic_adv_rx_enable...")
    _param = b''
    _sync_handle = (sync_handle if isinstance(sync_handle, uint16) else uint16(sync_handle)).encode()
    _param += _sync_handle
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _ret = brpc.call_fun(1057, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_sync_transfer(conn_handle: hci_con_handle | int,
        service_data: uint16 | int,
        sync_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_periodic_adv_sync_transfer...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _service_data = (service_data if isinstance(service_data, uint16) else uint16(service_data)).encode()
    _param += _service_data
    _sync_handle = (sync_handle if isinstance(sync_handle, uint16) else uint16(sync_handle)).encode()
    _param += _sync_handle
    _ret = brpc.call_fun(1058, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_set_info_transfer(conn_handle: hci_con_handle | int,
        service_data: uint16 | int,
        adv_handle: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_periodic_adv_set_info_transfer...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _service_data = (service_data if isinstance(service_data, uint16) else uint16(service_data)).encode()
    _param += _service_data
    _adv_handle = (adv_handle if isinstance(adv_handle, uint8) else uint8(adv_handle)).encode()
    _param += _adv_handle
    _ret = brpc.call_fun(1059, _param)
    return uint8.deserialize(_ret)

def gap_periodic_adv_sync_transfer_param(conn_handle: hci_con_handle | int,
        mode: periodic_adv_sync_transfer_mode,
        skip: uint16 | int,
        sync_timeout: uint16 | int,
        cte_excl_types: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_periodic_adv_sync_transfer_param...")
    _param = b''
    _conn_handle = (conn_handle if isinstance(conn_handle, hci_con_handle) else hci_con_handle(conn_handle)).encode()
    _param += _conn_handle
    _mode = mode.encode()
    _param += _mode
    _skip = (skip if isinstance(skip, uint16) else uint16(skip)).encode()
    _param += _skip
    _sync_timeout = (sync_timeout if isinstance(sync_timeout, uint16) else uint16(sync_timeout)).encode()
    _param += _sync_timeout
    _cte_excl_types = (cte_excl_types if isinstance(cte_excl_types, uint8) else uint8(cte_excl_types)).encode()
    _param += _cte_excl_types
    _ret = brpc.call_fun(1060, _param)
    return uint8.deserialize(_ret)

def gap_default_periodic_adv_sync_transfer_param(mode: periodic_adv_sync_transfer_mode,
        skip: uint16 | int,
        sync_timeout: uint16 | int,
        cte_excl_types: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_default_periodic_adv_sync_transfer_param...")
    _param = b''
    _mode = mode.encode()
    _param += _mode
    _skip = (skip if isinstance(skip, uint16) else uint16(skip)).encode()
    _param += _skip
    _sync_timeout = (sync_timeout if isinstance(sync_timeout, uint16) else uint16(sync_timeout)).encode()
    _param += _sync_timeout
    _cte_excl_types = (cte_excl_types if isinstance(cte_excl_types, uint8) else uint8(cte_excl_types)).encode()
    _param += _cte_excl_types
    _ret = brpc.call_fun(1061, _param)
    return uint8.deserialize(_ret)

def gap_set_host_channel_classification(channel_low: uint32 | int,
        channel_high: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_host_channel_classification...")
    _param = b''
    _channel_low = (channel_low if isinstance(channel_low, uint32) else uint32(channel_low)).encode()
    _param += _channel_low
    _channel_high = (channel_high if isinstance(channel_high, uint8) else uint8(channel_high)).encode()
    _param += _channel_high
    _ret = brpc.call_fun(1062, _param)
    return uint8.deserialize(_ret)

def gap_update_connection_parameters(con_handle: hci_con_handle | int,
        conn_interval_min: uint16 | int,
        conn_interval_max: uint16 | int,
        conn_latency: uint16 | int,
        supervision_timeout: uint16 | int,
        min_ce_len: uint16 | int,
        max_ce_len: uint16 | int) -> int:
    log.LOG_D("gap_update_connection_parameters...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _conn_interval_min = (conn_interval_min if isinstance(conn_interval_min, uint16) else uint16(conn_interval_min)).encode()
    _param += _conn_interval_min
    _conn_interval_max = (conn_interval_max if isinstance(conn_interval_max, uint16) else uint16(conn_interval_max)).encode()
    _param += _conn_interval_max
    _conn_latency = (conn_latency if isinstance(conn_latency, uint16) else uint16(conn_latency)).encode()
    _param += _conn_latency
    _supervision_timeout = (supervision_timeout if isinstance(supervision_timeout, uint16) else uint16(supervision_timeout)).encode()
    _param += _supervision_timeout
    _min_ce_len = (min_ce_len if isinstance(min_ce_len, uint16) else uint16(min_ce_len)).encode()
    _param += _min_ce_len
    _max_ce_len = (max_ce_len if isinstance(max_ce_len, uint16) else uint16(max_ce_len)).encode()
    _param += _max_ce_len
    _ret = brpc.call_fun(1063, _param)
    return struct.unpack('<i', _ret)[0]

def gap_get_connection_parameter_range(range: le_connection_parameter_range):
    log.LOG_D("gap_get_connection_parameter_range...")
    _param = b''
    _range = range.encode()
    _val_range = _range
    _range = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_range, _val_range)
    _range = struct.pack('<I', _range)
    _param += _range
    brpc.call_void_fun(1064, _param)

def gap_set_connection_parameter_range(range: le_connection_parameter_range):
    log.LOG_D("gap_set_connection_parameter_range...")
    _param = b''
    _range = range.encode()
    _val_range = _range
    _range = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_range, _val_range)
    _range = struct.pack('<I', _range)
    _param += _range
    brpc.call_void_fun(1065, _param)

def gap_read_local_tx_power_level(con_handle: hci_con_handle | int,
        phy: unified_phy_type) -> uint8 | int:
    log.LOG_D("gap_read_local_tx_power_level...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _phy = phy.encode()
    _param += _phy
    _ret = brpc.call_fun(1066, _param)
    return uint8.deserialize(_ret)

def gap_read_remote_tx_power_level(con_handle: hci_con_handle | int,
        phy: unified_phy_type) -> uint8 | int:
    log.LOG_D("gap_read_remote_tx_power_level...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _phy = phy.encode()
    _param += _phy
    _ret = brpc.call_fun(1067, _param)
    return uint8.deserialize(_ret)

def gap_set_path_loss_reporting_param(con_handle: hci_con_handle | int,
        high_threshold: uint8 | int,
        high_hysteresis: uint8 | int,
        low_threshold: uint8 | int,
        low_hysteresis: uint8 | int,
        min_time_spent: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_path_loss_reporting_param...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _high_threshold = (high_threshold if isinstance(high_threshold, uint8) else uint8(high_threshold)).encode()
    _param += _high_threshold
    _high_hysteresis = (high_hysteresis if isinstance(high_hysteresis, uint8) else uint8(high_hysteresis)).encode()
    _param += _high_hysteresis
    _low_threshold = (low_threshold if isinstance(low_threshold, uint8) else uint8(low_threshold)).encode()
    _param += _low_threshold
    _low_hysteresis = (low_hysteresis if isinstance(low_hysteresis, uint8) else uint8(low_hysteresis)).encode()
    _param += _low_hysteresis
    _min_time_spent = (min_time_spent if isinstance(min_time_spent, uint8) else uint8(min_time_spent)).encode()
    _param += _min_time_spent
    _ret = brpc.call_fun(1068, _param)
    return uint8.deserialize(_ret)

def gap_set_path_loss_reporting_enable(con_handle: hci_con_handle | int,
        enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_path_loss_reporting_enable...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _ret = brpc.call_fun(1069, _param)
    return uint8.deserialize(_ret)

def gap_set_tx_power_reporting_enable(con_handle: hci_con_handle | int,
        local_enable: uint8 | int,
        remote_enable: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_set_tx_power_reporting_enable...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _local_enable = (local_enable if isinstance(local_enable, uint8) else uint8(local_enable)).encode()
    _param += _local_enable
    _remote_enable = (remote_enable if isinstance(remote_enable, uint8) else uint8(remote_enable)).encode()
    _param += _remote_enable
    _ret = brpc.call_fun(1070, _param)
    return uint8.deserialize(_ret)

def gap_set_default_subrate(subrate_min: uint16 | int,
        subrate_max: uint16 | int,
        max_latency: uint16 | int,
        continuation_number: uint16 | int,
        supervision_timeout: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_set_default_subrate...")
    _param = b''
    _subrate_min = (subrate_min if isinstance(subrate_min, uint16) else uint16(subrate_min)).encode()
    _param += _subrate_min
    _subrate_max = (subrate_max if isinstance(subrate_max, uint16) else uint16(subrate_max)).encode()
    _param += _subrate_max
    _max_latency = (max_latency if isinstance(max_latency, uint16) else uint16(max_latency)).encode()
    _param += _max_latency
    _continuation_number = (continuation_number if isinstance(continuation_number, uint16) else uint16(continuation_number)).encode()
    _param += _continuation_number
    _supervision_timeout = (supervision_timeout if isinstance(supervision_timeout, uint16) else uint16(supervision_timeout)).encode()
    _param += _supervision_timeout
    _ret = brpc.call_fun(1071, _param)
    return uint8.deserialize(_ret)

def gap_subrate_request(con_handle: hci_con_handle | int,
        subrate_min: uint16 | int,
        subrate_max: uint16 | int,
        max_latency: uint16 | int,
        continuation_number: uint16 | int,
        supervision_timeout: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_subrate_request...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _subrate_min = (subrate_min if isinstance(subrate_min, uint16) else uint16(subrate_min)).encode()
    _param += _subrate_min
    _subrate_max = (subrate_max if isinstance(subrate_max, uint16) else uint16(subrate_max)).encode()
    _param += _subrate_max
    _max_latency = (max_latency if isinstance(max_latency, uint16) else uint16(max_latency)).encode()
    _param += _max_latency
    _continuation_number = (continuation_number if isinstance(continuation_number, uint16) else uint16(continuation_number)).encode()
    _param += _continuation_number
    _supervision_timeout = (supervision_timeout if isinstance(supervision_timeout, uint16) else uint16(supervision_timeout)).encode()
    _param += _supervision_timeout
    _ret = brpc.call_fun(1072, _param)
    return uint8.deserialize(_ret)

def gap_rx_test_v2(rx_channel: uint8 | int,
        phy: uint8 | int,
        modulation_index: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_rx_test_v2...")
    _param = b''
    _rx_channel = (rx_channel if isinstance(rx_channel, uint8) else uint8(rx_channel)).encode()
    _param += _rx_channel
    _phy = (phy if isinstance(phy, uint8) else uint8(phy)).encode()
    _param += _phy
    _modulation_index = (modulation_index if isinstance(modulation_index, uint8) else uint8(modulation_index)).encode()
    _param += _modulation_index
    _ret = brpc.call_fun(1073, _param)
    return uint8.deserialize(_ret)

def gap_rx_test_v3(rx_channel: uint8 | int,
        phy: uint8 | int,
        modulation_index: uint8 | int,
        expected_cte_length: uint8 | int,
        expected_cte_type: uint8 | int,
        slot_durations: uint8 | int,
        antenna_ids: bytes) -> uint8 | int:
    log.LOG_D("gap_rx_test_v3...")
    _param = b''
    _rx_channel = (rx_channel if isinstance(rx_channel, uint8) else uint8(rx_channel)).encode()
    _param += _rx_channel
    _phy = (phy if isinstance(phy, uint8) else uint8(phy)).encode()
    _param += _phy
    _modulation_index = (modulation_index if isinstance(modulation_index, uint8) else uint8(modulation_index)).encode()
    _param += _modulation_index
    _expected_cte_length = (expected_cte_length if isinstance(expected_cte_length, uint8) else uint8(expected_cte_length)).encode()
    _param += _expected_cte_length
    _expected_cte_type = (expected_cte_type if isinstance(expected_cte_type, uint8) else uint8(expected_cte_type)).encode()
    _param += _expected_cte_type
    _slot_durations = (slot_durations if isinstance(slot_durations, uint8) else uint8(slot_durations)).encode()
    _param += _slot_durations
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _ret = brpc.call_fun(1074, _param)
    return uint8.deserialize(_ret)

def gap_tx_test_v2(tx_channel: uint8 | int,
        test_data_length: uint8 | int,
        packet_payload: uint8 | int,
        phy: uint8 | int) -> uint8 | int:
    log.LOG_D("gap_tx_test_v2...")
    _param = b''
    _tx_channel = (tx_channel if isinstance(tx_channel, uint8) else uint8(tx_channel)).encode()
    _param += _tx_channel
    _test_data_length = (test_data_length if isinstance(test_data_length, uint8) else uint8(test_data_length)).encode()
    _param += _test_data_length
    _packet_payload = (packet_payload if isinstance(packet_payload, uint8) else uint8(packet_payload)).encode()
    _param += _packet_payload
    _phy = (phy if isinstance(phy, uint8) else uint8(phy)).encode()
    _param += _phy
    _ret = brpc.call_fun(1075, _param)
    return uint8.deserialize(_ret)

def gap_tx_test_v4(tx_channel: uint8 | int,
        test_data_length: uint8 | int,
        packet_payload: uint8 | int,
        phy: uint8 | int,
        cte_length: uint8 | int,
        cte_type: uint8 | int,
        antenna_ids: bytes,
        tx_power_level: int8 | int) -> uint8 | int:
    log.LOG_D("gap_tx_test_v4...")
    _param = b''
    _tx_channel = (tx_channel if isinstance(tx_channel, uint8) else uint8(tx_channel)).encode()
    _param += _tx_channel
    _test_data_length = (test_data_length if isinstance(test_data_length, uint8) else uint8(test_data_length)).encode()
    _param += _test_data_length
    _packet_payload = (packet_payload if isinstance(packet_payload, uint8) else uint8(packet_payload)).encode()
    _param += _packet_payload
    _phy = (phy if isinstance(phy, uint8) else uint8(phy)).encode()
    _param += _phy
    _cte_length = (cte_length if isinstance(cte_length, uint8) else uint8(cte_length)).encode()
    _param += _cte_length
    _cte_type = (cte_type if isinstance(cte_type, uint8) else uint8(cte_type)).encode()
    _param += _cte_type
    _param += struct.pack('<B', len(antenna_ids))
    _antenna_ids = antenna_ids
    _val_antenna_ids = _antenna_ids
    _antenna_ids = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_antenna_ids, _val_antenna_ids)
    _antenna_ids = struct.pack('<I', _antenna_ids)
    _param += _antenna_ids
    _tx_power_level = (tx_power_level if isinstance(tx_power_level, int8) else int8(tx_power_level)).encode()
    _param += _tx_power_level
    _ret = brpc.call_fun(1076, _param)
    return uint8.deserialize(_ret)

def gap_test_end() -> uint8 | int:
    log.LOG_D("gap_test_end...")
    _param = b''
    
    _ret = brpc.call_fun(1077, _param)
    return uint8.deserialize(_ret)

def gap_vendor_tx_continuous_wave(enable: uint8 | int,
        power_level_index: uint8 | int,
        freq: uint16 | int) -> uint8 | int:
    log.LOG_D("gap_vendor_tx_continuous_wave...")
    _param = b''
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _power_level_index = (power_level_index if isinstance(power_level_index, uint8) else uint8(power_level_index)).encode()
    _param += _power_level_index
    _freq = (freq if isinstance(freq, uint16) else uint16(freq)).encode()
    _param += _freq
    _ret = brpc.call_fun(1078, _param)
    return uint8.deserialize(_ret)

def att_server_deferred_read_response(con_handle: hci_con_handle | int,
        attribute_handle: uint16 | int,
        value: bytes) -> int:
    log.LOG_D("att_server_deferred_read_response...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _attribute_handle = (attribute_handle if isinstance(attribute_handle, uint16) else uint16(attribute_handle)).encode()
    _param += _attribute_handle
    _value = value
    _val_value = _value
    _value = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_value, _val_value)
    _value = struct.pack('<I', _value)
    _param += _value
    _param += struct.pack('<H', len(value))
    _ret = brpc.call_fun(1079, _param)
    return struct.unpack('<i', _ret)[0]

def att_server_notify(con_handle: hci_con_handle | int,
        attribute_handle: uint16 | int,
        value: bytes) -> int:
    log.LOG_D("att_server_notify...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _attribute_handle = (attribute_handle if isinstance(attribute_handle, uint16) else uint16(attribute_handle)).encode()
    _param += _attribute_handle
    _value = value
    _val_value = _value
    _value = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_value, _val_value)
    _value = struct.pack('<I', _value)
    _param += _value
    _param += struct.pack('<H', len(value))
    _ret = brpc.call_fun(1080, _param)
    return struct.unpack('<i', _ret)[0]

def att_server_indicate(con_handle: hci_con_handle | int,
        attribute_handle: uint16 | int,
        value: bytes) -> int:
    log.LOG_D("att_server_indicate...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _attribute_handle = (attribute_handle if isinstance(attribute_handle, uint16) else uint16(attribute_handle)).encode()
    _param += _attribute_handle
    _value = value
    _val_value = _value
    _value = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_value, _val_value)
    _value = struct.pack('<I', _value)
    _param += _value
    _param += struct.pack('<H', len(value))
    _ret = brpc.call_fun(1081, _param)
    return struct.unpack('<i', _ret)[0]

def att_server_get_mtu(con_handle: hci_con_handle | int) -> uint16 | int:
    log.LOG_D("att_server_get_mtu...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1082, _param)
    return uint16.deserialize(_ret)

def gatt_client_discover_primary_services(callback: user_packet_handler_t,
        con_handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gatt_client_discover_primary_services...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1083, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_primary_services_by_uuid16(callback: user_packet_handler_t,
        con_handle: hci_con_handle | int,
        uuid16: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_discover_primary_services_by_uuid16...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _uuid16 = (uuid16 if isinstance(uuid16, uint16) else uint16(uuid16)).encode()
    _param += _uuid16
    _ret = brpc.call_fun(1084, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_primary_services_by_uuid128(callback: user_packet_handler_t,
        con_handle: hci_con_handle | int,
        uuid128: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_discover_primary_services_by_uuid128...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _uuid128 = uuid128
    _val_uuid128 = _uuid128
    _uuid128 = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_uuid128, _val_uuid128)
    _uuid128 = struct.pack('<I', _uuid128)
    _param += _uuid128
    _ret = brpc.call_fun(1085, _param)
    return uint8.deserialize(_ret)

def gatt_client_find_included_services_for_service(callback: user_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_group_handle: uint16 | int,
        end_group_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_find_included_services_for_service...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_group_handle = (start_group_handle if isinstance(start_group_handle, uint16) else uint16(start_group_handle)).encode()
    _param += _start_group_handle
    _end_group_handle = (end_group_handle if isinstance(end_group_handle, uint16) else uint16(end_group_handle)).encode()
    _param += _end_group_handle
    _ret = brpc.call_fun(1086, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_characteristics_for_service(callback: user_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_group_handle: uint16 | int,
        end_group_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_discover_characteristics_for_service...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_group_handle = (start_group_handle if isinstance(start_group_handle, uint16) else uint16(start_group_handle)).encode()
    _param += _start_group_handle
    _end_group_handle = (end_group_handle if isinstance(end_group_handle, uint16) else uint16(end_group_handle)).encode()
    _param += _end_group_handle
    _ret = brpc.call_fun(1087, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_characteristics_for_handle_range_by_uuid16(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_handle: uint16 | int,
        end_handle: uint16 | int,
        uuid16: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_discover_characteristics_for_handle_range_by_uuid16...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_handle = (start_handle if isinstance(start_handle, uint16) else uint16(start_handle)).encode()
    _param += _start_handle
    _end_handle = (end_handle if isinstance(end_handle, uint16) else uint16(end_handle)).encode()
    _param += _end_handle
    _uuid16 = (uuid16 if isinstance(uuid16, uint16) else uint16(uuid16)).encode()
    _param += _uuid16
    _ret = brpc.call_fun(1088, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_characteristics_for_handle_range_by_uuid128(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_handle: uint16 | int,
        end_handle: uint16 | int,
        uuid128: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_discover_characteristics_for_handle_range_by_uuid128...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_handle = (start_handle if isinstance(start_handle, uint16) else uint16(start_handle)).encode()
    _param += _start_handle
    _end_handle = (end_handle if isinstance(end_handle, uint16) else uint16(end_handle)).encode()
    _param += _end_handle
    _uuid128 = uuid128
    _val_uuid128 = _uuid128
    _uuid128 = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_uuid128, _val_uuid128)
    _uuid128 = struct.pack('<I', _uuid128)
    _param += _uuid128
    _ret = brpc.call_fun(1089, _param)
    return uint8.deserialize(_ret)

def gatt_client_discover_characteristic_descriptors(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic: gatt_client_characteristic) -> uint8 | int:
    log.LOG_D("gatt_client_discover_characteristic_descriptors...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic = characteristic.encode()
    _val_characteristic = _characteristic
    _characteristic = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_characteristic, _val_characteristic)
    _characteristic = struct.pack('<I', _characteristic)
    _param += _characteristic
    _ret = brpc.call_fun(1090, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_value_of_characteristic_using_value_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_value_of_characteristic_using_value_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _ret = brpc.call_fun(1091, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_value_of_characteristics_by_uuid16(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_handle: uint16 | int,
        end_handle: uint16 | int,
        uuid16: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_value_of_characteristics_by_uuid16...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_handle = (start_handle if isinstance(start_handle, uint16) else uint16(start_handle)).encode()
    _param += _start_handle
    _end_handle = (end_handle if isinstance(end_handle, uint16) else uint16(end_handle)).encode()
    _param += _end_handle
    _uuid16 = (uuid16 if isinstance(uuid16, uint16) else uint16(uuid16)).encode()
    _param += _uuid16
    _ret = brpc.call_fun(1092, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_value_of_characteristics_by_uuid128(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        start_handle: uint16 | int,
        end_handle: uint16 | int,
        uuid128: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_read_value_of_characteristics_by_uuid128...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _start_handle = (start_handle if isinstance(start_handle, uint16) else uint16(start_handle)).encode()
    _param += _start_handle
    _end_handle = (end_handle if isinstance(end_handle, uint16) else uint16(end_handle)).encode()
    _param += _end_handle
    _uuid128 = uuid128
    _param += _uuid128
    _ret = brpc.call_fun(1093, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_long_value_of_characteristic_using_value_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_long_value_of_characteristic_using_value_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _ret = brpc.call_fun(1094, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_long_value_of_characteristic_using_value_handle_with_offset(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        offset: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_long_value_of_characteristic_using_value_handle_with_offset...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _offset = (offset if isinstance(offset, uint16) else uint16(offset)).encode()
    _param += _offset
    _ret = brpc.call_fun(1095, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_multiple_characteristic_values(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        value_handles: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_multiple_characteristic_values...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _param += struct.pack('<i', len(value_handles))
    _value_handles = b''.join([(x if isinstance(x, uint16) else value_handles(x)).encode() for x in value_handles])
    _val_value_handles = _value_handles
    _value_handles = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_value_handles, _val_value_handles)
    _value_handles = struct.pack('<I', _value_handles)
    _param += _value_handles
    _ret = brpc.call_fun(1096, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_value_of_characteristic_without_response(con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_value_of_characteristic_without_response...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1097, _param)
    return uint8.deserialize(_ret)

def gatt_client_signed_write_without_response(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        handle: uint16 | int,
        message: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_signed_write_without_response...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _handle = (handle if isinstance(handle, uint16) else uint16(handle)).encode()
    _param += _handle
    _param += struct.pack('<H', len(message))
    _message = message
    _val_message = _message
    _message = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_message, _val_message)
    _message = struct.pack('<I', _message)
    _param += _message
    _ret = brpc.call_fun(1098, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_value_of_characteristic(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_value_of_characteristic...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1099, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_long_value_of_characteristic(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_long_value_of_characteristic...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1100, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_long_value_of_characteristic_with_offset(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        offset: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_long_value_of_characteristic_with_offset...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _offset = (offset if isinstance(offset, uint16) else uint16(offset)).encode()
    _param += _offset
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1101, _param)
    return uint8.deserialize(_ret)

def gatt_client_reliable_write_long_value_of_characteristic(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic_value_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_reliable_write_long_value_of_characteristic...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic_value_handle = (characteristic_value_handle if isinstance(characteristic_value_handle, uint16) else uint16(characteristic_value_handle)).encode()
    _param += _characteristic_value_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1102, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_characteristic_descriptor_using_descriptor_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_characteristic_descriptor_using_descriptor_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _ret = brpc.call_fun(1103, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_long_characteristic_descriptor_using_descriptor_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_long_characteristic_descriptor_using_descriptor_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _ret = brpc.call_fun(1104, _param)
    return uint8.deserialize(_ret)

def gatt_client_read_long_characteristic_descriptor_using_descriptor_handle_with_offset(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int,
        offset: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_read_long_characteristic_descriptor_using_descriptor_handle_with_offset...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _offset = (offset if isinstance(offset, uint16) else uint16(offset)).encode()
    _param += _offset
    _ret = brpc.call_fun(1105, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_characteristic_descriptor_using_descriptor_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_characteristic_descriptor_using_descriptor_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1106, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_long_characteristic_descriptor_using_descriptor_handle(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_long_characteristic_descriptor_using_descriptor_handle...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1107, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_long_characteristic_descriptor_using_descriptor_handle_with_offset(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        descriptor_handle: uint16 | int,
        offset: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_write_long_characteristic_descriptor_using_descriptor_handle_with_offset...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _descriptor_handle = (descriptor_handle if isinstance(descriptor_handle, uint16) else uint16(descriptor_handle)).encode()
    _param += _descriptor_handle
    _offset = (offset if isinstance(offset, uint16) else uint16(offset)).encode()
    _param += _offset
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1108, _param)
    return uint8.deserialize(_ret)

def gatt_client_write_client_characteristic_configuration(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        characteristic: gatt_client_characteristic,
        configuration: uint16 | int) -> uint8 | int:
    log.LOG_D("gatt_client_write_client_characteristic_configuration...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _characteristic = characteristic.encode()
    _val_characteristic = _characteristic
    _characteristic = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_characteristic, _val_characteristic)
    _characteristic = struct.pack('<I', _characteristic)
    _param += _characteristic
    _configuration = (configuration if isinstance(configuration, uint16) else uint16(configuration)).encode()
    _param += _configuration
    _ret = brpc.call_fun(1109, _param)
    return uint8.deserialize(_ret)

def gatt_client_prepare_write(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        attribute_handle: uint16 | int,
        offset: uint16 | int,
        data: bytes) -> uint8 | int:
    log.LOG_D("gatt_client_prepare_write...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _attribute_handle = (attribute_handle if isinstance(attribute_handle, uint16) else uint16(attribute_handle)).encode()
    _param += _attribute_handle
    _offset = (offset if isinstance(offset, uint16) else uint16(offset)).encode()
    _param += _offset
    _param += struct.pack('<H', len(data))
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _ret = brpc.call_fun(1110, _param)
    return uint8.deserialize(_ret)

def gatt_client_execute_write(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gatt_client_execute_write...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1111, _param)
    return uint8.deserialize(_ret)

def gatt_client_cancel_write(callback: btstack_packet_handler_t,
        con_handle: hci_con_handle | int) -> uint8 | int:
    log.LOG_D("gatt_client_cancel_write...")
    _param = b''
    _callback = struct.pack('<I', ObjectSim.address_of_object(callback))
    _param += _callback
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1112, _param)
    return uint8.deserialize(_ret)

def gatt_client_is_ready(con_handle: hci_con_handle | int) -> int:
    log.LOG_D("gatt_client_is_ready...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1113, _param)
    return struct.unpack('<i', _ret)[0]

def gatt_client_listen_for_characteristic_value_updates(packet_handler: btstack_packet_handler_t,
        con_handle: hci_con_handle | int,
        value_handle: uint16 | int):
    log.LOG_D("gatt_client_listen_for_characteristic_value_updates...")
    _param = b''
    _obj_notification = gatt_client_notification()
    _notification = ObjectSim.address_of_object(_obj_notification)
    brpc.alloc_heap_for_conn(_notification, len(_obj_notification.encode()), con_handle)
    _notification = struct.pack('<I', _notification)
    _param += _notification
    _packet_handler = struct.pack('<I', ObjectSim.address_of_object(packet_handler))
    _param += _packet_handler
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _value_handle = (value_handle if isinstance(value_handle, uint16) else uint16(value_handle)).encode()
    _param += _value_handle
    brpc.call_void_fun(1114, _param)

def sm_config(enable: uint8 | int,
        io_capability: io_capability,
        request_security: int,
        persistent: sm_persistent) -> int:
    log.LOG_D("sm_config...")
    _param = b''
    _enable = (enable if isinstance(enable, uint8) else uint8(enable)).encode()
    _param += _enable
    _io_capability = io_capability.encode()
    _param += _io_capability
    _request_security = struct.pack('<i', request_security)
    _param += _request_security
    _persistent = persistent.encode()
    _param += _persistent
    _ret = brpc.call_fun(1115, _param)
    return struct.unpack('<i', _ret)[0]

def sm_private_random_address_generation_set_mode(random_address_type: gap_random_address_type):
    log.LOG_D("sm_private_random_address_generation_set_mode...")
    _param = b''
    _random_address_type = random_address_type.encode()
    _param += _random_address_type
    brpc.call_void_fun(1116, _param)

def sm_private_random_address_generation_get_mode() -> gap_random_address_type:
    log.LOG_D("sm_private_random_address_generation_get_mode...")
    _param = b''
    
    _ret = brpc.call_fun(1117, _param)
    return gap_random_address_type.deserialize(_ret)

def sm_private_random_address_generation_set_update_period(period_ms: int):
    log.LOG_D("sm_private_random_address_generation_set_update_period...")
    _param = b''
    _period_ms = struct.pack('<i', period_ms)
    _param += _period_ms
    brpc.call_void_fun(1118, _param)

def sm_set_accepted_stk_generation_methods(accepted_stk_generation_methods: uint8 | int):
    log.LOG_D("sm_set_accepted_stk_generation_methods...")
    _param = b''
    _accepted_stk_generation_methods = (accepted_stk_generation_methods if isinstance(accepted_stk_generation_methods, uint8) else uint8(accepted_stk_generation_methods)).encode()
    _param += _accepted_stk_generation_methods
    brpc.call_void_fun(1119, _param)

def sm_set_encryption_key_size_range(min_size: uint8 | int,
        max_size: uint8 | int):
    log.LOG_D("sm_set_encryption_key_size_range...")
    _param = b''
    _min_size = (min_size if isinstance(min_size, uint8) else uint8(min_size)).encode()
    _param += _min_size
    _max_size = (max_size if isinstance(max_size, uint8) else uint8(max_size)).encode()
    _param += _max_size
    brpc.call_void_fun(1120, _param)

def sm_set_authentication_requirements(auth_req: uint8 | int):
    log.LOG_D("sm_set_authentication_requirements...")
    _param = b''
    _auth_req = (auth_req if isinstance(auth_req, uint8) else uint8(auth_req)).encode()
    _param += _auth_req
    brpc.call_void_fun(1121, _param)

def sm_address_resolution_lookup(addr_type: uint8 | int,
        addr: bd_addr) -> int:
    log.LOG_D("sm_address_resolution_lookup...")
    _param = b''
    _addr_type = (addr_type if isinstance(addr_type, uint8) else uint8(addr_type)).encode()
    _param += _addr_type
    _addr = addr.encode()
    _val_addr = _addr
    _addr = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_addr, _val_addr)
    _addr = struct.pack('<I', _addr)
    _param += _addr
    _ret = brpc.call_fun(1122, _param)
    return struct.unpack('<i', _ret)[0]

def sm_config_conn(con_handle: hci_con_handle | int,
        io_capability: io_capability,
        auth_req: uint8 | int):
    log.LOG_D("sm_config_conn...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _io_capability = io_capability.encode()
    _param += _io_capability
    _auth_req = (auth_req if isinstance(auth_req, uint8) else uint8(auth_req)).encode()
    _param += _auth_req
    brpc.call_void_fun(1123, _param)

def sm_set_key_distribution_flags(flags: uint8 | int):
    log.LOG_D("sm_set_key_distribution_flags...")
    _param = b''
    _flags = (flags if isinstance(flags, uint8) else uint8(flags)).encode()
    _param += _flags
    brpc.call_void_fun(1124, _param)

def sm_bonding_decline(con_handle: hci_con_handle | int):
    log.LOG_D("sm_bonding_decline...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1125, _param)

def sm_just_works_confirm(con_handle: hci_con_handle | int):
    log.LOG_D("sm_just_works_confirm...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1126, _param)

def sm_passkey_input(con_handle: hci_con_handle | int,
        passkey: uint32 | int):
    log.LOG_D("sm_passkey_input...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _passkey = (passkey if isinstance(passkey, uint32) else uint32(passkey)).encode()
    _param += _passkey
    brpc.call_void_fun(1127, _param)

def sm_send_security_request(con_handle: hci_con_handle | int):
    log.LOG_D("sm_send_security_request...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1128, _param)

def sm_encryption_key_size(con_handle: hci_con_handle | int) -> int:
    log.LOG_D("sm_encryption_key_size...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1129, _param)
    return struct.unpack('<i', _ret)[0]

def sm_authenticated(con_handle: hci_con_handle | int) -> int:
    log.LOG_D("sm_authenticated...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1130, _param)
    return struct.unpack('<i', _ret)[0]

def sm_authorization_state(con_handle: hci_con_handle | int) -> authorization_state:
    log.LOG_D("sm_authorization_state...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1131, _param)
    return authorization_state.deserialize(_ret)

def sm_request_pairing(con_handle: hci_con_handle | int):
    log.LOG_D("sm_request_pairing...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1132, _param)

def sm_authorization_decline(con_handle: hci_con_handle | int):
    log.LOG_D("sm_authorization_decline...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1133, _param)

def sm_authorization_grant(con_handle: hci_con_handle | int):
    log.LOG_D("sm_authorization_grant...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    brpc.call_void_fun(1134, _param)

def sm_le_device_key(con_handle: hci_con_handle | int) -> int:
    log.LOG_D("sm_le_device_key...")
    _param = b''
    _con_handle = (con_handle if isinstance(con_handle, hci_con_handle) else hci_con_handle(con_handle)).encode()
    _param += _con_handle
    _ret = brpc.call_fun(1135, _param)
    return struct.unpack('<i', _ret)[0]

def kv_remove_all():
    log.LOG_D("kv_remove_all...")
    _param = b''
    
    brpc.call_void_fun(1136, _param)

def kv_remove(key: kvkey | int):
    log.LOG_D("kv_remove...")
    _param = b''
    _key = (key if isinstance(key, kvkey) else kvkey(key)).encode()
    _param += _key
    brpc.call_void_fun(1137, _param)

def kv_put(key: kvkey | int,
        data: bytes) -> int:
    log.LOG_D("kv_put...")
    _param = b''
    _key = (key if isinstance(key, kvkey) else kvkey(key)).encode()
    _param += _key
    _data = data
    _val_data = _data
    _data = ObjectSim.make_unique_address()
    brpc.remote_mem_map(_data, _val_data)
    _data = struct.pack('<I', _data)
    _param += _data
    _param += struct.pack('<h', len(data))
    _ret = brpc.call_fun(1138, _param)
    return struct.unpack('<i', _ret)[0]

def kv_value_modified():
    log.LOG_D("kv_value_modified...")
    _param = b''
    
    brpc.call_void_fun(1139, _param)

def kv_commit(flag_always_write: int):
    log.LOG_D("kv_commit...")
    _param = b''
    _flag_always_write = struct.pack('<i', flag_always_write)
    _param += _flag_always_write
    brpc.call_void_fun(1140, _param)

def le_device_db_remove_key(index: int):
    log.LOG_D("le_device_db_remove_key...")
    _param = b''
    _index = struct.pack('<i', index)
    _param += _index
    brpc.call_void_fun(1141, _param)

