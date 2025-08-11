<!-- markdownlint-disable MD026 MD031 MD033 MD036 MD041 MD046 -->
<div align="center">
  <img src="https://raw.githubusercontent.com/Agnes4m/nonebot_plugin_l4d2_server/main/image/logo.png" width="180" height="180"  alt="AgnesDigitalLogo">
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_poke（仅支持 onebotv11）

_✨Nonebot & 自定义戳戳群聊事件 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue?logo=python&logoColor=edb641" alt="python">
<a href ="LICENSE">
<img src="https://img.shields.io/github/license/Agnes4m/nonebot_plugin_poke" alt="pokelogo">
<img src="https://img.shields.io/badge/nonebot-2.1.0+-red.svg" alt="NoneBot">
<a href="https://pypi.python.org/pypi/nonebot_plugin_l4d2_server">

<a href="https://pypi.python.org/pypi/nonebot_plugin_poke">
        <img src="https://img.shields.io/pypi/v/nonebot_plugin_poke.svg" alt="pypi">
</a>
</br>
<a href="https://github.com/astral-sh/ruff">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/psf/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=edb641" alt="black">
</a>
<img src="https://img.shields.io/badge/alconna-0.58.3+-red.svg" alt="NoneBot">

<a href="https://github.com/Agnes4m/nonebot_plugin_poke/issues">
        <img alt="GitHub issues" src="https://img.shields.io/github/issues/Agnes4m/nonebot_plugin_poke" alt="issues">
</a>
</div>

## 注意事项

**如果使用 napcat，请将版本更新到 1.6.6 或者以上，否则这个功能用不了**

**如果使用非gocq，则暂时无法使用反戳戳的回复**

## 安装

方法一 （推荐）：

```bash
nb plugin install nonebot_plugin_poke
```

方法二：

```bash
poetry add nonebot_plugin_poke
pdm add nonebot_plugin_poke
```

方法三：

```bash
pip install nonebot_plugin_poke
```

再手动添加`nonebot_plugin_poke`到 bot 文件下`pyproject.toml`文件中

## env 配置项:

    # 在完全不写的情况下，效果是戳戳后回复文字
    # 机器人名称
    bot_nickname = '宁宁'
    # 是否回复图片
    poke_send_pic = False
    # 是否回复戳戳 (接口失效)
    # poke_send_poke = False
    # 是否回复文字
    poke_send_text = True
    # 是否回复音频
    poke_send_acc = False

如果不知道以下配置，默认就可以，只修改上面部分

    # poke文件夹位置
    poke_path = 'data/poke'
    # 是否开启黑名单模式（否则是白名单）
    poke_black = True
    # 黑名单屏蔽群组
    poke_ban_group = []
    # 白名单允许群组
    poke_allow_group = []
    # 戳戳优先级
    poke_priority = 1
    # 是否阻断其他指令
    poke_block = True

## 指令

群里双击 bot 头像，会依次按照配置文件，逐步检查回复

## 数据结构

```txt
举例：
└── data
    └── poke
        ├── poke.txt        # 回复文字
        ├── pic             # 回复图片
            ├── 1.png
            ├── 2.jpg
            ├── 3.jpeg
            └── ...
        └── acc             # 回复音频
            ├── 1.acc
            ├── 2.mp3
            └── ...
...
```

## 其他

- 如果发不出语音，请手动安装 ffmpeg, deb 类系统请使用`sudo apt install ffmpeg`，rpm 类系统请使用`sudo yum install ffmpeg`

- 当语音，与图或文都为 True 的时候，则随机发送一种，防止刷屏刷到风控

## 参考

- [智障回复](https://github.com/Special-Week/nonebot_plugin_smart_reply)
