#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xmpp
from hatblog.settings import JABBER_ID, JABBER_PASSWORD, JABBER_MSG_RECIPIENT

def jabber_notify(message):
	jid = xmpp.protocol.JID(JABBER_ID)
	cl = xmpp.Client(jid.getDomain(), debug=[])
	if cl.connect() == '':
		return
	if cl.auth(jid.getNode(), JABBER_PASSWORD) == None:
		return
	cl.send(xmpp.protocol.Message(JABBER_MSG_RECIPIENT, message))
	cl.disconnect()

