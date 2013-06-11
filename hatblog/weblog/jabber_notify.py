#!/usr/bin/env python
#-*- coding:utf-8 -*-

from xmpp import Client, Message
from hatblog.settings import JABBER_USER, JABBER_PASSWORD, JABBER_SERVER, JABBER_RESOURCE, JABBER_MSG_RECIPIENT

def jabber_notify(self):
	cl = Client(JABBER_SERVER)
	if not cl.connect(server=('JABBER_SERVER',5223)):
        raise IOError('Can not connect to server.')
    if not cl.auth(JABBER_USER, JABBER_PASSWORD, JABBER_RESOURCE):
    	raise IOError('Can not auth with server.')
    cl.sendInitPresence()
    cl.send(Message(JABBER_MSG_RECIPIENT, unicode('ðÒÏ×ÅÒËÁ Ó×ÑÚÉ','koi8-r')))
    cl.disconnect()
