import random

from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.matcher import Matcher

from .utils import acc_send, config, pic_or_text, pic_send, poke_send, text_send


async def poke_reply(event: PokeNotifyEvent, matcher: Matcher):
    if config.poke_send_poke:
        await poke_send(event, matcher)

    if config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        roll = random.random()
        if roll > 0.5:
            await acc_send(matcher)
        else:
            await matcher_pic_text(matcher)
    elif config.poke_send_acc and not (config.poke_send_pic or config.poke_send_text):
        await acc_send(matcher)
    elif not config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        await matcher_pic_text(matcher)
    else:
        return


async def matcher_pic_text(matcher):
    if config.poke_send_pic and config.poke_send_text:
        await pic_or_text(
            await pic_send(),
            await text_send(),
            matcher,
        )
    elif config.poke_send_pic and not config.poke_send_text:
        await pic_or_text(await pic_send(), None, matcher)
    elif not config.poke_send_pic and config.poke_send_text:
        await pic_or_text(None, await text_send(), matcher)
