import imghdr
from datetime import datetime
from typing import Any, cast

from nonebot.adapters import Message, MessageSegment
from nonebot.adapters.onebot.v11 import MessageEvent, PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_command, on_notice

from .config import config
from .matcher import poke_reply
from .utils import get_data, poke_rule

__version__ = "0.2.0"
__plugin_meta__ = PluginMetadata(
    name="戳一戳事件",
    description="自定义群聊戳一戳事件",
    usage="戳戳",
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
    logger.info("戳戳触发")
    await poke_reply(event, matcher)


add_pic = on_command("zq", aliases={"抓图"}, priority=30)


@add_pic.handle()
async def _(event: MessageEvent, matcher: Matcher):
    images: list[bytes] = []
    images_name: list[str] = []

    success: int = 0
    fail: int = 0

    # 处理回复消息中的图片
    if event.reply:
        for pic in event.reply.message["image"]:
            try:
                url = pic.data["url"] if hasattr(pic, "data") and "url" in pic.data else str(pic)
                img_data = await get_data(url)
                if img_data:
                    success += 1
                    images.append(img_data)
                else:
                    fail += 1
            except Exception as e:
                logger.warning(f"获取图片失败: {e}")
                fail += 1
                
    # 处理消息中的图片
            
    msg: Message[Any] = event.model_dump()["message"]  # pyright: ignore[reportAny, reportExplicitAny]
    for msg_seg in msg:  # pyright: ignore[reportAny]
        msg_seg= cast(MessageSegment[Any], msg_seg)  # pyright: ignore[reportExplicitAny]

        if msg_seg.type == "image":
            try:
                data = msg_seg.data
                str_data: str = cast(str, data.get("url", ""))
                img_data = await get_data(str_data)
                if img_data:
                    success += 1
                    images.append(img_data)
                else:
                    fail += 1
            except Exception as e:
                logger.warning(f"获取图片失败: {e}")
                fail += 1

        if not images:
            return


    timestamp = int(datetime.now().timestamp())
    images_name = [
        f"{timestamp + i}.{imghdr.what(None, h=img)}"
        for i, img in enumerate(images)
    ]

    path = config.get_poke_path().joinpath("pic")
    path.mkdir(parents=True, exist_ok=True)
    
    for img, name in zip(images, images_name):
        img_path = path / name
        with img_path.open("wb") as f:
            _ = f.write(img)

    tosend = f"添加完成，成功{success}张，失败{fail}张，可用于戳戳随机图"
    await matcher.send(message=tosend, at_sender=True)  # pyright: ignore[reportUnknownMemberType]
