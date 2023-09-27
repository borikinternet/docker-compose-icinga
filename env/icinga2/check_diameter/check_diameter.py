#!/usr/bin/env python3
import argparse
import socket
import random

from pyDiameter import pyDiaMessageConst
from pyDiameter import pyDiaMessage
from pyDiameter import pyDiaAVPTypes
from pyDiameter import pyDiaAVPPath
from pyDiameter import pyDiaAVPTools
from pyDiameter import pyDiaAVPDict


def visitAVP(avp, tab=''):
  print(tab, end='')
  print('name:  ', avp.getAVPName())
  print(tab, end='')
  print('type:  ', avp.getAVPType())
  print(tab, end='')
  print('code:  ', avp.getAVPCode())
  print(tab, end='')
  print('flags: ', avp.getAVPFlags())
  print(tab, end='')
  print('len:   ', len(avp))
  value = avp.getAVPValue()
  if avp.getAVPVSFlag():
    print(tab, end='')
    print('vendor:', avp.getAVPVendor())
  if type(value) is list:
    print(tab, end='')
    print('====>')
    for sub in value:
      visitAVP(sub, tab + '    ')
    print(tab, end='')
    print('<====')
  else:
    print(tab, end='')
    print('value: ', value)
  print(tab, end='')
  print('-------')


def visitMessage(msg):
  print('len:   ', len(msg))
  print('flags: ', msg.getFlags())
  print('code:  ', msg.getCommandCode())
  print('app:   ', msg.getApplicationID())
  print('hbh:   ', msg.getHBHID())
  print('e2e:   ', msg.getE2EID())
  avps = msg.getAVPs()
  for avp in avps:
    visitAVP(avp)


