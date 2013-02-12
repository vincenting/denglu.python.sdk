#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DengLu底层方法，负责和服务器数据传输以及数据解析
"""

__author__ = 'Vincent Ting'

import httplib
import urllib
import socket
import urlparse
import hashlib
import json
import time


class DengLuBase():
    #denglu API的域名，默认http://open.denglu.cc
    #设置此属性以满足以后有做二级域名重定向需求的客户
    domain = 'http://open.denglu.cc'

    version = '1.0'
    #DENGLU Restful API的地址
    apiPath = {
        'bind': '/api/v3/bind',
        'unbind': '/api/v3/unbind',
        'login': '/api/v3/send_login_feed',
        'getUserInfo': '/api/v4/user_info',
        'share': '/api/v4/share',
        'getMedia': '/api/v3/get_media',
        'unbindAll': '/api/v3/all_unbind',
        'getBind': '/api/v3/bind_info',
        'getInvite': '/api/v3/friends',
        'getRecommend': '/api/v3/recommend_user',
        'sendInvite': '/api/v3/invite',
        # 最新评论
        'latestComment': '/api/v4/latest_comment',
        # 评论列表，用于数据本地化
        'getComments': '/api/v4/get_comment_list',
        # 评论状态列表
        'getCommentState': '/api/v4/get_change_comment_ids'
    }

    #Provider的枚举，里面包括了/transfer/[name]的地址后缀
    providers = {
        'google': '/transfer/google',
        'windowslive': '/transfer/windowslive',
        'sina': '/transfer/sina',
        'tencent': '/transfer/tencent',
        'sohu': '/transfer/sohu',
        'netease': '/transfer/netease',
        'renren': '/transfer/renren',
        'kaixin001': '/transfer/kaixin001',
        'douban': '/transfer/douban',
        'yahoo': '/transfer/yahoo',
        'qzone': '/transfer/qzone',
        'alipay': '/transfer/alipay',
        'taobao': '/transfer/taobao',
        'tianya': '/transfer/tianya',
        'alipayquick': '/transfer/alipayquick',
        'guard360': '/transfer/guard360',
        'tianyi': '/transfer/tianyi',
        'facebook': '/transfer/facebook',
        'twitter': '/transfer/twitter'
    }

    def __init__(self, appID, apiKey, charset="utf-8", signatureMethod='MD5', httpConnectionTimeout=30):
        """
        构造函数
        :param appID: 灯鹭后台分配的appID {@link http://open.denglu.cc}
        :param apiKey: 灯鹭后台分配的apiKey {@link http://open.denglu.cc}
        :param charset: 系统使用的编码类型utf-8 或gbk
        :param signatureMethod: 签名算法，暂时只支持MD5
        :param httpConnectionTimeout: 默认的HTTPConnection的超时时间
        """
        self.appID = appID
        self.apiKey = apiKey
        self.charset = charset
        self.signatureMethod = signatureMethod
        self.httpConnectionTimeout = httpConnectionTimeout
        self._setEnableSSL()

    def getApiKey(self):
        return self.apiKey

    def setApiKey(self, apiKey):
        self.apiKey = apiKey

    def getAppID(self):
        return self.appID

    def setAppID(self, appID):
        self.appID = appID

    def callApi(self, method, **request):
        """
        发送http请求并获得返回信息
        :param method: 请求的api类型
        :param request: 该请求所发送的参数
        :return: 本请求是否有返回值
        """
        apiPath = self._getApiPath(method)
        post = self._createPostBody(request)
        result = json.loads(self._makeRequest(apiPath, post))
        if self.charset.lower() == "gbk":
            result = self._charsetConvert(result, "gb2312", "utf8")
        if isinstance(result, dict) and result.get("errorCode", None):
            self._throwAPIException(result)
        return result

    def _getApiPath(self, method):
        """
        从apiPath数组里获得相应method的实际调用地址
        :param method: 对应方法
        :return: Api PATH
        """
        return "{0}{1}".format(self.domain, self.apiPath.get(method, ""))

    def _makeRequest(self, url_str, params=None):
        """
        发送HTTP请求并获得相应
        :param url_str: 请求的URL
        :param params: 提交的POST参数
        """

        if not params:
            params = {}
        url = urlparse.urlparse(url_str)
        path = "{0}{1}".format(url.path or "/", "" if not url.query else "?{0}".format(url.query))
        if self.enableSSL:
            conn = httplib.HTTPConnection(url.hostname, url.port, self.httpConnectionTimeout)
        else:
            conn = httplib.HTTPSConnection(url.hostname, url.port, self.httpConnectionTimeout)

        def _open(params, path):
            """
            发送HTTP请求
            :param params:
            :param path:
            :return:
            """
            headers = {
                "Accept": "*/*",
                "Accept-Language": "zh-cn",
                "Connection": "Close",
                "Cookie:": "",
            }
            try:
                if params:
                    params = urllib.urlencode(params)
                    if self.charset.lower() == "gbk":
                        params = self._charsetConvert(params, "gb2312", "utf8")
                    headers.update({
                        "Content-type": "application/x-www-form-urlencoded"
                    })
                    conn.request("POST", path, params, headers)
                else:
                    conn.request("GET", path, headers)
                return conn.getresponse().read() or {
                    'errorCode': 10,
                    'errorDescription': "Your website can't connect to denglu server!"
                }
            except socket.timeout:
                return False

        while True:
            result = _open(params, path)
            if not result is False:
                return result

    def _signRequest(self, request=None):
        """
        为HTTP请求加签名
        :param request: HTTP请求
        :return: 加密后的字符串
        """

        if not request:
            request = {}
        request = sorted(request.items(), key=lambda request: request[0])
        sig = "".join(["{0}={1}".format(item[0], item[1]) for item in request])
        sig += self.apiKey
        return hashlib.md5(sig).hexdigest()

    def _createPostBody(self, param=None):
        if not param:
            param = {}
        param.update({
            'timestamp' : '{0}000'.format(int(time.time())),
            'appid' : self.appID,
            'sign_type' : self.signatureMethod
        })
        param['sign'] = self._signRequest(param)
        return param

    def _charsetConvert(self, oriStr, strTo, strFrom):
        """
        编码转换
        :param oriStr: 需要转换的字符串
        :param strTo: 要转换成的编码
        :param strFrom: 字符串的初始编码
        :return:转码后的字符串
        """
        _convert = lambda x: x.decode(strFrom).encode(strTo)
        if isinstance(oriStr, dict):
            result = {}
            for item in oriStr.keys():
                result[_convert(item)] = _convert(oriStr[item])
            return result
        return _convert(oriStr)

    def _setEnableSSL(self):
        """
        检查系统是否支持SSL
        """
        self.enableSSL = True
        try:
            import ssl
        except ImportError:
            self.enableSSL = False

    def _throwAPIException(self, result):
        """
        抛出异常
        :param result:
        """
        raise DengluError(result)


class DengluError(Exception):
    def __init__(self, result):
        """
        错误类型对照表
        Code Description
        1	参数错误，请参考API文档
        2	站点不存在
        3 	时间戳有误
        4 	只支持md5签名
        5 	签名不正确
        6 	token已过期
        7 	媒体用户不存在
        8 	媒体用户已绑定其他用户
        9 	媒体用户已解绑
        10 	未知错误
        :param result:
        """
        Exception.__init__(self)
        self.result = result

    def __str__(self):
        return "Error Code: {0}".format(self.result['errorCode'])