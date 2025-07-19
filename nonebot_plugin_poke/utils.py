import random
from pathlib import Path
from typing import Optional

import aiofiles
import aiohttp
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher

from .config import config


async def get_data(url: str) -> Optional[bytes]:
    """获取url内容"""
    if not url:
        return None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    }
    async with (
        aiohttp.ClientSession() as session,
        session.get(url, headers=headers, timeout=600) as response,
    ):
        if response.status == 200:
            return await response.read()
        return None


class PokeSender:
    def __init__(self):
        self.poke_path: Path = config.get_poke_path()
        self.bot_nickname: str = config.bot_nickname

    async def poke_send(self, event: PokeNotifyEvent, matcher: Matcher):
        if config.poke_send_poke:
            await matcher.send(  # pyright: ignore[reportUnknownMemberType]
                Message([MessageSegment("poke", {"qq": f"{event.user_id}"})]),
            )

    async def pic_send(self):
        pic_file_path = self.poke_path.joinpath("pic")
        pic_file_path.mkdir(parents=True, exist_ok=True)
        if config.poke_send_pic:
            poke_pic_list = pic_file_path.iterdir()
            pic_file_list = [
                pic_file
                for pic_file in poke_pic_list
                if pic_file.is_file()
                and pic_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".gif"]
            ]
            return random.choice(pic_file_list) if pic_file_list else None
        return None

    async def text_send(self):
        pic_file_path = self.poke_path

        async def _get_random_text() -> str:
            if pic_file_path.joinpath("poke.txt").is_file():
                async with aiofiles.open(
                    pic_file_path.joinpath("poke.txt"),
                    mode="r",
                    encoding="utf-8",
                ) as f:
                    text_file_list = (await f.read()).split("\n")
                    send_text = random.choice(text_file_list)
            else:
                default_texts = [
                    "lsp你再戳？",
                    "连个可爱美少女都要戳的肥宅真恶心啊。",
                    "你再戳！",
                    "？再戳试试？",
                    "别戳了别戳了再戳就坏了555",
                    "我爪巴爪巴，球球别再戳了",
                    "你戳你🐎呢？！",
                    "请不要戳我 >_<",
                    "放手啦，不给戳QAQ",
                    "喂(#`O′) 戳我干嘛！",
                    "戳坏了，赔钱！",
                    "戳坏了",
                    "嗯……不可以……啦……不要乱戳",
                    "那...那里...那里不能戳...绝对...",
                    "(。´・ω・)ん?",
                    "有事恁叫我，别天天一个劲戳戳戳！",
                    "欸很烦欸！你戳🔨呢",
                    "再戳一下试试？",
                    "正在关闭对您的所有服务...关闭成功",
                    "啊呜，太舒服刚刚竟然睡着了。什么事？",
                    "正在定位您的真实地址...定位成功。轰炸机已起飞",
                ]
                async with aiofiles.open(
                    pic_file_path.joinpath("poke.txt"),
                    mode="w",
                    encoding="utf-8",
                ) as f:
                    _ = await f.write("\n".join(default_texts))
                send_text = random.choice(default_texts)
            return send_text

        def _replace_pronoun(text: str) -> str:
            return text.replace("我", self.bot_nickname)

        send_text = await _get_random_text()
        return _replace_pronoun(send_text)

    async def acc_send(self, matcher: Matcher):
        """语音部分"""
        poke_file_path = config.get_poke_path()
        poke_file_path.joinpath("acc").mkdir(parents=True, exist_ok=True)
        poke_acc_list = poke_file_path.joinpath("acc").iterdir()
        acc_file_list: list[Path] = []
        for acc_file in poke_acc_list:
            if acc_file.is_file() and acc_file.suffix.lower() in [
                ".wav",
                ".mp3",
                ".acc",
            ]:
                acc_file_list.append(acc_file)
        send_acc = random.choice(acc_file_list)
        logger.info(f"选择{send_acc}")
        await matcher.send(
            MessageSegment.record(file=f"file:///{send_acc.resolve()}")
        )  # pyright: ignore[reportUnknownMemberType]

    async def pic_or_text(
        self,
        send_pic: Optional[Path],
        send_text: Optional[str],
        matcher: Matcher,
    ):
        if send_pic and send_text:
            await matcher.send(  # pyright: ignore[reportUnknownMemberType]
                MessageSegment.image(file=f"file:///{send_pic.resolve()}") + send_text,
            )
        elif send_pic and not send_text:
            await matcher.send(  # pyright: ignore[reportUnknownMemberType]
                MessageSegment.image(file=f"file:///{send_pic.resolve()}"),
            )
        elif not send_pic and send_text:
            await matcher.send(send_text)  # pyright: ignore[reportUnknownMemberType]
        return


async def poke_rule(event: Event):
    """黑白名单判断"""
    if isinstance(event, PokeNotifyEvent) and event.target_id == event.self_id:
        group = event.group_id
        return (
            (
                group not in set(config.poke_ban_group)
            )  # pyright: ignore[reportUnnecessaryContains]
            if config.poke_black
            else (
                group in set(config.poke_allow_group)
            )  # pyright: ignore[reportUnnecessaryContains]
        )
    return False


PS = PokeSender()
