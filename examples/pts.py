import os, sys
import logging
import time
import datetime
import ctypes
from ctypes import*
from random import *
import threading
import shutil
from os.path import basename
import codecs
from lxml import etree
import collections

from constants import *

from ble_rpc_client.log import LOG_OK, LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL, LOG_I, LOG_D, LOG_E, LOG_W

PTS_DIR = "C:\\Program Files (x86)\\Bluetooth SIG\\Bluetooth PTS\\bin\\"

class ETSAssetProvider:
    def __init__(self, pts_dir, ets_name):

        self.log      = logging.getLogger("Logger")
        self.pts_dir  = pts_dir
        self.ets_name = ets_name

        self.__init()

    @classmethod
    def instantiateEtsAsset(cls, pts_dir, ets_name):
        # xml path
        xmlFilePath = os.path.join(pts_dir, 'Bluetooth\\Ets\\{0}.xml'.format(ets_name))
        if not os.path.exists(xmlFilePath):
            return None
        else:
            return cls(pts_dir, ets_name)

    #############################################################
    #############################################################
    def getIcsAsset(self):
        return self.ets_ics

    #############################################################
    #############################################################
    def getIxitAsset(self):
        return self.ets_ixit

    #############################################################
    #############################################################
    def getTcAsset(self):
        return self.ets_tc

    #############################################################
    #############################################################

    def __init(self):

        locations = []
        locations.append(os.path.join(self.pts_dir, 'Bluetooth\\Ets'))
        locations.append(os.path.join(self.pts_dir, 'Bluetooth\\PICSX'))
        locations.append(os.path.join(self.pts_dir, 'Bluetooth\\PIXITX'))

        self.ets_db_file_info = collections.OrderedDict()
        for location in locations:
            for file in os.listdir(location):
                fileinfo = os.path.splitext(file)
                if fileinfo[0] == self.ets_name:
                    self.ets_db_file_info[fileinfo[1][1:].lower()] = os.path.join(location, file)

        self.__construct_tc()
        self.__construct_ics()
        self.__construct_ixit()

    #############################################################
    #############################################################

    def __construct_tc(self):
        self.ets_tc = collections.OrderedDict()
        fp = codecs.open(self.ets_db_file_info['xml'], 'r', 'UTF-8') #open(self.ets_db_file_info['xml'])
        tree = etree.parse(fp)
        for el in tree.findall('.//TestCase'):
            name      = el.attrib['Name']
            if 'Description' in el.attrib:
                desc = el.attrib['Description']
            else:
                desc = ''
            if 'Mapping' in el.attrib:
                mapping = el.attrib['Mapping']
            else:
                mapping = ''
            if 'Reference' in el.attrib:
                reference = el.attrib['Reference']
            else:
                reference = ''
            if not name.endswith('_HELPER'):
                self.ets_tc[name] = { 'desc' : desc, 'mapping' : mapping, 'reference': reference}

    #############################################################
    #############################################################

    def __construct_ics(self):
        self.ets_ics = collections.OrderedDict()
        fp = codecs.open(self.ets_db_file_info['picsx'], 'r', 'UTF-8') #fp = open(self.ets_db_file_info['picsx'])
        tree = etree.parse(fp)
        for el in tree.findall('.//Row'):
            name  = el.findtext('Name',        default = 'None')
            desc  = el.findtext('Description', default = 'None')
            value = el.findtext('Value',       default = 'None')
            mand  = el.findtext('Mandatory',   default = 'None')
            self.ets_ics[name] = { 'desc' : desc, 'value' : value, 'mand': mand}

    #############################################################
    #############################################################

    def __construct_ixit(self):
        self.ets_ixit = collections.OrderedDict()
        fp = codecs.open(self.ets_db_file_info['pixitx'], 'r', 'UTF-8') #fp = open(self.ets_db_file_info['pixitx'])
        tree = etree.parse(fp)
        for el in tree.findall('.//Row'):
            name   = el.findtext('Name',        default = 'None')
            desc   = el.findtext('Description', default = 'None')
            value  = el.findtext('Value',       default = 'None')
            elType = el.findtext('Type',        default = 'None')
            self.ets_ixit[name] = { 'desc' : desc, 'value' : value, 'type': elType}

