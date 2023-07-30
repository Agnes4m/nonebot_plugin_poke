import imghdr
from datetime import datetime
from typing import List

from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, PokeNotifyEvent
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_command, on_notice

from .matcher import poke_reply
from .utils import config, get_data, poke_rule

logo = """
    ......                  ` .]]@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    ......                ,/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    ......            /O@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@OO^       
    `.....           ,@^=.OOO\/\@@@@@@@@@@@@@@@@@@@@OO//@@@@@/OO\]]]OO\]
    ``....          ,@@/=^OOOOOOOO@@@@@@@@@@@\]OOOOOOO^^=@@@@OOOOOOOOOOO
    `.....          O@O^==OOOOOOOO@@@/.,@@@OOOOOOOOOOO\O,@@@@OOOOOOOOO@@
    ......    ,    .@@@^=`OOOOOOOOO/  ,O@@OOOOOOOOOOOOOO.O@@@OO/[[[[[[[.
    ......    =..,//@@@^=`OOOOOOOOO@.*=@@@OOOOOOOOOOOOOO]@@@OOO.     ,/`
    ......    =.\O]`,@O^\=OOOO@@@@@@O`=@@@@@@@OOOOOOOO*O,OO^....[[``]./]
    ......    ,^.oOoO@O^=,OO@@@@@OoO`\O\OO@@@@OOOOOOOOO]@@^.]]]/OOOo.,OO
    ......     =.=OOOO@@@@/[[=/.^,/....*.=^,[O@@@@OOOO.@@OOOOOOOOO/..OOO
    ......      \.\OO`.,....*`.=.^.......=....=@O[\@@O@@[^ ,`.=Oo*.,OOO/
    ......       ,@,`...  ....=^/......../....=/O^....\..O]/[\O[*]/OOO. 
    ......       ]@^.,....*..=O\^........^..*.O.\O.^..=^\..,\/\@OOO[.   
    ......    ,,`O^.,..../.,O`//........=..=`=^.=O`O..=^..OOO*/OOO.     
    ......   .=.=@..^...=^/O`*OO.]...o**\.,/=^...O^@^..^...OO^=`OOO`    
    ......  `=.,O^./.*.,OO`,.,/@/.*,O`,O*/@/`....\O\^......Oo^.^,OOO.   
    ...... .,`.o=^=^.../`...]/`***/O^/@oO@`..[[[[\/=\......O^^...=OO^   
    ......  ^.=`O^O.*.=\],]]]/\O/\@O[=O/`        =.=O....=^O^*....OOO.  
    ...... =../=OO^.*.=@@[[,@@@\ .. ..    ,\@@@@@] =O...`=^@`.....=OO^  
    ...... `..^=OO^.^,@`  ^ =oO\          .O\O@\.,\@@..,^OoO......=OOO. 
    ...... ^...=OO^.^.@^ =^*=^,O          \..Ooo^  ,@..=OOOO..*....OOO. 
    ...... ^...=o@^.`.O@. .  ... .. ....  ^.*`.*^  =^..o@oO@*.=....OOO^ 
    ...... ^...=oOO.*.\O   ... .......... .\   ` ,=^*.,OOOO@^.=`^..=OO\ 
    ...... ^...*`OO.*.=O ........          ......,`*^.=OOOo@^.=^^..=OOO.
    ...... \....*oO^..*O^ ....... @OO[[[`  ......../.,@OOOo@^..OO...OOO`
    ...... =.....*.=`..,O`       .O.....=   ... ^.=..OOOOO=O@..=O^..OOO^
    ...... .^...**.O@...\O^ .     \.....`   .^ /.,^.=O@OO`=O@^..OO`.=OO\
    ...... .^...,.=O=@...OO@\      ,[O\=.    ./`.*.*OOOOO..OOO*..OO.,OOO
    ....../O....../^=O@`..O@@@@@]`    .* .,/@@/..../OOOOO*.,OOO..,OO`=OO
    @OO\ooO....,*/@^,@@@\..@^[\@@@@@@O]*]//[`@^*^*=OOOOOO^..=OO\...\^.\@
    OOooo^..`./oOO@/ =^\/^.^\\....=]......,/@@^O^*O.... .,][],OO\....\`.
    @Oooo\/]OOOOOO/  .  \.=^....,..........[.,OO^=^.    /    ,`\OO`.....
    """
__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="戳一戳事件",
    description="自定义群聊戳一戳事件",
    usage=logo,
    type="application",
    homepage="https://github.com/Agnes4m/nonebot_plugin_poke",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)

poke_ = on_notice(block=config.poke_block, priority=config.poke_priority, rule=poke_rule)


@poke_.handle()
async def _(event: PokeNotifyEvent, matcher: Matcher):
    await poke_reply(event, matcher)


add_pic = on_command("zq", aliases={"抓图"}, priority=30)


@add_pic.handle()
async def _(event: MessageEvent, matcher: Matcher):
    images: List[bytes] = []
    images_name: List[str] = []

    success: int = 0
    fail: int = 0
    if event.reply:
        for pic in event.reply.message["image"]:
            try:
                _img = await get_data(str(pic.data.get("url", "")))
                if not _img:
                    return
                success += 1
                images.append(_img)
            except Exception:
                fail += 1

            msg: Message = event.dict()["message"]
            for msg_seg in msg:
                if msg_seg.type == "image":
                    try:
                        _img = await get_data(str(msg_seg.data.get("url", "")))
                        success += 1
                        if not _img:
                            return
                        images.append(_img)
                    except Exception:
                        fail += 1

            base = 0
            while len(images_name) < len(images):
                images_name.append(str(int(datetime.now().timestamp()) + base))
                base += 1
            images_name = images_name[: len(images)]
            images_name = [
                f"{img_name}.{imghdr.what(None, h=images[i])}"
                for i, img_name in enumerate(images_name)
            ]

            path = config.poke_path.joinpath("pic")
            for i, img in enumerate(images):
                img_path = path / images_name[i]
                with img_path.open("wb+") as f:
                    f.write(img)

            tosend = f"添加完成，成功{success}张，失败{fail}张，可用于戳戳随机图"
            await matcher.send(message=tosend, at_sender=True)
