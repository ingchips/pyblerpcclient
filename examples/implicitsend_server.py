import time
import socket
import base64

from ble_rpc_client.log import LOG_OK, LOG_PLAIN, LOG_PROG, LOG_PASS, LOG_FAIL, LOG_I, LOG_D, LOG_E, LOG_W

class Handler:
    def __init__(self, iut_handler) -> None:
        self.acc = b''
        self.iut_handler = iut_handler

    def InitImplicitSend(self) -> bool:
        self.iut_handler._preinit()
        return True

    def ImplicitStartTestCase(self, tc_name: str) -> None:
        self.iut_handler._init({'tc': tc_name})

    def ImplicitTestCaseFinished(self) -> None:
        self.iut_handler._post()

    def ImplicitSendStyle(self, mmiStyle: int, mmiText: str) -> str:
        return self.ImplicitSendStyle(mmiStyle, mmiText, '')

    def ImplicitSendStyleEx(self, mmiStyle: int, mmiText: str, bdAddr: str) -> str:
        descr_str = mmiText.strip()
        indx = descr_str.find('}')

        if indx != -1:
            res = self.onMMIReceive(mmiStyle, descr_str, indx)
            return res
        else:
            LOG_E("[ImplicitSend] invalid mmi description, {1:s}".format(descr_str))
            time.sleep(3)
            return 'OK'

    def ImplicitSendPinCode(self) -> str:
        return 'RFU'

    def ImplicitSendPinCodeEx(self, bdAddr: str) -> str:
        return 'RFU'

    def onMMIReceive(self, style, descr_str, indx):
        implicitSendInfo = descr_str[1:(indx)]
        implicitSendDesc = descr_str[(indx + 1):]

        items                    = implicitSendInfo.split(',')
        implicitSendInfoID       = items[0].strip()
        implicitSendInfoTestCase = items[1].strip() # remove front or end white space
        implicitSendInfoProject  = items[2].strip()

        mmiString  = "#################################### MMI #######################################\n"
        mmiString += "    project_name = {0:s}\n".format(implicitSendInfoProject)
        mmiString += "    id           = {0:s}\n".format(implicitSendInfoID)
        mmiString += "    test_case    = {0:s}\n".format(implicitSendInfoTestCase)
        mmiString += "    description  = {0:s}\n".format(implicitSendDesc)
        mmiString += "    style        = {0:#X}\n".format(style)
        mmiString += "#################################################################################"
        mmiString.strip()

        LOG_I("[MMI]\n" + mmiString)

        mmi_function = 'mmi_' + implicitSendInfoID
        mmi_handler  = None

        if hasattr(self.iut_handler, mmi_function):
            mmi_handler = getattr(self.iut_handler, mmi_function)

        res = b'OK'
        params = {'desc': implicitSendDesc, 'tc': implicitSendInfoTestCase, 'style': style}
        if mmi_handler is not None:
            res = mmi_handler(params)
        else:
            style = params['style']
            LOG_W("[ImplicitSend] mmi_handler {1:s} for id {0:s} not found!\n".format(implicitSendInfoID, mmi_function))
            if (self.MMI_USER_ACCEPT_OK_CANCEL == style
                or self.MMI_USER_ACCEPT_YES_NO == style):
                time.sleep(3)

        self.iut_handler._postmmi(mmi_function, params)

        return res

    def rx(self, data: bytes):
        self.acc = self.acc + data
        if not self.acc.endswith(b'\n'): return None

        command = self.acc[:-1]
        self.acc = b''

        call = base64.decodebytes(command).decode()
        param = ''
        if ':' in call:
            pos = call.index(':')
            param = call[pos + 1:]
            call = call[:pos]

        match call:
            case 'InitImplicitSend':
                return str(self.InitImplicitSend())
            case 'ImplicitStartTestCase':
                self.ImplicitStartTestCase(param)
                return ''
            case 'ImplicitTestCaseFinished':
                self.ImplicitTestCaseFinished()
                return ''
            case 'ImplicitSendStyle':
                params = param.split(',', maxsplit=1)
                return self.ImplicitSendStyle(int(params[0]), params[1])
            case 'ImplicitSendStyleEx':
                params = param.split(',', maxsplit=2)
                return self.ImplicitSendStyleEx(int(params[0]), params[2], params[1])
            case 'ImplicitSendPinCode':
                return self.ImplicitSendPinCode()
            case 'ImplicitSendPinCodeEx':
                return self.ImplicitSendPinCode(param)
            case _:
                return 'error'

def start_server(iut_handler, port: int = 9168):

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', port))
    srv.listen(1)

    handler = Handler(iut_handler)

    try:
        intentional_exit = False
        while not intentional_exit:
            LOG_PROG('Waiting for connection on {}...\n'.format(port))
            client_socket, addr = srv.accept()
            LOG_PROG('Connected by {}\n'.format(addr))
            try:
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            except AttributeError:
                pass # XXX not available on windows
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            try:
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data: break
                        response = handler.rx(data)
                        if response is None: continue

                        if isinstance(response, str):
                            response = response.encode()
                        if not response.endswith(b'\n'):
                            response = response + b'\n'

                        client_socket.send(response)
                    except socket.error as msg:
                        LOG_E('ERROR: {}\n'.format(msg))
                        break
            except KeyboardInterrupt:
                intentional_exit = True
                raise
            except socket.error as msg:
                LOG_E('ERROR: {}\n'.format(msg))
            finally:
                LOG_I('Disconnected\n')
                client_socket.close()

    except KeyboardInterrupt:
        pass