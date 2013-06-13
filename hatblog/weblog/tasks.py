from celery.decorators import task
from hatblog.settings import JABBER_ID, JABBER_PASSWORD, JABBER_MSG_RECIPIENT
import xmpp


@task()
def jabber_notify(message):
	jid = xmpp.protocol.JID(JABBER_ID)
	cl = xmpp.Client(jid.getDomain(), debug=[])
	if cl.connect() == '':
		return
	if cl.auth(jid.getNode(), JABBER_PASSWORD) == None:
		return
	cl.send(xmpp.protocol.Message(JABBER_MSG_RECIPIENT, message))
	cl.disconnect()


