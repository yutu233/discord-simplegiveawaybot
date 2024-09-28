# 版权所有，侵权不究

## 想怎么用就怎么用

### 预览
![指令输入](https://github.com/user-attachments/assets/26a023a5-4d33-4f68-b23a-964eaa32b2ce)
![抽奖实测](https://github.com/user-attachments/assets/561d2341-cb1b-44f0-a994-8a3af2b2003c)
![中奖私信](https://github.com/user-attachments/assets/c25dee90-3522-4422-b4d2-4a846cd5a85e)

### 食用方法

1. 声明：本文件夹只包含4个文件
    main.py: 主程序，所有代码都在里面
    requirements.txt：运行程序需要安装的库，食用方法在下文
    var.env：包含机器人的TOKEN参数，可根据需要自行修改
    README.md：本文件，介绍项目的食用方法

2. 各文件食用方法:
    main.py：主程序，在运行前请保证你的Python环境版本为3.12.2(其他版本不敢保证能正常
    运行)，且已经安装了requirements.txt中的库，如有需要，还要改变TOKEN参数
    requirements.txt：食用方法：
        1. 打开cmd(搜索框输入cmd，点击进入即可)
        2. 输入pip install -r requirements.txt，回车(确保在执行这个操作前你已经安装
        好了python环境，并且正常运行了python)
        3. 等待安装完成
    var.env: 在本文件中修改你的TOKEN参数

3. 开心地玩耍吧！

### 如果你并未事先将机器人加入群组，请看这里

### 怎么将机器人加入自己的频道呢？

1. 如果你想直接食用的话，点击这个网址：[https://discord.com/oauth2/authorize?client_id=1289247997175136256&permissions=580690316306496&integration_type=0&scope=bot]
如果你想创建一个自己的机器人，请看第二步

2. 1. 进入discord网站[https://discord.com/developers/applications]
        (你需要拥有一个discord账号)
   2. 点击applications，点击右上角的New Application
   3. 输入你创建的app名称，勾选下方协议条款，点击create
   4. 点击左侧Bot，找到Reset Token，点击，随后将重置的TOKEN复制到var.env文件中
   5. 点击左侧OAuth2，滑到下方SCOPE处，找到Bot选项并勾选
   6. 在下方出现的新选项中选择你想要的功能，一一勾选(* 推荐勾选下图的权限)
   7. 最后，复制下方的链接，在新标签页中打开，将机器人授权到自己的群组中即可

   ![权限选择](https://github.com/user-attachments/assets/000e1c38-f6b1-4b7b-84fa-a59aa4137b90)


### 频道内食用方法

1. 确保你拥有这个频道的管理员权限
2. 在输入框内输入/，选择/giveaway
3. 输入必要变量prize和duration和可选变量winners(中奖人数，默认为1)和max_participants(最大参与人数，默认无限制)
4. 按下回车，就可以开始抽奖了

### 常见问题

1. “我的Python在pip安装时报错了？”
   解答：可能是你的系统环境变量Path路径中没有pip.exe所在的路径，可以上网查找怎么添加环境变量
2. “为什么终端每次抽奖都会报错？”
   解答：你就说能不能正常运行吧，能跑就行，不要在意这么多
3. “要是不好用怎么办”
   解答：你看看我这文件的数量，如果真的能适应所有环境的话那我就真的无敌了
