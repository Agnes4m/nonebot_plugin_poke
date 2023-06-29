from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import  on_notice,on_command
from nonebot.adapters.onebot.v11 import PokeNotifyEvent,MessageSegment, Message,GroupMessageEvent

import random
from typing import List
from pathlib import Path

from .config import config
from .utils import *

__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="戳一戳事件",
    description='自定义戳一戳事件',
    usage='戳就完事了',
    type="application",
    homepage="https://github.com/Agnes4m/nonebot_plugin_poke",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)
poke_ = on_notice(rule=to_me(), block=False,rlue=poke_rule)



@poke_.handle()
async def _(event: PokeNotifyEvent,matcher:Matcher):
    await poke_send(event,matcher)
    await acc_send(matcher)
    
