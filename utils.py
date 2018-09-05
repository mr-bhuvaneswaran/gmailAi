
def parse_rule(rule):
    query = rule['field']
    if rule['predicate'] == "contains":
        query += " LIKE "
    elif rule['predicate'] == "not equal":
        query += " NOT LIKE "
    query += "'%" + rule['value'] + "%' "
    return query


def match_value(value):
    if value == "any":
        return "OR"
    else:
        return "AND"


def AddMsgLabels(label):
    return {'addLabelIds': [label]}


def RemoveMsgLabels(label):
    return {'removeLabelIds': [label]}
