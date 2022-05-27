from email import message
from nonebot import require, get_bot
import requests
import os
import json
from bs4 import BeautifulSoup
import sqlite3
scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('interval', minutes = 5, id = 'ytb')
async def ytb_live_pusher():
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Origin': 'https://www.youtube.com',
        'Content-Type': 'application/json',
        'host': 'www.youtube.com',
    }
    bot = get_bot()
    if os.path.exists('vtb.db') == False:
        con = sqlite3.connect("vtb.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ytb(id INTEGER PRIMARY KEY,url TEXT,times INTEGER)")
        cur.execute('INSERT INTO ytb VALUES(?,?,?)',(124,'https://www.youtube.com/channel/UCGcD5iUDG8xiywZeeDxye-A',0))
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS users(num INTEGER PRIMARY KEY,qqid INTEGER)")
        cur.execute('INSERT INTO users VALUES(?,?)',(124,1111111111))
        con.commit()
    else:
        con = sqlite3.connect("vtb.db")
        cur = con.cursor()
    cur.execute("SELECT * FROM ytb")
    obj = cur.fetchall()
    for i in range(0, len(obj)):
        url = obj[i][1]
        r = requests.get(url + '/live')
        html = r.content.decode("utf-8")
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('link', rel="canonical")
        url0 = links[0]['href']
        push_time = obj[i][2]
        if url == url0:
            cur.execute("UPDATE ytb SET times=0 WHERE url='%s'" % url)
            con.commit()
            continue
        else:
            if push_time == 1:
                continue
            else:
                cur.execute("UPDATE ytb SET times=1 WHERE url='%s'" % url)
                con.commit()
                vid = format(url0.replace('https://www.youtube.com/watch?v=', ''))
                data = {
                    "context": {
                        "client": {
                            "hl": "zh-CN",
                            "gl": "US",
                            "remoteHost": "",
                            "deviceMake": "",
                            "deviceModel": "",
                            "visitorData": "",
                            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0,gzip(gfe)",
                            "clientName": "WEB",
                            "clientVersion": "2.20220124.01.00",
                            "osName": "Windows",
                            "osVersion": "10.0",
                            "originalUrl": "",
                            "screenPixelDensity": 1,
                            "platform": "DESKTOP",
                            "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                            "configInfo": {
                                "appInstallData": ""
                            },
                            "screenDensityFloat": 1.25,
                            "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                            "timeZone": "Asia/Shanghai",
                            "browserName": "Firefox",
                            "browserVersion": "96.0",
                            "screenWidthPoints": 1536,
                            "screenHeightPoints": 26,
                            "utcOffsetMinutes": 480,
                            "mainAppWebInfo": {
                                "graftUrl": "",
                                "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                                "isWebNativeShareAvailable": False
                            }
                        },
                        "user": {
                            "lockedSafetyMode": False
                        },
                        "request": {
                            "useSsl": True,
                            "consistencyTokenJars": [{
                                "encryptedTokenJarContents": ""
                            }],
                            "internalExperimentFlags": []
                        },
                        "clickTracking": {
                            "clickTrackingParams": ""
                        },
                        "adSignalsInfo": {
                            "params": [{
                                "key": "dt",
                                "value": ""
                            }, {
                                "key": "flash",
                                "value": "0"
                            }, {
                                "key": "frm",
                                "value": "0"
                            }, {
                                "key": "u_tz",
                                "value": "480"
                            }, {
                                "key": "u_his",
                                "value": "2"
                            }, {
                                "key": "u_h",
                                "value": "864"
                            }, {
                                "key": "u_w",
                                "value": "1536"
                            }, {
                                "key": "u_ah",
                                "value": "864"
                            }, {
                                "key": "u_aw",
                                "value": "1536"
                            }, {
                                "key": "u_cd",
                                "value": "24"
                            }, {
                                "key": "bc",
                                "value": "31"
                            }, {
                                "key": "bih",
                                "value": "26"
                            }, {
                                "key": "biw",
                                "value": "1519"
                            }, {
                                "key": "brdim",
                                "value": "-7,-7,-7,-7,1536,0,1550,878,1536,26"
                            }, {
                                "key": "vis",
                                "value": "2"
                            }, {
                                "key": "wgl",
                                "value": "true"
                            }, {
                                "key": "ca_type",
                                "value": "image"
                            }]
                        }
                    },
                    "videoId": vid
                }

                apiurl = 'https://www.youtube.com/youtubei/v1/updated_metadata?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
                r = requests.post(apiurl, headers=h, data=json.dumps(data))
                r_json = json.loads(r.text)
                name = r_json["actions"][4]['updateDescriptionAction']['description']['runs'][5]['text']
                title = r_json["actions"][3]['updateTitleAction']['title']['runs'][0]['text']
                last_live = r_json['actions'][2]['updateDateTextAction']['dateText']['simpleText']
                img_url = str('https://i.ytimg.com/vi/' + vid + '/hqdefault_live.jpg')
                cq = "[CQ:image,file=" + img_url + ",id=40000]"
                cur.execute("SELECT * FROM users")
                users = cur.fetchall()
                for i in range(len(users)):
                    group_id = users[i][1]
                    try:
                        person = r_json['actions'][0]['updateViewershipAction']['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
                        if '预定发布' in last_live:
                            cur.execute("UPDATE ytb SET times=0 WHERE url='%s'" % url)
                            con.commit()
                            continue
                        else:
                            url += "/live"
                            try:
                                await bot.send_group_msg(group_id = group_id, message=f"{name}开播啦!\n直播标题：{title}\n直播链接：{url}\n{last_live}\n当前同接：{person}\n直播封面:{cq}")
                            except:
                                pass
                    except:
                        if '预定发布' in last_live:
                            cur.execute("UPDATE ytb SET times=0 WHERE url='%s'" % url)
                            con.commit()
                            continue
                        else:
                            await bot.send_group_msg(group_id = group_id, message=f"{name}开播啦!\n直播标题：{title}\n{last_live}\n直播封面:{cq}")

