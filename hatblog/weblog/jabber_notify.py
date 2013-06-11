#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xmpp
from hatblog.settings import JABBER_USER, JABBER_PASSWORD, JABBER_SERVER, JABBER_RESOURCE, JABBER_MSG_RECIPIENT

def jabber_notify(self):

	#jid=xmpp.protocol.JID(jidparams[JABBER_ID])
	#cl=xmpp.Client(jid.getDomain(),debug=[])
	#cl.connect()
	#cl.auth(jid.getNode(),jidparams[JABBER_PASSWORD])
	#cl.send(xmpp.protocol.Message(JABBER_MSG_RECIPIENT, 'hallo'))


	#cl = Client(JABBER_SERVER)
	#if not cl.connect(server=('JABBER_SERVER',5223)):
    #    raise IOError('Can not connect to server.')
    #if not cl.auth(JABBER_USER, JABBER_PASSWORD, JABBER_RESOURCE):
   # 	raise IOError('Can not auth with server.')
   # cl.sendInitPresence()
   # cl.send(Message(JABBER_MSG_RECIPIENT, unicode('ðÒÏ×ÅÒËÁ Ó×ÑÚÉ','koi8-r')))
   # cl.disconnect()
