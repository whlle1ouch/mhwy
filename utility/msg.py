

def packMsg(sender , time , message , seq="{%mh%}" , seq_msg="{%mh-wx%}"):
    msg_list = [sender,time,message]
    msg_pack = seq.join(msg_list)
    msg_pack += seq_msg
    return msg_pack

def dePackMsgList(packMsg , seq_msg="{%mh-wx%}"):
    msg_list = packMsg.split(seq_msg)
    return msg_list[:-1]

def dePackMsg(packMsg , seq="{%mh%}"):
    msg = packMsg.split(seq)
    sender = msg[0]
    time = msg[1]
    message = msg[2]
    return sender,time,message

def parseMsg(sender,time,message):
    return sender + "   " + "(" + time + ")" + ":\n" + message + "\n"


