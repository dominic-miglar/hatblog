#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xmpp
#from hatblog.settings import JABBER_ID, JABBER_PASSWORD, JABBER_MSG_RECIPIENT

JABBER_ID = 'hatblog@w1r3.net'
JABBER_PASSWORD = 'hat.blog@work.31337'
JABBER_MSG_RECIPIENT = 'firehat@w1r3.net'


def jabber_notify(message):
	jid = xmpp.protocol.JID(JABBER_ID)
	cl = xmpp.Client(jid.getDomain(), debug=[])
	cl.connect()
	cl.auth(jid.getNode(), JABBER_PASSWORD, 'hatblog')
	cl.send(xmpp.protocol.Message('firehat@w1r3.net', message))
	cl.disconnect()
