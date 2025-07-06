import random

from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.matcher import Matcher

from .config import config
from .utils import PS


async def poke_reply(event: PokeNotifyEvent, matcher: Matcher):
    if config.poke_send_poke:
        await PS.poke_send(event, matcher)

    if config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        roll = random.random()
        if roll > 0.5:
            await PS.acc_send(matcher)
        else:
            await matcher_pic_text(matcher)
    elif config.poke_send_acc and not (config.poke_send_pic or config.poke_send_text):
        await PS.acc_send(matcher)
    elif not config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        await matcher_pic_text(matcher)
    else:
        return


async def matcher_pic_text(matcher):
    if config.poke_send_pic and config.poke_send_text:
        await PS.pic_or_text(
            await PS.pic_send(),
            await PS.text_send(),
            matcher,
        )
    elif config.poke_send_pic and not config.poke_send_text:
        await PS.pic_or_text(await PS.pic_send(), None, matcher)
    elif not config.poke_send_pic and config.poke_send_text:
        await PS.pic_or_text(None, await PS.text_send(), matcher)
