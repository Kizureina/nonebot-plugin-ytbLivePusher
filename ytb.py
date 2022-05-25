from email import message
from nonebot import require, get_bot
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('interval', minutes=5, id='ytb')
async def ytb_live_pusher():
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Origin': 'https://www.youtube.com',
        'Content-Type': 'application/json',
        'host': 'www.youtube.com',
    }
    bot = get_bot()
    con = sqlite3.connect("vtb.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ytb")
    obj = cur.fetchall()
    v_num = len(obj)
    for i in range(0, v_num):
        url = obj[i][1]
        r = requests.get(url + '/live')
        html = r.content.decode("utf-8")
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('link', rel="canonical")
        url0 = links[0]['href']
        push_time = obj[i][2]
        if url == url0:
            cur.execute("UPDATE ytb SET times=0 WHERE url='%s'"%url)
            con.commit()
            continue
        else:
            if push_time == 1:
                continue
            else:
                cur.execute("UPDATE ytb SET times=1 WHERE url='%s'"%url)
                con.commit()
                vid = format(url0.replace('https://www.youtube.com/watch?v=', ''))
                data = {
                    "context": {
                        "client": {
                            "hl": "zh-CN",
                            "gl": "US",
                            "remoteHost": "104.238.183.19",
                            "deviceMake": "",
                            "deviceModel": "",
                            "visitorData": "CgtvMXpSUVRfTllXVSje7L6PBg%3D%3D",
                            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0,gzip(gfe)",
                            "clientName": "WEB",
                            "clientVersion": "2.20220124.01.00",
                            "osName": "Windows",
                            "osVersion": "10.0",
                            "originalUrl": "https://www.youtube.com/watch?v=PVCEhD6zyXs",
                            "screenPixelDensity": 1,
                            "platform": "DESKTOP",
                            "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                            "configInfo": {
                                "appInstallData": "CN7svo8GELvH_RIQt8utBRCA6q0FEJjqrQUQveutBRDYvq0FEJH4_BI%3D"
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
                                "graftUrl": "https://www.youtube.com/watch?v=PVCEhD6zyXs",
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
                                "encryptedTokenJarContents": "AGDxDePLfe_Lq5NyjA1C5nhEksdINB4VL5EcmFaVNVkqUw-0KdV0PXj-PJef54WriipjpEy-gey1ewetVkOf35qV8ET_YapXqWrpXpvD0Trxq9f4Mg35UouxGk92w1gNkDmmgIbgmaUQRlaGW1uEj384"
                            }],
                            "internalExperimentFlags": []
                        },
                        "clickTracking": {
                            "clickTrackingParams": "CLkCEMyrARgAIhMI_NrTw7_M9QIVVEhMCB2ACgrN"
                        },
                        "adSignalsInfo": {
                            "params": [{
                                "key": "dt",
                                "value": "1643099758577"
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
                title = r_json["actions"][3]['updateTitleAction']['title']['runs'][0]['text']
                last_live = r_json['actions'][2]['updateDateTextAction']['dateText']['simpleText']
                img_url = str('https://i.ytimg.com/vi/'+vid+'/hqdefault_live.jpg')
                cq = "[CQ:image,file="+ img_url + ",id=40000]"
                userid = 111111111111
                try:
                    person = r_json['actions'][0]['updateViewershipAction']['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
                    if '预定发布' in last_live:
                        cur.execute("UPDATE ytb SET times=0 WHERE url='%s'"%url)
                        con.commit()
                        continue
                    else:
                        await bot.send_private_msg(user_id=userid, message=f"你推的V在404开播啦!\n直播标题：{title}\n直播链接：{url}\n{last_live}\n当前同接：{person}")
                except:
                    if '预定发布' in last_live:
                        cur.execute("UPDATE ytb SET times=0 WHERE url='%s'"%url)
                        con.commit()
                        continue
                    else:
                        await bot.send_private_msg(user_id=userid,message=cq)
                        await bot.send_private_msg(user_id=userid, message=f"你推的V在404开播啦!\n直播标题：{title}\n{last_live}")

