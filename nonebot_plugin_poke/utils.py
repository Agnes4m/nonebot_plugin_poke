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


async def acc_send(matcher:Matcher):
    """音乐部分"""
    if not config.poke_send_acc:
        return
    else:
        poke_file_path = config.poke_path
        poke_acc_list = poke_file_path.joinpath('acc').iterdir()
        acc_file_list:List[str] = []
        for acc_file in poke_acc_list:
            if acc_file.is_file() and acc_file.suffix.lower() in [".wav",".mp3",".acc"]:
                acc_file_list.append(str(acc_file))
        send_acc = random.choice(acc_file_list)
        await matcher.send(MessageSegment.record(send_acc))
    
async def poke_send(event:PokeNotifyEvent,matcher:Matcher):
    if config.poke_send_poke:
        await matcher.send(Message(f"[CQ:poke,qq={event.user_id}]"))
    else:
        return
    
async def poke_rule(event:PokeNotifyEvent):
    """黑白名单判断"""
    group = event.group_id
    if config.poke_black:
        if group in config.poke_ban_group:
            return False
        else:
            return True
    else:
        if group in config.poke_allow_group:
            return True
        else:
            return False        