USEAUTOIMPLSENDFUNC    = CFUNCTYPE(c_bool)
DONGLE_MSG_FUNC        = CFUNCTYPE(c_bool, c_char_p)
DEVICE_SEARCH_MSG_FUNC = CFUNCTYPE(c_bool, c_char_p, c_char_p, c_char_p)
LOGFUNC                = CFUNCTYPE(c_bool, c_char_p, c_char_p, c_char_p, c_int, c_void_p)
ONIMPLSENDFUNC         = CFUNCTYPE(c_char_p, c_char_p, c_int)
SEH_CALLBACK_FUNC      = CFUNCTYPE(None, c_ulong)

class PTSAutomation:
    def __init__(self, pts_dir, pts_workspace_dir, ets_name, batch_name, ets_handler, tester, dongle_type = 'laird', allow_dongle_fallback = True):

        self.log                    = logging.getLogger("Logger")
        self.current_dir            = os.getcwd()

        self.pts_dir                = pts_dir
        self.ets_manager_dir        = os.path.join(pts_dir, "ETSManager.dll")
        self.implicit_send_dir      = os.path.join(pts_dir + "implicit_send3.dll")
        self.ets_name               = ets_name
        self.batch_name             = batch_name
        self.ets_handler            = ets_handler
        self.tc_log_path            = None
        self.dongle_type            = dongle_type
        self.allow_dongle_fallback  = allow_dongle_fallback

        # workspace path = <pts_workspace_dir> \ <ets_name>_<current_date_time>
        ts = time.time()
        cur_datetime = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%H_%M_%S')

        if (tester is not None) and (tester != ''):
            if 'LT2' in tester:
                self.workspace_dir = os.path.join(pts_workspace_dir, batch_name + '_' + tester)
            else:
                self.workspace_dir = os.path.join(pts_workspace_dir, batch_name + '_' + tester + '_' + cur_datetime)
                # since this is LT1, we should remove residual LT2 workspace folder (from previous runs)
                shutil.rmtree(os.path.join(pts_workspace_dir, batch_name + '_HELPER LT2'), ignore_errors=True)
            self.tester_name = '[' + tester + ']'
        else:
            self.workspace_dir = os.path.join(pts_workspace_dir, batch_name + '_' + cur_datetime)
            self.tester_name = ''

        self.workspace_dir = os.path.normpath(self.workspace_dir)
        LOG_I("Log {0}".format(self.workspace_dir))

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

        # result path = <pts_workspace_dir> \ <ets_name>_<current_date_time> \ automation_result
        self.automation_result_workspace_dir = os.path.join(self.workspace_dir + '\\automation_result\\' )
        if not os.path.exists(self.automation_result_workspace_dir):
            os.makedirs(self.automation_result_workspace_dir)

        self.pts_address = None
        self.prepared   = False
        self.tc_name    = ''

        self.ets         = None
        self.ets_assets  = None

        self.ets_state_subscriber = None

        self.ets_tc     = {}
        self.ets_ics    = {}
        self.ets_ixit   = {}

        self.test_result = RESULT_INCOMP
        self.dongle_legacy_mode = False

        # Define callback functions
        self.use_auto_impl_send_func = USEAUTOIMPLSENDFUNC(self.UseAutoImplicitSend)
        self.dongle_msg_func         = DONGLE_MSG_FUNC(self.DongleMsg)
        self.dev_search_msg_func     = DEVICE_SEARCH_MSG_FUNC(self.DeviceSearchMsg)
        self.log_func                = LOGFUNC(self.Log)
        self.onimplsend_func         = ONIMPLSENDFUNC(self.ImplicitSend)
        self.seh_func                = SEH_CALLBACK_FUNC(self.SehHandleFunc)
        self.pts_crashed_func        = None

        self.__init()

    ############################################################
    ############################################################
    def __init(self):
        # Change working directory to the PTS installation directory
        os.chdir(self.pts_dir)
        print(self.ets_manager_dir)
        self.ets = cdll.LoadLibrary(self.ets_manager_dir)
        LOG_I("[PTSAutomation]{0:s} ETS Manager library {1:s} has been loaded".format(self.tester_name, self.ets_manager_dir))

        res = self.__initGetDevInfo()
        if res is not True:
            LOG_I("[PTSAutomation]{0:s} Device Info has failed initialization.".format(self.tester_name))

        self.__initPTSDongle()

        res = self.__initETS()
        if res is not True:
            LOG_I("[PTSAutomation]{0:s} ETS initialization failed.".format(self.tester_name))

        self.__loadETSAssets()

        # Change the current working directory to the workspace directory
        print('{0:s}Changing DIR to {1}'.format(self.tester_name, self.workspace_dir))
        os.chdir(self.workspace_dir) # os.chdir(self.current_dir)

    ############################################################
    ############################################################
    def __initETS(self):
        self.ets.RegisterProfileWithCallbacks.restype = c_bool
        self.ets.RegisterProfileWithCallbacks.argtypes = [c_char_p, \
                                                          USEAUTOIMPLSENDFUNC,
                                                          ONIMPLSENDFUNC, \
                                                          LOGFUNC, \
                                                          DEVICE_SEARCH_MSG_FUNC, \
                                                          DONGLE_MSG_FUNC]

        res = self.ets.RegisterProfileWithCallbacks(self.ets_name.encode('UTF-8'), \
                                                    self.use_auto_impl_send_func, \
                                                    self.onimplsend_func, \
                                                    self.log_func, \
                                                    self.dev_search_msg_func, \
                                                    self.dongle_msg_func)

        LOG_D("[PTSAutomation]{0:s} {1:s} has been registered with result {2:s}".format(self.tester_name, self.ets_name, str(res)))
        return res

    ############################################################
    ############################################################
    def __initGetDevInfo(self):
        self.ets.RegisterSehCallback.argtypes = [ SEH_CALLBACK_FUNC ]
        self.ets.RegisterSehCallback(self.seh_func)

        self.ets.InitGetDevInfoWithCallbacks.restype = c_bool
        self.ets.InitGetDevInfoWithCallbacks.argtypes = [c_char_p, \
                                                         DEVICE_SEARCH_MSG_FUNC, \
                                                         DONGLE_MSG_FUNC]

        res = self.ets.InitGetDevInfoWithCallbacks(self.pts_dir.encode('UTF-8'),  \
                                                   self.dev_search_msg_func, \
                                                   self.dongle_msg_func)

        LOG_D("[PTSAutomation] {0} GetDevInfo has been initialized with result {1:s}".format(self.tester_name, str(res)))
        return res

    ############################################################
    ############################################################
    def __initPTSDongle(self):
        if hasattr(self.ets, 'GetDeviceList'):
            self.dongle_legacy_mode = False
            LOG_PROG("[PTSAutomation] GetDeviceList() found in etsManager. Desired dongle type is {0:s}.".format(self.dongle_type))

            self.ets.GetDeviceList.restype = ctypes.c_char_p
            bDeviceList = self.ets.GetDeviceList()
            sDeviceList = bDeviceList.decode("utf-8")
            if len(sDeviceList) < 1:
                LOG_E("[PTSAutomation] cannot find a dongle to connect")
                sys.exit(-1)

            aDeviceList = sDeviceList.split(';')
            LOG_OK("[PTSAutomation] Device List: " + sDeviceList)

            deviceToConnect = None

            # look at each device
            for sDevice in aDeviceList:
                # parse each device data
                # e.g.
                # COM format -> 'COM7'
                # USB format -> 'USB:Free:6&10EF065E&3&1' ('Free' or 'InUse')
                aInfo = sDevice.split(':')
                if ('COM' in aInfo[0]) and ('laird' in self.dongle_type.lower()):
                    deviceToConnect = aInfo[0]
                    break

                if ('USB' in aInfo[0]) and ('qualcomm' in self.dongle_type.lower()) and (len(aInfo) == 3):
                    if aInfo[1] == 'Free':
                        deviceToConnect = aInfo[2]
                        break

            # if we dont get a match above but fallback is allowed, let's check for any available dongle
            if deviceToConnect is None and self.allow_dongle_fallback:
                LOG_E("[PTSAutomation] Expected dongle not available. Fallback invoked.")
                for sDevice in aDeviceList:
                    aInfo = sDevice.split(':')
                    if ('COM' in aInfo[0]):
                        deviceToConnect = aInfo[0]
                        break
                    if ('USB' in aInfo[0]) and (len(aInfo) == 3) and (aInfo[1] == 'Free'):
                        deviceToConnect = aInfo[2]
                        break

            if deviceToConnect is None:
                LOG_E("[PTSAutomation] none of the returned device was available for usage")
                sys.exit(-1)

            LOG_PROG("[PTSAutomation] Connecting to {0} ".format(deviceToConnect))
            self.ets.SetPTSDevice.argtypes = [ctypes.c_char_p]
            # self.ets.SetPTSDevice(deviceToConnect.encode("utf-8"))

        else:
            # LEGACY
            self.dongle_legacy_mode = True
            LOG_E("[PTSAutomation] GetDeviceList() NOT in etsManager. Falling back to 'USB'. (Desired dongle type is {0:s})".format(self.dongle_type))
            self.ets.VerifyDongleEx.restype = c_bool
            res = self.ets.VerifyDongleEx()
            LOG_D("[PTSAutomation] {0} PTS dongle has been initialized with result {1:s}".format(self.tester_name, str(res)))
            if res is not True:
                self.pts_address = "{0:012X}".format(0x0)
                LOG_OK("[PTSAutomation] {0} PTS BD Address: {1}".format(self.tester_name, self.pts_address))
                sys.exit(-1)
        dongle_address = None
        self.ets.GetDongleBDAddress.restype = ctypes.c_ulonglong

        if self.dongle_legacy_mode:
            self.ets.GetDongleBDAddress.restype = ctypes.c_ulonglong
            dongle_address = self.ets.GetDongleBDAddress()
            self.pts_address = "{0:012X}".format(dongle_address)
            LOG_OK("[PTSAutomation] {0} PTS BD Address: {1}".format(self.tester_name, self.pts_address))

            if dongle_address is None or dongle_address == 0:
                LOG_E("[PTSAutomation] {0} Failed to connect to PTS dongle".format(self.tester_name))
                sys.exit(-1)
        else: # retrying when it is not legacy mode
            count = 0
            while True:
                self.ets.SetPTSDevice(deviceToConnect.encode("utf-8"))
                dongle_address = self.ets.GetDongleBDAddress()
                if dongle_address is None or dongle_address == 0:
                    count = count + 1
                    LOG_E("[PTSAutomation] {0} Failed to connect to PTS dongle".format(self.tester_name))
                    if count > 3:
                        sys.exit(-1)
                    LOG_D("[PTSAutomation] {0} Retrying to connect to PTS dongle after 15s- {1}/3".format(self.tester_name, count))
                    self.ets.SetPTSDevice(''.encode("utf-8")) # disconnect dongle
                else:
                    self.pts_address = "{0:012X}".format(dongle_address)
                    LOG_D("[PTSAutomation] {0} PTS BD Address: {1}".format(self.tester_name, self.pts_address))
                    break

    def __loadETSAssets(self):
        self.ets_assets = ETSAssetProvider.instantiateEtsAsset(self.pts_dir, self.ets_name)

        message = 'Assets have been loaded for'
        if self.ets_assets is None:
            message = 'Failed to load assets for'
            LOG_E("[PTSAutomation] {0:s} {1} {2}".format(self.tester_name, message, self.ets_name))
        else:
            message = 'Assets have been loaded for'
            LOG_OK("[PTSAutomation] {0:s} {1} {2}".format(self.tester_name, message, self.ets_name))

    def __prepareToStart(self):
        self.ets.InitEtsEx.restype = c_bool
        self.ets.InitEtsEx.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        res = self.ets.InitEtsEx(self.ets_name.encode("utf-8"),\
                                 self.workspace_dir.encode("utf-8"), \
                                 self.implicit_send_dir.encode("utf-8"), \
                                 self.pts_address.encode("utf-8"))
        if res:
            LOG_OK("[PTSAutomation] {0:s} ETS initialized successfully".format(self.tester_name))
        else:
            LOG_E("[PTSAutomation] {0:s} ETS failed to be initialize".format(self.tester_name))

        # Initialize Host Stack DLL
        self.ets.InitStackEx.restype = c_bool
        self.ets.InitStackEx.argtypes = [c_char_p]
        res = self.ets.InitStackEx(self.ets_name.encode("utf-8"))
        if res:
            LOG_OK("[PTSAutomation] {0:s} Stack initialized successfully".format(self.tester_name))
        else:
            LOG_E("[PTSAutomation] {0:s} Stack failed to be initialize".format(self.tester_name))

        # Select to receive Log messages after test is done
        self.ets.SetPostLoggingEx.argtypes = [c_bool, c_char_p]
        self.ets.SetPostLoggingEx(False, self.ets_name.encode("utf-8"))
        self.prepared = True

    ############################################################
    ############################################################
    def setETSStateSubscriber(self, subscriber):
        self.ets_state_subscriber = subscriber

    def callETSStateSubscriber(self, tc_name, test_result_s, logfiles_to_store):
        if self.ets_state_subscriber is not None:
            self.ets_state_subscriber(tc_name, test_result_s, logfiles_to_store)

    ############################################################
    ############################################################
    def getETSName(self):
        return self.ets_name

    ############################################################
    ############################################################
    def getPTSBDAddr(self):
        return self.pts_address

    ############################################################
    ############################################################
    def getIcs(self):
        return self.ets_ics

    ############################################################
    ############################################################
    def getIxit(self):
        return self.ets_ixit

    ############################################################
    ############################################################
    def getTestcases(self):
        return self.ets_assets.getTcAsset()

    ############################################################
    ############################################################
    def setIcsParameters(self, icsParameters=None):
        self.ets.SetParameterEx.restype = c_bool
        self.ets.SetParameterEx.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        ics_assets = self.ets_assets.getIcsAsset()
        for ics_key in ics_assets:
            # default ics value from assets
            ics_name  = ics_key
            ics_value = ics_assets[ics_key]['value']

            # overwrite value from passed parameters
            if icsParameters and ics_key in icsParameters:
                ics_value = icsParameters[ics_key]

            # set ics value
            self.ets_ics[ics_key] = ics_value
            res = self.ets.SetParameterEx(ics_name.encode('UTF-8'), \
                                          b'BOOLEAN', \
                                          ics_value.encode('UTF-8'), \
                                          self.ets_name.encode('UTF-8'))
            if not res:
                LOG_E("[PTSAutomation] {0} Setting ICS {1:s} value failed".format(self.tester_name, ics_name))
            #else:
                #LOG_D("[PTSAutomation] Setting ICS {0:s} Completed: {1:s} ".format(ics_name, ics_value))

        LOG_OK("[PTSAutomation] {0:s} ICS(s) have been set for {1}".format(self.tester_name, self.ets_name))

    ############################################################
    ############################################################
    def setIxitParameters(self, ixitParameters=None):
        self.ets.SetParameterEx.restype = c_bool
        self.ets.SetParameterEx.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        ixit_assets = self.ets_assets.getIxitAsset()

        #set iut BD Address
        iut_bd_address = self.ets_handler._iut_address
        if  iut_bd_address is not None:
            LOG_D("[PTSAutomation]{0:s} IUT BD ADDRESS {1:s}".format(self.tester_name, iut_bd_address))
            ixitParameters['TSPX_bd_addr_iut'] = str(iut_bd_address)

        #override ixit settings of workspace from test config
        for ixit_key in ixit_assets:
            ixit_name  = ixit_key
            ixit_type  = ixit_assets[ixit_key]['type']
            ixit_value = ixit_assets[ixit_key]['value']

            # overwrite value from passed parameters
            if ixitParameters and ixit_key in ixitParameters:
                ixit_value = ixitParameters[ixit_key]
                ixit_assets[ixit_key]['value'] = ixit_value

            # set ixit value
            self.ets_ixit[ixit_key] = ixit_value
            res = self.ets.SetParameterEx(ixit_name.encode('UTF-8'), \
                                          ixit_type.encode('UTF-8'), \
                                          ixit_value.encode('UTF-8'),
                                          self.ets_name.encode('UTF-8'))
            if not res:
                LOG_E("[PTSAutomation] {0} Setting IXIT {1:s} value failed".format(self.tester_name, ixit_name))
            #else:
            #    LOG_D("[PTSAutomation] Setting IXIT {0:s} Completed: {1:s} ".format(ixit_name, ixit_value))

        LOG_OK("[PTSAutomation] {0:s} IXIT(s) have been set for {1}".format(self.tester_name, self.ets_name))

    ############################################################
    ############################################################
    def startTestcase(self, testcaseName, startingMsg):

        res = False

        if not self.prepared:
            self.__prepareToStart()

        # Custom Init Procedure
        self.ets_handler.onBeforeTestcaseStart(testcaseName)

        # If iut bd address is known, then update ixit
        iut_bd_address = self.ets_handler._iut_address
        assert iut_bd_address is not None

        if  (iut_bd_address is not None) and (iut_bd_address != self.ets_ixit.get('TSPX_bd_addr_iut')):
            LOG_D("[PTSAutomation]{0:s} IUT BD ADDRESS {1:s}".format(self.tester_name, iut_bd_address))
            res = self.ets.SetParameterEx("TSPX_bd_addr_iut".encode('UTF-8'), \
                                          "OCTETSTRING".encode('UTF-8'), \
                                          iut_bd_address.encode('UTF-8'),
                                          self.ets_name.encode('UTF-8'))

        # Print starting message
        LOG_D("{0:s}".format(startingMsg))

        # indivisual log file
        ts = time.time()
        cur_datetime = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%H_%M_%S')
        name = testcaseName.replace('/', '_')
        self.tc_log_path = os.path.join(self.automation_result_workspace_dir, name + '_' + cur_datetime + '.log')

        if self.pts_address is not None and self.pts_address != '000000000000':
            count = 0
            while count < 3:
                self.ets.StartTestCaseEx.restype = c_bool
                self.ets.StartTestCaseEx.argtypes = [c_char_p, c_char_p, c_bool]
                res = self.ets.StartTestCaseEx(testcaseName.encode("utf-8"), self.ets_name.encode("utf-8"), True)
                LOG_D("[PTSAutomation]{0:s} {1:s} has been started with result {2:s}".format(self.tester_name, testcaseName, str(res)))
                if res == True:
                    break
                count = count + 1
                time.sleep(1)
        else:
            res = False

        # State Changed
        self.tc_name = testcaseName

        if res is not True:
            test_result = "NONE"
            self.ets_handler.onFinalVerdictReceive(test_result)
            self.callETSStateSubscriber(self.tc_name, test_result, None)
            self.tc_name = ''

        return res

    ############################################################
    ############################################################
    def stopTestcase(self, testcaseName):

        # Stop selected test
        self.ets.StopTestCaseEx.restype = c_bool
        self.ets.StopTestCaseEx.argtypes = [c_char_p, c_char_p]
        res = self.ets.StopTestCaseEx(testcaseName.encode("utf-8"), \
                                       self.ets_name.encode("utf-8"))
        LOG_D("[PTSAutomation]{0:s} {1:s} has been stopped with result {2:s}".format(self.tester_name, testcaseName, str(res)))

        # Inform to ETSHandler
        self.ets_handler.onTestcaseStop()

    ############################################################
    ############################################################
    def UseAutoImplicitSend(self):
        return True

    ############################################################
    ############################################################
    def SehHandleFunc(self, errorcode):
        LOG_E("[PTSAutomation] {0} SEH ExceptionCode: {1:s}".format(self.tester_name, hex(errorcode)))

        if (self.pts_crashed_func is not None):
            self.pts_crashed_func(errorcode)

        self.ets_handler.onTestcaseAbort()

        LOG_D("[PTSAutomation] Wait for 3 sec to terminate gracefully...")
        time.sleep(3)

    ############################################################
    ############################################################
    def setSEHCallback(self, callback):
        self.pts_crashed_func = callback

    ############################################################
    ############################################################
    def DongleMsg(self, msg_str):
        """msg = (ctypes.c_char_p(msg_str).value).decode("utf-8")
        LOG_D("[PTSAutomation] DongleMsg - " + msg)

        global sniffer_ready
        if SNIFFER_READY in msg:
            sniffer_ready = True"""
        return True

    ############################################################
    ############################################################
    def DeviceSearchMsg(self, addr_str, name_str, cod_str):
        """addr = (ctypes.c_char_p(addr_str).value).decode("utf-8")
        name = (ctypes.c_char_p(name_str).value).decode("utf-8")
        cod = (ctypes.c_char_p(cod_str).value).decode("utf-8")
        global devices
        devices.append("Device address = {0:s} name = {1:s} cod = {2:s}".format(addr, name, cod))"""
        return True

    ############################################################
    ############################################################
    def Log(self, log_time_str, log_descr_str, log_msg_str, log_type, project):
        log_time  = (ctypes.c_char_p(log_time_str).value).decode("utf-8")
        log_descr = (ctypes.c_char_p(log_descr_str).value).decode("utf-8")
        log_msg_body   = (ctypes.c_char_p(log_msg_str).value).decode("utf-8")
        log_msg   = log_descr + log_msg_body

        # send log to ets_handler
        if os.environ.get("DEBUG") != None:
            # Set environment variable DEBUG to get log in console output
            LOG_I("[PTSAutomation][LOG] {0} {1}".format(self.tester_name, log_msg))

        is_testcase_completed = False
        is_device_reset = False

        # 'DEVICECTL' indicates dongle cold reset because of malfunctional state
        if log_msg_body.startswith('DEVICECTL'):
            LOG_I("[PTS Dongle][{0}] - COLD RESET".format(self.tester_name))
            is_device_reset = True

        if ctypes.c_int(log_type).value == LOG_TYPE_FINAL_VERDICT:
            is_testcase_completed = True

        if is_testcase_completed or is_device_reset:
            keep_log_files = True

            # initial values for
            test_result   = RESULT_INCONC
            test_result_s = "INCONC"
            indx = log_msg.find(VERDICT)
            if indx == 0 or is_device_reset:
                test_result   = RESULT_INCOMP
                test_result_s = "INCOMP"
                if RESULT_INCONC in log_msg:
                    test_result   = RESULT_INCONC
                    test_result_s = "INCONC"
                elif RESULT_FAIL in log_msg:
                    test_result   = RESULT_FAIL
                    test_result_s = "FAIL"
                elif RESULT_PASS in log_msg:
                    test_result   = RESULT_PASS
                    test_result_s = "PASS"

                    # do not store log from 'PASS' testcase
                    keep_log_files = False
                elif RESULT_NONE in log_msg:
                    test_result   = RESULT_NONE
                    test_result_s = "NONE"

                # send log to ets_handler
                self.ets_handler.onFinalVerdictReceive(test_result)

                # done!
                self.ets.TestCaseFinishedEx.restype = c_bool
                self.ets.TestCaseFinishedEx.argtypes = [c_char_p, c_char_p]
                res = self.ets.TestCaseFinishedEx(self.tc_name.encode('utf-8'), \
                                                    self.ets_name.encode('utf-8'))

                ts = time.time()
                cur_datetime = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%H_%M_%S')

                # store log files to upload to blob storage
                logfiles_to_store = {}

                # store debug log
                if keep_log_files:
                    logfiles_to_store[os.path.basename(self.tc_log_path)] = self.tc_log_path

                    debug_log_path = self.workspace_dir + '\\logfiles'
                    for log_file in os.listdir(debug_log_path):
                        new_log_file = self.tc_name.replace("/", "_")
                        new_log_file = test_result_s + '-' + new_log_file + '_' + cur_datetime + '_' + basename(log_file)
                        shutil.copy(debug_log_path + '\\' + log_file, self.workspace_dir + '\\' + new_log_file)

                        logfiles_to_store[log_file] = self.workspace_dir + '\\' + new_log_file
                # delete runtime-log from logger
                else:
                    pass

                # state changed
                self.callETSStateSubscriber(self.tc_name, test_result_s, logfiles_to_store)

                # case is done
                self.tc_name = ''

                # if dongle reset happened
                if is_device_reset:
                    if self.dongle_legacy_mode is not True:
                        time.sleep(10)
                        self.__initPTSDongle()
                    else:
                        sys.exit(-1) # legacy doesn't support disconnect and reconnect. just exit

        return True

    ############################################################
    ############################################################
    def ImplicitSend(self, description, style):
        descr_str = (ctypes.c_char_p(description).value).decode("utf-8")
        descr_str = descr_str.strip()
        indx = descr_str.find('}')

        if indx != -1:
            res = self.ets_handler.onMMIReceive(style, descr_str, indx)
            return res
        else:
            LOG_E("[PTSAutomation]{0:s} invalid mmi description, {1:s}".format(self.tester_name, descr_str))
            # Sends OK to keep proceed regardless invalid MMI
            time.sleep(3)
            return b'OK'

    ############################################################
    ############################################################
    def ptsAutoName(self):
        return self.tester_name

    ############################################################
    def getDeviceHandler(self):
        return self.ets_handler.getDeviceHandler()

    ############################################################
    def healthCheck(self):
        return self.ets_handler.healthCheck()

    def wait(self):
        while self.tc_name != '':
            time.sleep(0.1)

    def runTestCase(self, tc_to_run, startingMsg = ''):
        self._tc_started_time = time.time()
        self._tc_current = tc_to_run

        self.setIcsParameters(self.ets_handler.getICSSettings(tc_to_run))
        self.setIxitParameters(self.ets_handler.getIXITSettings(tc_to_run))
        self.startTestcase(tc_to_run, startingMsg)

        self.wait()

