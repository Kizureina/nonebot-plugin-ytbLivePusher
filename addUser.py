from nonebot import on_command
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
# from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import State
import sqlite3
adduser = on_command("add_user", aliases={"adduser","添加用户"}, priority=5, rule=to_me())

@adduser.handle()
async def add_user(bot: Bot, event: Event, state: T_State = State()):
        con = sqlite3.connect('vtb.db')
        cur = con.cursor()
        m = str(event.get_plaintext())
        message = m.replace("adduser ","")
        try:
            qqid = int(message)
        except:
            await adduser.send("格式错误!请输入Q群号")
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        for i in range(0,len(data)):
            if data[i][1] == qqid:
                await adduser.send("已在推送列表，无需重复添加哦")
                break
            else:
                num = data[0][0] - 1
                cur.execute('INSERT INTO users VALUES(?,?)', (num,qqid))
                con.commit()
                cur.close()
                con.close()
                await adduser.send(Message(str(qqid))+"已添加至推送列表🥰")
