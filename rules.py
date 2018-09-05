from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import json
import mysql.connector
from utils import parse_rule, match_value, RemoveMsgLabels, AddMsgLabels


# For performing the actions
def AlterLabel(service, message_ids, label):
    for msg_id in message_ids:
        msg_id = msg_id[0]
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                    body=label).execute()
    print("LABEL MODIFIED SUCCESSFULLY")


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="gmail"
)

cursor = db.cursor()

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'

# Parsing Json file
with open('rules.json') as f:
    rule_json = json.load(f)

# performing query building and actions specified in json

for unit_rule in rule_json:
    q_condition = ""
    match = match_value(unit_rule['match'])
    l_len = len(unit_rule['rules']) - 1
    for rule in unit_rule['rules']:
        q_condition += parse_rule(rule)
        if rule != unit_rule['rules'][l_len]:
            q_condition += match + " "
    query = "select message_id from email where %s;" % q_condition
    cursor.execute(query)
    result = cursor.fetchall()
    if unit_rule['label'] == "ARCHIVED":
        AlterLabel(GMAIL, result, RemoveMsgLabels("INBOX"))
    elif unit_rule['label'] == "READ":
        AlterLabel(GMAIL,result, RemoveMsgLabels("UNREAD"))
    elif unit_rule['label'] == "UNREAD":
        AlterLabel(GMAIL, result, AddMsgLabels("UNREAD"))
    else:
        AlterLabel(GMAIL, result, AddMsgLabels(unit_rule['label']))
