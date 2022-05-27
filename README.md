# nonebot plugin ytbLivePusher
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-picsearcher)
[![license](https://img.shields.io/github/license/synodriver/nonebot_plugin_picsearcher.svg)](https://raw.githubusercontent.com/synodriver/nonebot_plugin_picsearcher/main/LICENSE)
- 基于[nonebot2](https://github.com/nonebot/nonebot2)
## 基本功能
- 推送Youtube的开播提醒
- 支持前端添加监听直播状态的Youtuber和bot推送的QQ群
## 快速上手
因为本插件使用了定时任务，需要先添加nonebot2的定时任务插件。

如正在使用 nb-cli 构建项目，你可以从插件市场复制安装命令或手动输入以下命令以添加`nonebot_plugin_apscheduler`

```
nb plugin install nonebot_plugin_apscheduler
```
具体定时任务配置参见[官方文档](https://v2.nonebot.dev/docs/advanced/scheduler).

在bot的**插件目录/plugins**执行如下脚本
```
bash <(proxychains curl -s -L https://raw.githubusercontent.com/Kizureina/nonebot_plugin_ytbLivePusher/master/init.sh)
```
注：因为众所周知的原因，要正常运行本插件需要服务器在墙外或者配置代理。
## 开始使用
@bot+addytb+空格+Youtuber频道url 可添加推送的Youtuber。
示例：
```
@bot addytb https://www.youtube.com/channel/UC-hM6YJuNYVAmUWxeIr9FeA
```
@bot+adduser+空格+QQ群号 可添加bot推送的QQ群。
