import random
from pathlib import Path
from typing import Optional

import aiofiles
import aiohttp
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PokeNotifyEvent
from nonebot.matcher import Matcher

from .config import config


async def get_data(url: str) -> Optional[bytes]:
    if not url:
        return None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    }
    timeout = aiohttp.ClientTimeout(total=600)
    async with (
        aiohttp.ClientSession() as session,
        session.get(url, headers=headers, timeout=timeout) as response,
    ):
        return await response.read() if response.status == 200 else None


class PokeSender:
    def __init__(self):
        self.poke_path = config.get_poke_path()
        self.bot_nickname = config.bot_nickname

    async def poke_send(self, event: PokeNotifyEvent, matcher: Matcher):
        await matcher.send(
            Message([MessageSegment("poke", {"qq": str(event.user_id)})]),
        )

    async def pic_send(self) -> Optional[Path]:
        pic_file_path = self.poke_path.joinpath("pic")
        pic_file_path.mkdir(parents=True, exist_ok=True)
        pic_file_list = [
            f
            for f in pic_file_path.iterdir()
            if f.is_file()
            and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        ]
        return random.choice(pic_file_list) if pic_file_list else None

    async def text_send(self) -> str:
        text_path = self.poke_path.joinpath("poke.txt")
        default_texts = [
            "lsp 你再戳？",
            "连个可爱美少女都要戳的肥宅真恶心啊。",
            "你再戳！",
            "？再戳试试？",
            "别戳了别戳了再戳就坏了 555",
            "我爪巴爪巴，球球别再戳了",
            "你戳你🐎呢？！",
            "请不要戳我 >_<",
            "放手啦，不给戳 QAQ",
            "喂 (#`O′) 戳我干嘛！",
            "戳坏了，赔钱！",
            "戳坏了",
            "嗯……不可以……啦……不要乱戳",
            "那...那里...那里不能戳...绝对...",
            "(。´・ω・) ん?",
            "有事恁叫我，别天天一个劲戳戳戳！",
            "欸很烦欸！你戳🔨呢",
            "再戳一下试试？",
            "正在关闭对您的所有服务...关闭成功",
            "啊呜，太舒服刚刚竟然睡着了。什么事？",
            "正在定位您的真实地址...定位成功。轰炸机已起飞",
        ]

        if text_path.is_file():
            async with aiofiles.open(text_path, mode="r", encoding="utf-8") as f:
                send_text = random.choice((await f.read()).split("\n"))
        else:
            async with aiofiles.open(text_path, mode="w", encoding="utf-8") as f:
                await f.write("\n".join(default_texts))
            send_text = random.choice(default_texts)

        return send_text.replace("我", self.bot_nickname)

    async def acc_send(self, matcher: Matcher):
        acc_path = self.poke_path.joinpath("acc")
        acc_path.mkdir(parents=True, exist_ok=True)
        acc_file_list = [
            f
            for f in acc_path.iterdir()
            if f.is_file() and f.suffix.lower() in {".wav", ".mp3", ".acc"}
        ]
        if not acc_file_list:
            return
        await matcher.send(
            MessageSegment.record(
                file=f"file:///{random.choice(acc_file_list).resolve()}",
            ),
        )

    async def pic_or_text(
        self,
        send_pic: Optional[Path],
        send_text: Optional[str],
        matcher: Matcher,
    ):
        if send_pic and send_text:
            await matcher.send(
                MessageSegment.image(file=f"file:///{send_pic.resolve()}") + send_text,
            )
        elif send_pic:
            await matcher.send(
                MessageSegment.image(file=f"file:///{send_pic.resolve()}"),
            )
        elif send_text:
            await matcher.send(send_text)


async def poke_rule(event: Event):
    if isinstance(event, PokeNotifyEvent) and event.target_id == event.self_id:
        group = event.group_id
        if config.poke_black:
            return group not in set(config.poke_ban_group)
        return group in set(config.poke_allow_group)
    return False


PS = PokeSender()
