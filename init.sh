#!/bin/bash
#fonts color
yellow(){
    echo -e "\033[33m\033[01m$1\033[0m"
}
green(){
    echo -e "\033[32m\033[01m$1\033[0m"
}
red(){
    echo -e "\033[31m\033[01m$1\033[0m"
}
git clone https://github.com/Kizureina/nonebot_plugin_ytbLivePusher
green "源码下载完成"
cd nonebot_plugin_ytbLivePusher && python3 _dbSetup.py && mv *.py ../ && mv *.db ../
green "数据库初始化完成"
cd .. && rm -rf nonebot_plugin_ytbLivePusher
green "全部操作完成！"