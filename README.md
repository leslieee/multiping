# MultiPing
Network packet loss analysis script

同时ping多个服务器并统计丢包率, 观察线路的国际出口情况, 便于ss/ssr线路选择
# 效果图
> Windows
![](show1.png)
> Mac
![](show2.png)
# 运营环境
> pyhton2.7.*
# 支持平台
Mac, Linux, Windows
# 启动
mac/linux
> python multiping.py

windows

双击执行multiping.py(有py环境)或者multiping.exe(没有安装python)
# 停止
ctrl + z, 或者直接关掉terminal
# 加入新的ip
方法1 在multiping.py的ip列表中加入, 注意格式 'your ip',
>ip = [  '101.254.176.225', '222.186.56.1', '103.236.136.1', ...

方法2 脚本第一次运行会在当前目录生成ip.txt文件, 直接在文件中添加ip, 保存后重启脚本

(注意格式为utf-8)
# 使用事项

1.丢包情况直接看lost(丢包的包)值就可以了

2.sent(已发送的包)值不一致是因为高丢包导致每次超时(1秒)才会结束, 发包的总数量就少了

3.delay不显示表示上一次ping失败了

4.ip归属地是火猫的免费接口
