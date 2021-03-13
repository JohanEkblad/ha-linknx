"""Class for linknx REST integration."""
import logging
import socket
import time
import xml.etree.ElementTree as ET
import re

class Linknx:
    """Integration against Linknx xml server"""
    linknx_host="0.0.0.0"
    linknx_port=1028
    linknx_write_success="<write status='success'/>"
    linknx_read_first="<read status='success'>" # First part
    linknx_read_second="</read>\n\4"

    def __init__(self, host, port=1028):
        self.linknx_host = host
        self.linknx_port = port

    # name from linknx, for example: light_garage
    # value in linknx on/off to turn lights on and off
    def write(self, name, value):
        try:
            s = socket.socket()
            s.connect((self.linknx_host,self.linknx_port))
            s.send(bytes("<write><object id='"+name+"' value='"+value+"'/></write>\n\4","utf-8"))
            res = s.recv(128).decode("utf-8")
            s.close()
        except:
            return False
        else:
            if res[0:len(self.linknx_write_success)] == self.linknx_write_success:
                return True
            else:
                return False

    # read status from linknx name
    def read(self, name):
        try:
            s = socket.socket()
            s.connect((self.linknx_host,self.linknx_port))
            s.send(bytes("<read><object id='"+name+"'/></read>\n\4","utf-8"))
            res = s.recv(128).decode("utf-8")
            s.close()
        except:
            return ""
        else:
            if res[0:len(self.linknx_read_first)] == self.linknx_read_first:
                rest=res[len(self.linknx_read_first):]
                res=rest[0:len(rest)-len(self.linknx_read_second)]
                return res
            else:
                return ""

    def __extract_ids(self, data, filter):
        res=[]
        root = ET.ElementTree(ET.fromstring('<root>'+data+'</root>'))
        for read in root.findall('read'):
            for config in read.findall('config'):
                for objects in config.findall('objects'):
                    for o in objects.findall('object'):
                        attributes = o.attrib
                        res.append({"id":attributes.get('id'), "name":o.text})
        if filter == '':
            return res
        else:
            p=re.compile(filter)
            ret=[]
            for theEntry in res:
                if p.match(theEntry["id"]):
                    ret.append(theEntry)
            return ret

    def readAll(self, filter=''):
        try:
            s = socket.socket()
            s.connect((self.linknx_host,self.linknx_port))
            s.sendall(bytes("<read><config/></read>\n\4","utf-8"))
            res = ''
            while True:
                data = s.recv(1024)
                if data:
                    datastr=data.decode("utf-8")
                    if datastr[len(datastr)-1] == '\4':
                        res += datastr[0:len(datastr)-1]
                        break;
                    else:
                        res += datastr
                else:
                    break
            s.close()
        except:
            return []
        else:
            return self.__extract_ids(res, filter)