class DiameterChecker:
  def __init__(self, args):
    self.init_success = False
    self.connection_socket = None

    origin_host_name = 'icinga-server.local'
    for (family, s_type, proto, canonical_name, sock_addr) in socket.getaddrinfo(args.host, args.port,
                                                                                 type=socket.SOCK_STREAM,
                                                                                 flags=socket.AI_CANONNAME):
      s = socket.socket(family=family, type=s_type, proto=proto)
      try:
        s.connect(sock_addr)
      except Exception:
        s.close()
        del s
        continue
      if len(canonical_name):
        origin_host_name = canonical_name
      self.connection_socket = s
      break

    if not self.connection_socket:
      return

    self.message = pyDiaMessage.DiaMessage()
    self.message.generateE2EID()
    self.message.generateHBHID()
    self.message.setRequestFlag()
    self.message.setCommandCode(257)
    self.message.setApplicationID(0)

    root_avp_path = pyDiaAVPPath.DiaAVPPath()
    root_avp_path.setPath('')

    origin_host_avp = pyDiaAVPTypes.DiaAVPStr()
    origin_host_avp.setAVPCode(264)
    origin_host_avp.setAVPMandatoryFlag()
    origin_host_avp.setAVPValue(origin_host_name)
    self.message.addAVPByPath(root_avp_path, origin_host_avp)

    origin_realm = pyDiaAVPTypes.DiaAVPStr()
    origin_realm.setAVPCode(296)
    origin_realm.setAVPMandatoryFlag()
    origin_realm.setAVPValue(args.realm)
    self.message.addAVPByPath(root_avp_path, origin_realm)

    host_ip_address = pyDiaAVPTypes.DiaAVPStr()
    host_ip_address.setAVPCode(257)
    host_ip_address.setAVPMandatoryFlag()
    if self.connection_socket.family == socket.AF_INET:
      (addr, port) = self.connection_socket.getsockname()
      host_ip_address.setAVPValue(pyDiaAVPTools.address_to_bytes(('ipv4', addr)))
    elif self.connection_socket.family == socket.AF_INET6:
      (addr, port, flowinfo, scope_id) = self.connection_socket.getsockname()
      host_ip_address.setAVPValue(pyDiaAVPTools.address_to_bytes(('ipv6', addr)))
    self.message.addAVPByPath(root_avp_path, host_ip_address)

    product_name = pyDiaAVPTypes.DiaAVPStr()
    product_name.setAVPCode(269)
    product_name.setAVPValue("NAGIOS-CheckDiameter-Plugin")
    self.message.addAVPByPath(root_avp_path, product_name)

    random.seed()
    self.origin_state_id = random.randrange(2 ** 32 - 1)
    origin_state_id = pyDiaAVPTypes.DiaAVPUInt32()
    origin_state_id.setAVPCode(278)
    origin_state_id.setAVPMandatoryFlag()
    origin_state_id.setAVPValue(self.origin_state_id)
    self.message.addAVPByPath(root_avp_path, origin_state_id)

    vendor_id = pyDiaAVPTypes.DiaAVPUInt32()
    vendor_id.setAVPCode(266)
    vendor_id.setAVPValue(10415)
    vendor_id.setAVPMandatoryFlag()
    self.message.addAVPByPath(root_avp_path, vendor_id)

    vendor_spec_app_id = pyDiaAVPTypes.DiaAVPGroup()
    vendor_spec_app_id.setAVPCode(260)
    vendor_spec_app_id.setAVPMandatoryFlag()
    self.message.addAVPByPath(root_avp_path, vendor_spec_app_id)

    vendor_sai_path = pyDiaAVPPath.DiaAVPPath()
    vendor_sai_path.setPath('0/260[0]')

    self.message.addAVPByPath(vendor_sai_path, vendor_id)

    auth_app_id = pyDiaAVPTypes.DiaAVPUInt32()
    auth_app_id.setAVPCode(258)
    auth_app_id.setAVPMandatoryFlag()
    auth_app_id.setAVPValue(16777216)
    self.message.addAVPByPath(vendor_sai_path, auth_app_id)

    self.init_success = True

  def __del__(self):
    if self.connection_socket:
      self.connection_socket.shutdown(socket.SHUT_RDWR)
      self.connection_socket.close()

  def sendCER(self) -> bool:
    try:
      self.connection_socket.sendall(self.message.encode())
    except Exception:
      return False
    return True

  def recvCEA(self) -> (int, pyDiaMessage.DiaMessage):
    try:
      buf = b''
      buf_len = 0
      while buf_len < pyDiaMessageConst.MSG_HEADER_BUFF_LEN:
        buf += self.connection_socket.recv(pyDiaMessageConst.MSG_HEADER_BUFF_LEN - buf_len)
        buf_len = len(buf)
      msg_len = pyDiaMessage.DiaMessage.decodeUIntValue(buf[1:])
      while buf_len < msg_len:
        buf += self.connection_socket.recv(msg_len - buf_len)
        buf_len = len(buf)
    except Exception:
      return -2, None  # exception while reading from socket
    message = pyDiaMessage.DiaMessage()
    message.decode(buf)
    if not (not message.getRequestFlag() and message.getCommandCode() == 257 and message.getApplicationID() == 0):
      return -3, message  # received unknown (not CEA) incoming message
    avps = message.getAVPs()
    for avp in avps:
      if avp.getAVPCode() == 268 and avp.getAVPVendor() == 0:
        return avp.getAVPValue()
    return -1, message  # no Result-Code AVP found in answer

  def run(self) -> int:
    if not self.connection_socket:
      print("CRITICAL: Can't connect to remote peer")
      return 2
    if self.init_success:
      if not self.sendCER():
        print("CRITICAL: Connection to peer was broken while sending request")
        return 2
      (res, msg) = self.recvCEA()
      dia_dict = pyDiaAVPDict.DiaAVPDict()
      if res == 2001:
        print("OK: CEA with Result-Code {res} successfully received".format(res=res))
        return 0
      elif 2000 <= res < 3000:
        print("WARNING: CEA with Result-Code {res} received".format(res=res))
        return 1
      elif res > 0:
        print("CRITICAL: CEA with Result-Code {res} received".format(res=res))
        return 2
      else:
        print("UNKNOWN: No CEA received, {res} code returned while trying to read answer".format(res=res))
        if msg:
          visitMessage(msg)
        return 3
    print("UNKNOWN: Can't process check")
    return 3  # return UNKNOWN state


if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="check_diameter",
                                   description="Nagios plugin to check DIAMETER peer is alive. "
                                               "Can be used only with TCP connection")
  parser.add_argument('-H', '--host', type=str, default='127.0.0.1', dest='host')
  parser.add_argument('-p', '--port', type=int, default=3868, dest='port')
  parser.add_argument('-r', '--realm', type=str, default='monitoring.local', dest='realm')

  exit(code=DiameterChecker(parser.parse_args()).run())
