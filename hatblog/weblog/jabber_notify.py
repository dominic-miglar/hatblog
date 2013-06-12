#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xmpp
from hatblog.settings import JABBER_ID, JABBER_PASSWORD, JABBER_MSG_RECIPIENT

def jabber_notify(message):
	jid = xmpp.protocol.JID(JABBER_ID)
	#cl = xmpp.Client(jid.getDomain(), debug=[])
	cl = xmpp.Client(jid.getDomain())
	cl.connect()
	cl.auth(jid.getNode(), JABBER_PASSWORD)
	cl.send(xmpp.protocol.Message('firehat@w1r3.net', message))
	cl.disconnect()
