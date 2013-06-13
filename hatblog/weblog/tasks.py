from celery.decorators import task
from hatblog.settings import JABBER_ID, JABBER_PASSWORD, JABBER_MSG_RECIPIENT
from hatblog.settings import EMAIL_FROM, EMAIL_RECIPIENT
import xmpp
from django.core.mail import EmailMessage



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


def send_email(subject, text, cc=None):
	if not cc:
		email = EmailMessage(subject, text, EMAIL_FROM, [EMAIL_RECIPIENT])
	else:
		email = EmailMessage(subject, text, EMAIL_FROM, [EMAIL_RECIPIENT], headers={'Reply-To': cc})
	email.send()
	