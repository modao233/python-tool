import itchat
from itchat.content import *


class auto_reply():
    def __init__(self, **kwargs):
        pass

    def run(self):
        try:
            itchat.auto_login(hotReload=True)
        except:
            itchat.auto_login(hotReload=True, enableCmdQR=True)
        itchat.run()

    # 好友
    @itchat.msg_register(TEXT, isFriendChat=True)
    def reply_friend_text(msg):
        print('微信昵称：' + itchat.search_friends(userName=msg['FromUserName'])['NickName'] + ' 备注：' + itchat.search_friends(userName=msg['FromUserName'])['RemarkName'] + ' 私发信息说：' + msg['Content'])
        content = '本微信由机器人接管，自动回复信息'
        itchat.send(content, msg['FromUserName'])

    @itchat.msg_register([PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
    
    def reply_friend_other(msg):
        print('微信昵称：' + itchat.search_friends(userName=msg['FromUserName'])['NickName'] + ' 备注：' +
                  itchat.search_friends(userName=msg['FromUserName'])['RemarkName'] + ' 私发了一条非文本信息，故不作记录')
        content = '本微信由机器人接管，自动回复信息'
        itchat.send(content, msg['FromUserName'])

    # 群聊
    @itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
    def reply_group(msg):
        # print(itchat.search_chatrooms(userName=msg['FromUserName']))
        # print(msg['FromUserName'])
        print('来自群聊：'+itchat.search_chatrooms(userName=msg['FromUserName'])['NickName']+ ' 的成员:' + msg['ActualNickName'] + ' 说：' + msg['Content'])
        if msg['isAt']:
            # content = '自动回复：艾特我干嘛'
            # itchat.send_msg(content, msg['FromUserName'])
            return '自动回复：艾特我干嘛'
        else:
            # content = ['自动回复：测试']
            # itchat.send(content, msg['FromUserName'])
            # return '自动回复：测试'
            pass

if __name__ == '__main__':
    auto_reply().run()
