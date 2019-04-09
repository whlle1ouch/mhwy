import re


def match_reply(reply_list,msg):
    for r in reply_list:
        reg = re.compile(r[0])
        mat = re.match(reg,msg)
        if mat:
            return r[1]
    return reply_list[0][1]





