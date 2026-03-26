import random
from pathlib import Path
from typing import Optional

from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher

from .config import config
from .utils import PS


async def _send_pic_text(matcher: Matcher) -> None:
    """发送图片和/或文本"""
    send_pic = config.poke_send_pic
    send_text = config.poke_send_text

    pic_path: Optional[Path] = None
    text: Optional[str] = None

    if send_pic:
        pic_path = await PS.pic_send()
    if send_text:
        text = await PS.text_send()

    await PS.pic_or_text(pic_path, text, matcher)


async def poke_reply(event: PokeNotifyEvent, matcher: Matcher) -> None:
    """戳一戳回复主逻辑"""
    logger.debug(f"收到戳一戳事件，群号: {event.group_id}, 用户: {event.user_id}")

    # 发送回戳
    if config.poke_send_poke:
        try:
            await PS.poke_send(event, matcher)
        except Exception as e:
            logger.warning(f"发送回戳失败: {e}")

    send_acc = config.poke_send_acc
    send_pic_or_text = config.poke_send_pic or config.poke_send_text

    # 根据配置发送内容
    if send_acc and send_pic_or_text:
        # 随机选择发送语音或图文
        if random.random() > 0.5:
            try:
                await PS.acc_send(matcher)
            except Exception as e:
                logger.warning(f"发送语音失败，尝试发送图文: {e}")
                await _send_pic_text(matcher)
        else:
            await _send_pic_text(matcher)
    elif send_acc:
        # 只发送语音
        try:
            await PS.acc_send(matcher)
        except Exception as e:
            logger.warning(f"发送语音失败: {e}")
    elif send_pic_or_text:
        # 只发送图文
        await _send_pic_text(matcher)