class ETSHandler:
    MMI_USER_ACCEPT_OK_CANCEL = 0x11041
    MMI_USER_ACCEPT_YES_NO = 0x11044
    MMI_USER_ACCEPT_EDIT_OK_CANCEL = 0x12040

    def _preinit(self):
        pass

    def _init(self, param):
        pass

    def _post(self):
        pass

    def _abort(self):
        pass

    def _verdict(self, param):
        pass

    def _wait_and_check_pass(self):
        pass

    def _postmmi(self, mmi_function, params):
        pass

    ############################################################
    def __init__(self, tester = None):
        self._log       = logging.getLogger("Logger")
        self._iut_address = '000000000000'
        self.automation = None

        self._commonHdlr = None
        self._etsHandler = None

        self._testcase = None

        self.lock   = threading.Lock()
        if (tester is not None) and (tester != ''):
            self.tester_name = '[' + tester + ']'
        else:
            self.tester_name = ''

        self.pre_inited = False

    ############################################################
    ############################################################
    def onBeforeTestcaseStart(self, testcaseName):
        self._testcase = testcaseName
        if not self.pre_inited:
            self.pre_inited = True
            self._preinit()

        params = {'tc': testcaseName, 'iutAddr': self._iut_address, 'ptsAddr': self.automation.getPTSBDAddr(), 'etsName':self.automation.getETSName()}
        self._init(params)

    ############################################################
    ############################################################
    def onTestcaseStop(self):
        # execute the init procedure
        self._post()

    def onTestcaseAbort(self):
        self._abort()

    ############################################################
    ############################################################
    def onFinalVerdictReceive(self, verdict):
        msg = "[etsHandler]{0} [VERDICT] {1}:{2}".format(self.tester_name, self._testcase, verdict)
        if verdict == 'PASS':
            LOG_PASS(msg)
        else:
            LOG_FAIL(msg)

        self._verdict(verdict)

    ############################################################
    ############################################################
    def onLogReceive(self, logString):
        LOG_D("[etsHandler][LOG] " + logString)

    ############################################################
    ############################################################
    def onMMIReceive(self, style, descr_str, indx):
        implicitSendInfo = descr_str[1:(indx)]
        implicitSendDesc = descr_str[(indx + 1):]

        items                    = implicitSendInfo.split(',')
        implicitSendInfoID       = items[0].strip()
        implicitSendInfoTestCase = items[1].strip() # remove front or end white space
        implicitSendInfoProject  = items[2].strip()

        mmiString  = "{0:s} #################################### MMI #######################################\n".format(self.tester_name)
        mmiString += "{0:s}     project_name = {1:s}\n".format(self.tester_name, implicitSendInfoProject)
        mmiString += "{0:s}     id           = {1:s}\n".format(self.tester_name, implicitSendInfoID)
        mmiString += "{0:s}     test_case    = {1:s}\n".format(self.tester_name, implicitSendInfoTestCase)
        mmiString += "{0:s}     description  = {1:s}\n".format(self.tester_name, implicitSendDesc)
        mmiString += "{0:s}     style        = {1:#X}\n".format(self.tester_name, ctypes.c_int(style).value)
        mmiString += "{0:s} #################################################################################".format(self.tester_name)
        mmiString.strip()

        LOG_I("[etsHandler][MMI]\n" + self.tester_name + mmiString)

        mmi_function = 'mmi_' + implicitSendInfoID
        mmi_handler  = None

        # Does ETS-specifc handler contains handler function?
        if hasattr(self, mmi_function):
            mmi_handler = getattr(self, mmi_function)

        # Execute MMI Handler
        res = b'OK'
        params = {'desc': implicitSendDesc, 'tc': implicitSendInfoTestCase, 'iutAddr': self._iut_address, 'ptsAddr': self.automation.getPTSBDAddr(), 'style':ctypes.c_int(style).value}
        if mmi_handler is not None:
            res = mmi_handler(params)
        else:
            style = params['style']
            LOG_W("[etsHandler]{0:s} mmi_handler {2:s} for id {1:s} not found!\n".format(self.tester_name, implicitSendInfoID, mmi_function))
            if (self.MMI_USER_ACCEPT_OK_CANCEL == style
                or self.MMI_USER_ACCEPT_YES_NO == style):
                #give a delay of 3 secs before sending the OK response
                time.sleep(3)

        self._postmmi(mmi_function, params)

        return res

    ############################################################
    def WaitAndcheckPass(self, testSuccessMyself=True):
        # If a profile handler has 2 lower testers, it needs to support WaitAndcheckPass method for synchronization.
        retval = testSuccessMyself
        return retval

    ############################################################
    def getDeviceHandler(self):
        return self._deviceHandler

    ############################################################
    def getETSHandler(self):
        return self._etsHandler

    ############################################################
    def healthCheck(self):
        return True

    def getICSSettings(self, tc_to_run):
        return {}

    def getIXITSettings(self, tc_to_run):
        return {}