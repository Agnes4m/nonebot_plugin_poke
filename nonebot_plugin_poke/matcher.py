import random

from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.matcher import Matcher

from .config import config
from .utils import PS


async def poke_reply(event: PokeNotifyEvent, matcher: Matcher):
    if config.poke_send_poke:
        await PS.poke_send(event, matcher)

    send_acc = config.poke_send_acc
    send_pic_or_text = config.poke_send_pic or config.poke_send_text

    if send_acc and send_pic_or_text:
        if random.random() > 0.5:
            await PS.acc_send(matcher)
        else:
            await matcher_pic_text(matcher)
    elif send_acc:
        await PS.acc_send(matcher)
    elif send_pic_or_text:
        await matcher_pic_text(matcher)


async def matcher_pic_text(matcher: Matcher):
    send_pic = config.poke_send_pic
    send_text = config.poke_send_text

    if send_pic and send_text:
        await PS.pic_or_text(await PS.pic_send(), await PS.text_send(), matcher)
    elif send_pic:
        await PS.pic_or_text(await PS.pic_send(), None, matcher)
    elif send_text:
        await PS.pic_or_text(None, await PS.text_send(), matcher)
