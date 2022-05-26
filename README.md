# nonebot plugin ytbLivePusher
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-picsearcher)
[![license](https://img.shields.io/github/license/synodriver/nonebot_plugin_picsearcher.svg)](https://raw.githubusercontent.com/synodriver/nonebot_plugin_picsearcher/main/LICENSE)
- 基于[nonebot2](https://github.com/nonebot/nonebot2)
## 基本功能
- 推送Youtube的开播提醒
- 支持前端添加删除Youtuber
## 开始使用
因为本插件使用了定时任务，需要先添加nonebot2的定时任务插件。

如正在使用 nb-cli 构建项目，你可以从插件市场复制安装命令或手动输入以下命令以添加`nonebot_plugin_apscheduler`

```
nb plugin install nonebot_plugin_apscheduler
```
## 配置定时任务
根据项目的 .env 文件设置，向 .env.* 或 bot.py 文件添加 `nonebot_plugin_apscheduler`的可选配置项。

在`.env`中添加

```#APSCHEDULER_CONFIG={"apscheduler.timezone": "Asia/Shanghai"}
```

在`bot.py`中添加

```#nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
```

注：`APScheduler`相关配置。修改/增加其中配置项需要确保 `prefix: apscheduler`。
