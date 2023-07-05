from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import PokeNotifyEvent,MessageSegment, Message

import random
import aiohttp
from typing import List,Optional
from pathlib import Path

from .config import config

async def get_data(url:str):
    """获取url内容"""
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, timeout=600) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None
            
            
async def acc_send(matcher:Matcher):
    """语音部分"""
    poke_file_path = config.poke_path
    poke_file_path.joinpath('acc').mkdir(parents=True, exist_ok=True)
    poke_acc_list = poke_file_path.joinpath('acc').iterdir()
    acc_file_list:List[Path] = []
    for acc_file in poke_acc_list:
        if acc_file.is_file() and acc_file.suffix.lower() in [".wav",".mp3",".acc"]:
            acc_file_list.append(acc_file)
    send_acc = random.choice(acc_file_list)
    await matcher.send(MessageSegment.record(file=f"file:///{send_acc.resolve()}"))
    
async def poke_send(event:PokeNotifyEvent,matcher:Matcher):
    if config.poke_send_poke:
        logger.success('反击戳戳')
        await matcher.send(Message([
        MessageSegment("poke",  {
           "qq": f"{event.user_id}"
       })
    ]))
    else:
        return
    
async def pic_send(event:PokeNotifyEvent,matcher:Matcher):
    """发送图片和text"""
    pic_file_path = config.poke_path
    pic_file_path.joinpath('pic').mkdir(parents=True, exist_ok=True)
    if config.poke_send_pic:
        logger.success('发送图片')
        poke_pic_list = pic_file_path.joinpath('pic').iterdir()
        pic_file_list:List[Path] = []
        for pic_file in poke_pic_list:
            if pic_file.is_file() and pic_file.suffix.lower() in [".png",".jpg",".jpeg",".webp",".gif"]:
                pic_file_list.append(pic_file)
        send_pic = random.choice(pic_file_list)
    else:
        send_pic = None
    return send_pic
        
async def text_send(event:PokeNotifyEvent,matcher:Matcher):
    logger.success('发送文字')
    pic_file_path = config.poke_path
    if pic_file_path.joinpath('poke.txt').is_file():
        with open(pic_file_path.joinpath('poke.txt'),mode='r',encoding='utf-8')as f :
            text_file_list:List[str] = f.read().split('/n')
            send_text = random.choice(text_file_list)
    else:
        with open(pic_file_path.joinpath('poke.txt'),mode='w',encoding='utf-8')as f :
            text_file_list:List[str] = [
            "lsp你再戳？",
            "连个可爱美少女都要戳的肥宅真恶心啊。",
            "你再戳！",
            "？再戳试试？",
            "别戳了别戳了再戳就坏了555",
            "我爪巴爪巴，球球别再戳了",
            "你戳你🐎呢？！",
            "请不要戳我 >_<",
            "放手啦，不给戳QAQ",
            "喂(#`O′) 戳我干嘛！",
            "戳坏了，赔钱！",
            "戳坏了",
            "嗯……不可以……啦……不要乱戳",
            "那...那里...那里不能戳...绝对...",
            "(。´・ω・)ん?",
            "有事恁叫我，别天天一个劲戳戳戳！",
            "欸很烦欸！你戳🔨呢",
            "再戳一下试试？",
            "正在关闭对您的所有服务...关闭成功",
            "啊呜，太舒服刚刚竟然睡着了。什么事？",
            "正在定位您的真实地址...定位成功。轰炸机已起飞",
            ]
            f.write('/n'.join(text_file_list))
            send_text = random.choice(text_file_list)
    send_text.replace('我',config.bot_nickname)
    return send_text

async def pic_or_text(send_pic:Optional[Path],send_text:Optional[str],matcher:Matcher):
    if send_pic and send_text:
        await matcher.send(MessageSegment.image(file=f"file:///{send_pic.resolve()}")+send_text)
        return
    elif send_pic and not send_text:
        await matcher.send(MessageSegment.image(file=f"file:///{send_pic.resolve()}"))
        return
    elif not send_pic and send_text:
        await matcher.send(send_text)
        return
    else:
        return

async def poke_rule(event:PokeNotifyEvent):
    """黑白名单判断"""
    if isinstance(event,PokeNotifyEvent) and event.target_id == event.self_id:
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
    else:
        return False


async def add_pic():
    pic_file_path = config.poke_path.joinpath('pic')
    pic_file_path.mkdir(parents=True, exist_ok=True)
    