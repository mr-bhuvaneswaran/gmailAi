from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import dateutil.parser as parser
import mysql.connector

#DATABASE CONNECTION
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="gmail"
)
cursor = db.cursor()


SCOPES = 'https://www.googleapis.com/auth/gmail.modify' #SCOPE FOR MESSAGES
store = file.Storage('storage.json') #AUTO GENERATED FILE FOR SESSION
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me' #DEFAULT USER SELF

#Replace the 'list:<receiver> Or q=<any query like from:**@gmail.com>'
msgs = GMAIL.users().messages().list(userId='me',q='list:mr.bhuvaneswaran@gmail.com',maxResults=5).execute()

mssg_list = msgs['messages']

final = []

for mssg in mssg_list:
    record = []
    m_id = mssg['id']
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
    payld = message['payload']
    headr = payld['headers']

    record.append(m_id)

    for head in headr:
        if head['name'] == 'Date':
            msg_date = head['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            record.append(str(m_date))
    for head in headr:
        if head['name'] == 'From':
            msg_from = head['value']
            record.append(msg_from)
    for head in headr:
        if head['name'] == 'Delivered-To':
            msg_to = head['value']
            record.append(msg_to)
    for head in headr:
        if head['name'] == 'Subject':
            msg_subject = head['value']
            record.append(msg_subject)

    final.append(tuple(record)) # A tupple list for writting in database

sql = "INSERT INTO email (message_id, recevied, sender, receiver, subject) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(sql, final)

db.commit()
