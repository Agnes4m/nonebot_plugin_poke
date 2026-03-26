from datetime import datetime, timezone
from io import BytesIO
from typing import Optional

from nonebot.adapters.onebot.v11 import MessageEvent, PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_command, on_notice
from PIL import Image

from .config import config
from .matcher import poke_reply
from .utils import get_data, poke_rule

__version__ = "0.3.0"
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

poke_ = on_notice(
    block=config.poke_block,
    priority=config.poke_priority,
    rule=poke_rule,
)


@poke_.handle()
async def _handle_poke(event: PokeNotifyEvent, matcher: Matcher) -> None:
    """处理戳一戳事件"""
    logger.info("戳戳触发")
    await poke_reply(event, matcher)


add_pic = on_command("zq", aliases={"抓图"}, priority=30)


@add_pic.handle()
async def _handle_add_pic(event: MessageEvent, matcher: Matcher) -> None:
    """处理添加图片命令"""
    images: list[bytes] = []
    success = 0
    fail = 0

    async def fetch_image(url: Optional[str]) -> bool:
        """获取图片数据"""
        nonlocal success, fail
        if url is None:
            fail += 1
            return False
        try:
            img_data = await get_data(url)
            if img_data:
                success += 1
                images.append(img_data)
                return True
            fail += 1
        except Exception as e:
            logger.warning(f"获取图片失败：{e}")
            fail += 1
        return False

    # 处理回复消息中的图片
    if event.reply:
        for pic in event.reply.message["image"]:
            url = pic.data.get("url") if hasattr(pic, "data") else str(pic)
            await fetch_image(url)

    # 处理当前消息中的图片
    for msg_seg in event.message:
        if msg_seg.type == "image":
            await fetch_image(msg_seg.data.get("url"))

    if not images:
        logger.debug("没有找到图片")
        return

    # 保存图片
    timestamp = int(datetime.now(timezone.utc).timestamp())
    path = config.get_poke_path() / "pic"
    path.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(images):
        try:
            img_type = (Image.open(BytesIO(img)).format or "png").lower()
            img_path = path / f"{timestamp + i}.{img_type}"
            img_path.write_bytes(img)
            logger.debug(f"成功保存图片: {img_path}")
        except Exception as e:
            logger.warning(f"保存图片失败: {e}")
            fail += 1

    await matcher.send(
        f"添加完成，成功{success}张，失败{fail}张，可用于戳戳随机图",
        at_sender=True,
    )
