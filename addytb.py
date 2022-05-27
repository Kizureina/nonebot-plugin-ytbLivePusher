from nonebot import on_command
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
# from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import State
import sqlite3
import requests
addytb = on_command("addytb", aliases={"addytb", "添加推送ytb"}, priority=5, rule=to_me())
@addytb.handle()
async def add_ytb_pusher(bot: Bot, event: Event, state: T_State = State()):
    con = sqlite3.connect('vtb.db')
    cur = con.cursor()
    
    m = str(event.get_message())
    url = m.replace("addytb ","")

    r = requests.get(url)
    if r.status_code == 200:    
        cur.execute("SELECT * FROM ytb")
        data = cur.fetchall()
        num = data[0][0] - 1
        cur.execute('INSERT INTO ytb VALUES(?,?,?)', (num, url, 0))
        con.commit()
        cur.close()
        con.close()
        await addytb.send("已添加至推送")
    else:
        await addytb.send("输入错误，请检查url")
