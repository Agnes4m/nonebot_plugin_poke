import imghdr
from datetime import datetime
from typing import List

from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_command, on_notice

from .matcher import poke_reply
from .utils import config, get_data, poke_rule

__version__ = "0.1.4"
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
    images: List[bytes] = []
    images_name: List[str] = []

    success: int = 0
    fail: int = 0

    # 处理回复消息中的图片
    if event.reply:
        for pic in event.reply.message["image"]:
            _img = None
            try:
                _img = await get_data(str(pic.data.get("url", "")))
                if not _img:
                    return
                success += 1
                images.append(_img)
            except Exception as e:
                if _img:
                    success += 1
                    images.append(_img)
                else:
                    logger.warning(f"获取图片失败: {e}")
                    fail += 1

            # 处理消息中的图片

            msg: Message = event.dict()["message"]
            for msg_seg in msg:
                if msg_seg.type == "image":
                    try:
                        _img = await get_data(str(msg_seg.data.get("url", "")))
                        success += 1
                        if not _img:
                            return
                        images.append(_img)

                    except Exception as e:
                        if _img:
                            success += 1
                            images.append(_img)
                        else:
                            fail += 1
                        logger.warning(f"获取图片失败: {e}")
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
