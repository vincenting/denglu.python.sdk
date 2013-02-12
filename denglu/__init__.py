#!/usr/bin/env python
# -- coding: utf-8 --

__author__ = 'Vincent Ting'
__version__ = '1.0'

from base import DengLuBase


class Denglu(DengLuBase):
    def getAuthUrl(self, Provider, isBind=False, uid=0):
        """
        获取登陆/绑定链接 目测暂不可用-Vincent
        :param Provider: 通过Denglu.Provider p = Denglu.Provider.guess(mediaNameEn) 获取。mediaNameEn获取媒体列表中得到
        :param isBind: 是否用于绑定（非绑定则为登录）
        :param uid: 用户网站的用户ID，绑定时需要
        :return: 最终URL或者异常错误
        """
        authUrl = self.domain
        if self.providers.get(Provider, None):
            authUrl += self.providers.get(Provider)
        else:
            return {
                'errorCode': 1,
                'errorDescription': 'Please update your denglu-scripts to the latest version!'
            }
        param = ['appid={0}'.format(self.appID), 'appkey={0}'.format(self.apiKey)]
        if isBind and uid > 0:
            param.append('uid={0}'.format(uid))
        authUrl += "?{0}".format("&".join(param))
        return authUrl

    def latestComment(self, count):
        """
        最新评论
        :param count: 评论条数
        :return:
        """
        return self.callApi('latestComment', count=count)

    def getComments(self, commentid, count=50):
        """
        返回自己应用的评论列表，用于本地化保存评论数据。
        :param commentid: commentid 若指定此参数，则返回ID比commentid大的评论（即比commentid时间晚的评论），默认为0。
        :param count: 返回的记录条数，默认为50。
        :return: eg:
            {
                "postid":"1",
                "content":"我是一条评论",
                "mediaID":3,
                "createTime":"2012-04-26 12:38:14",
                "state":0,
                "commentID":38751,
                "userImage":"http://tp4.sinaimg.cn/2132511355/50/0/1",
                    "userName":"testapis",
                "mediaUserID":1224050,
                "homepage":"http://weibo.com/2132511355",
                "ip":"106.3.63.172",
                "parent":
                {
                    "postid":"1",
                    "content":"我是它的父级评论",
                    "mediaID":101,
                    "commentID":38749,
                    "userName":"水脉烟香",
                    "userEmail":"xxx@qq.com",
                    "mediaUserID":3529900,
                    "homepage":"http://www.smyx.net/",
                    "ip":"123.116.124.167"
                }
            }
        """
        return self.callApi('getComments', commentid=commentid, count=count)

    def getCommentState(self, time):
        """
        返回自己应用的评论更新状态，比如评论被删除、审核，可以同步评论状态到本地。
        :param time: 时间 单位为1小时，数字类型
        :return: 0——正常评论，1——待审，2——垃圾评论，3——回收站，4——删除
        eg:
            {"582997":0,"571330":1,"571277":2,"583028":0}
            """
        return self.callApi('getCommentState', time=time)

    def getUserInfoByToken(self, token):
        """
        根据token获取用户信息
        :param token:
        :return: eg
            {
                "mediaID":7,							// 媒体ID
                "createTime":"2011-05-20 16:44:19",		// 创建时间
                "friendsCount":0,						// 好友数
                "location":null,						// 地址
                "favouritesCount":0,					// 收藏数
                "screenName":"denglu",					// 显示姓名
                "profileImageUrl":"http://head.xiaonei.com/photos/0/0/men_main.gif",		// 个人头像
                "mediaUserID":61,						// 用户ID
                "url":null,								// 用户博客/主页地址
                "city":null,							// 城市
                "description":null,						// 个人描述
                "createdAt":"",							// 在媒体上的创建时间
                "verified":0,							// 认证标志
                "name":null,							// 友好显示名称
                "domain":null,							// 用户个性化URL
                "province":null,						// 省份
                "followersCount":0,						// 粉丝数
                "gender":1,								// 性别 1--男，0--女,2--未知
                "statusesCount":0,						// 微博/日记数
                "personID":120							// 个人ID
            }
        """
        return self.callApi('getUserInfo', token=token)

    def getMedia(self):
        """
        获取当前应用ID绑定的所有社会化媒体及其属性        
        :return: eg:
          [
                {
                    "mediaID":7,																		// ID
                    "mediaIconImageGif":"http://test.denglu.cc/images/denglu_second_icon_7.gif",		// 社会化媒体亮色Icon
                    "mediaIconImage":"http://test.denglu.cc/images/denglu_second_icon_7.png",			// 社会化媒体亮色Icon
                    "mediaNameEn":"renren",																// 社会化媒体的名称的拼音
                    "mediaIconNoImageGif":"http://test.denglu.cc/images/denglu_second_icon_no_7.gif",	// 社会化媒体灰色Icon
                    "mediaIconNoImage":"http://test.denglu.cc/images/denglu_second_icon_no_7.png",		// 社会化媒体灰色Icon
                    "mediaName":"人人网",																// 社会化媒体的名称
                    "mediaImage":"http://test.denglu.cc/images/denglu_second_7.png",					// 社会化媒体大图标
                    "shareFlag":0,																		// 是否有分享功能 0是1否
                    "apiKey":"704779c3dd474a44b612199e438ba8e2"											// 社会化媒体的应用apikey
                }
          ]
        """
        return self.callApi('getMedia')

    def getBind(self, muid, uid=None):
        """
        获得同一用户的多个社会化媒体用户信息
        :param muid: 用户网站的用户ID(可选)
        :param uid: 社会化媒体的用户ID
        :return: eq:
        [
            {'mediaUserID':100,
            'mediaID':10,
            'screenName':'张三'},
            {'mediaUserID':101,
            'mediaID':11,
            'screenName':'李四'},
            {'mediaUserID':102,
            'mediaID':12,
            'screenName':'王五'},
        ]
        """
        if not muid:
            return self.callApi('getBind', uid=uid)

        return self.callApi('getBind', muid=muid)

    def getInvite(self, muid, uid=None):
        """
        获取可以邀请的媒体用户列表
        :param muid: 用户网站的用户ID(可选)
        :param uid: 社会化媒体的用户ID
        :return: eq:
        [
            {'mediaUserID':100,
            'mediaID':10,
            'screenName':'张三'},
            {'mediaUserID':101,
            'mediaID':11,
            'screenName':'李四'},
            {'mediaUserID':102,
            'mediaID':12,
            'screenName':'王五'},
        ]
        """
        if not muid:
            return self.callApi('getInvite', uid=uid)

        return self.callApi('getInvite', muid=muid)

    def getRecommend(self, muid, uid=None):
        """
        获取可以推荐的媒体用户列表
        :param muid: 用户网站的用户ID(可选)
        :param uid: 社会化媒体的用户ID
        :return: eq:
        [
            {'mediaUserID':100,
            'mediaID':10,
            'screenName':'张三'},
            {'mediaUserID':101,
            'mediaID':11,
            'screenName':'李四'},
            {'mediaUserID':102,
            'mediaID':12,
            'screenName':'王五'},
        ]
        """
        if not muid:
            return self.callApi('getRecommend', uid=uid)

        return self.callApi('getRecommend', muid=muid)

    def sendInvite(self, invitemuids, muid, uid=None):
        """
        发送邀请
        :param invitemuids:
        :param muid: 用户网站的用户ID(可选)
        :param uid: 社会化媒体的用户ID
        :return: eq:{"result": "1"}
        """
        if not muid:
            return self.callApi('sendInvite', uid=uid, invitemuids=invitemuids)

        return self.callApi('sendInvite', muid=muid, invitemuids=invitemuids)

    def bind(self, mediaUID, uid, uname, uemail):
        """
        用户绑定多个社会化媒体账号到已有账号上
        :param mediaUID: 社会化媒体的用户ID
        :param uid: 用户网站那边的用户ID
        :param uname: 用户网站的昵称
        :param uemail: 用户网站的邮箱
        :return: eg: {"result": "1"}
        """
        return self.callApi('bind', muid=mediaUID, uid=uid, uname=uname, uemail=uemail)

    def unbind(self, mediaUID):
        """
        用户解除绑定社会化媒体账号
        :param mediaUID: 社会化媒体的用户ID
        :return: eg: {"result": "1"}
        """
        return self.callApi('unbind', muid=mediaUID)

    def sendLoginFeed(self, mediaUserID):
        """
        发送登录的新鲜事
        :param mediaUserID: 从灯鹭获取的mediaUserID
        :return: eg: {"result": "1"}
        """
        return self.callApi('login', muid=mediaUserID)

    def share( self, mediaUserID, content, url, uid, imageurl='', videourl='', param1=''):
        """
        用户发布帖子、日志等信息时，可以把此信息分享到第三方
        :param mediaUserID:
        :param content: 分享显示的信息
        :param url: 查看信息的链接
        :param uid: 网站用户的唯一性标识ID
        :param imageurl: 图片URL
        :param videourl: 视频URL
        :param param1: 文章ID, 用于同步微博的评论抓取回来
        :return: eg: {"result": "1"}
        """
        return self.callApi('share', muid=mediaUserID, uid=uid, content=content, imageurl=imageurl, videourl=videourl,
                            param1=param1, url=url)

    def unbindAll(self, uid):
        """
        用户解除所有绑定社会化媒体账号
        :param uid: 网站用户的唯一性标识ID
        :return: eg: {"result": "1"}
        """
        return self.callApi('unbindAll', uid=uid)
