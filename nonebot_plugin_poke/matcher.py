from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import PokeNotifyEvent,MessageSegment

from .utils import *

async def poke_reply(event:PokeNotifyEvent,matcher:Matcher):
    if config.poke_send_poke:
        await poke_send(event,matcher)

    if config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        roll = random.random()
        if roll > 0.5:
            await acc_send(matcher)
        else:
            await matcher_pic_text(event,matcher)
    elif config.poke_send_acc and not (config.poke_send_pic or config.poke_send_text):
        await acc_send(matcher)
    elif not config.poke_send_acc and (config.poke_send_pic or config.poke_send_text):
        await matcher_pic_text(event,matcher)
    else:
        return
    
async def matcher_pic_text(event,matcher):
    if config.poke_send_pic and config.poke_send_text:
        await pic_or_text(await pic_send(event,matcher),await text_send(event,matcher),matcher)
    elif config.poke_send_pic and not config.poke_send_text:
        await pic_or_text(await pic_send(event,matcher),None,matcher)
    elif not config.poke_send_pic and config.poke_send_text:
        await pic_or_text(None,await text_send(event,matcher),matcher)