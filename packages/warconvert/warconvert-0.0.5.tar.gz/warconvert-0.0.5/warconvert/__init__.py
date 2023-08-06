#-*- coding : utf-8-*-

import os
import datetime
import base64, json
from har2warc.har2warc import har2warc


def http2har(http, isResponse, url):

    ret = {}
    pos = http.find('\r\n\r\n'.encode('utf-8'))
    body = http[pos + 4:]
    # body有可能是二进制文件，如图片、视频，此时会decode出错，这里采用base64的方式解决
    body = base64.encodebytes(body).decode('utf-8')
    http = http[:pos].decode('utf-8')
    http = http.split('\r\n')
    if isResponse:
        bodyLength = 0
        bodyType = ''
        http[0] = http[0].split(' ')
        ret['status'] = http[0][1]
        ret['statusText'] = http[0][2]
        ret['httpVersion'] = http[0][0]
        ret['headers'] = []
        for header in http[1:]:
            if len(header) > 0:
                header = header.split(': ')
                ret['headers'].append({
                    'name': header[0],
                    'value': header[1]
                })
                if header[0] == 'Content-Length':
                    bodyLength = header[1]
                if header[0] == 'Content-Type':
                    bodyType = header[1]
        ret['bodySize'] = bodyLength
        ret['content'] = {
            'size': bodyLength,
            'mimeType': bodyType,
            'text': body,
            'encoding': 'base64'
        }
        return ret
    else:
        http[0] = http[0].split(' ')
        ret['method'] = http[0][0]
        ret['url'] = url
        ret['httpVersion'] = http[0][2]
        ret['headers'] = []
        ret['bodySize'] = -1
        for header in http[1:]:
            if len(header) > 0:
                header = header.split(': ')
                ret['headers'].append({
                    'name': header[0],
                    'value': header[1]
                })
        return ret


def burp2har(content):
    DOMTree = content
    collection = DOMTree.documentElement

    items = collection.getElementsByTagName('item')

    harContent = {
        'log': {
            'pages': [],
            'entries': [],
            'creator': {
                'name': 'gditsec',
                'version': '1.0'
            },
            'version': '1.0'
        }
    }

    for item in items:
        startedTime = datetime.datetime.strptime(item.getElementsByTagName('time')[0].childNodes[0].data, "%a %b %d %H:%M:%S HKT %Y")
        startedTime = startedTime.strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'startedDateTime': startedTime,
            'time': 0,
            'request': {},
            'response': {},
            'cache': {
                'beforeRequest': {},
                'afterRequest': {},
                'comment': ''
            },
            'timeings': {
                'blocked': 0,
                'dns': 0,
                'connect': 0,
                'send': 0,
                'wait': 0,
                'receive': 0,
                'ssl': 0
            },
            'pageref': ''
        }
        url = item.getElementsByTagName('url')[0].childNodes[0].data
        req = item.getElementsByTagName('request')[0]
        if req.getAttribute('base64'):
            req = base64.decodestring(req
                        .childNodes[0].data.encode('utf-8'))
            req = http2har(req, False, url)
        else:
            req = http2har(req.childNodes[0].data.encode('utf-8'), False, url)
        res = item.getElementsByTagName('response')[0]
        if res.getAttribute('base64'):
            res = base64.decodestring(res
                        .childNodes[0].data.encode('utf-8'))
            res = http2har(res, True, url)
        else:
            res = http2har(res.childNodes[0].data.encode('utf-8'), True, url)
        entry['response'] = res
        entry['request'] = req
        harContent['log']['entries'].append(entry)
        harContent['log']['pages'].append({
            'startedDateTime': startedTime,
            'id': url,
            'title': url
        })
    return harContent


def burp2warc(content, outfile):
    content = burp2har(content)
    with open('tmp.har', 'a+') as har:
        har.write(json.dumps(content))
    har2warc('tmp.har', outfile)
    os.unlink('tmp.har')

