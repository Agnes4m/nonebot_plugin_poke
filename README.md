<!-- markdownlint-disable MD026 MD031 MD033 MD036 MD041 MD046 -->
<div align="center">
  <img src="https://raw.githubusercontent.com/Agnes4m/nonebot_plugin_l4d2_server/main/image/logo.png" width="180" height="180"  alt="AgnesDigitalLogo">
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_poke（仅支持onebotv11）

_✨Nonebot & 自定义戳戳群聊事件✨_

<a href="https://github.com/Agnes4m/nonebot_plugin_poke/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/Agnes4m/nonebot_plugin_poke" alt="stars">
</a>
<a href="https://github.com/Agnes4m/nonebot_plugin_poke/issues">
        <img alt="GitHub issues" src="https://img.shields.io/github/issues/Agnes4m/nonebot_plugin_poke" alt="issues">
</a>
<a href="https://jq.qq.com/?_wv=1027&k=HdjoCcAe">
        <img src="https://img.shields.io/badge/QQ%E7%BE%A4-399365126-orange?style=flat-square" alt="QQ Chat Group">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_poke">
        <img src="https://img.shields.io/pypi/v/nonebot_plugin_poke.svg" alt="pypi">
</a>
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
    <img src="https://img.shields.io/badge/nonebot-2.0.0-red.svg" alt="NoneBot">

</div>

## 注意事项

**如果使用napcat，请将版本更新到1.6.6或者以上，否则这个功能用不了**

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
再手动添加`nonebot_plugin_poke`到bot文件下`pyproject.toml`文件中

## env配置项:

    # 在完全不写的情况下，效果是戳戳后反戳戳
    # 机器人名称
    bot_nickname: str = '宁宁'
    # 是否回复图片
    poke_send_pic: bool = False
    # 是否回复戳戳
    poke_send_poke: bool = True
    # 是否回复文字
    poke_send_text: bool = False
    # 是否回复音频
    poke_send_acc: bool = False

如果不知道以下配置，默认就可以，只修改上面部分

    # poke文件夹位置
    poke_path:Path = Path('data/poke')
    # 是否开启黑名单模式（否则是白名单）
    poke_black: bool = True
    # 黑名单屏蔽群组
    poke_ban_group:List[str] = []
    # 白名单允许群组
    poke_allow_group:List[str] = []
    # 戳戳优先级
    poke_priority:int = 1
    # 是否阻断其他指令
    poke_block:bool = True

## 指令

群里双击bot头像，会依次按照配置文件，逐步检查回复

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

- 如果发不出语音，请手动安装ffmpeg
- 当语音，与图或文都为True的时候，则随机发送一种，防止刷屏刷到风控

## 参考

- [智障回复](https://github.com/Special-Week/nonebot_plugin_smart_reply)
