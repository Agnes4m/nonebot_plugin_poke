import random
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

import aiofiles
import aiohttp
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher

from .config import config

# 支持的图片格式
SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
# 支持的音频格式
SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".aac", ".acc"}

# 默认文本回复
DEFAULT_TEXTS = [
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


@asynccontextmanager
async def get_http_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """获取 HTTP 会话的上下文管理器"""
    timeout = aiohttp.ClientTimeout(total=600)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    }
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        yield session


async def get_data(url: str) -> Optional[bytes]:
    """从 URL 获取数据"""
    if not url:
        return None

    try:
        async with get_http_session() as session, session.get(url) as response:
            if response.status == 200:
                return await response.read()
            logger.warning(f"获取数据失败，状态码: {response.status}")
    except Exception as e:
        logger.warning(f"获取数据异常: {e}")

    return None


class ResourceManager:
    """资源管理器"""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def get_pic_path(self) -> Path:
        """获取图片目录路径"""
        return self.base_path / "pic"

    def get_acc_path(self) -> Path:
        """获取音频目录路径"""
        return self.base_path / "acc"

    def get_text_path(self) -> Path:
        """获取文本文件路径"""
        return self.base_path / "poke.txt"

    def list_files(
        self,
        directory: Path,
        extensions: set[str],
    ) -> list[Path]:
        """列出目录下指定扩展名的文件"""
        if not directory.exists():
            return []

        return [
            f
            for f in directory.iterdir()
            if f.is_file() and f.suffix.lower() in extensions
        ]


class TextManager:
    """文本管理器"""

    def __init__(self, resource_manager: ResourceManager, bot_nickname: str):
        self.resource_manager = resource_manager
        self.bot_nickname = bot_nickname

    async def get_random_text(self) -> str:
        """获取随机文本"""
        text_path = self.resource_manager.get_text_path()

        try:
            if text_path.is_file():
                async with aiofiles.open(text_path, mode="r", encoding="utf-8") as f:
                    lines = (await f.read()).split("\n")
                    texts = [line.strip() for line in lines if line.strip()]
                    if texts:
                        return random.choice(texts).replace("我", self.bot_nickname)
        except Exception as e:
            logger.warning(f"读取文本文件失败: {e}")

        # 使用默认文本
        return random.choice(DEFAULT_TEXTS).replace("我", self.bot_nickname)


class MediaManager:
    """媒体管理器"""

    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager

    def get_random_pic(self) -> Optional[Path]:
        """获取随机图片"""
        pic_files = self.resource_manager.list_files(
            self.resource_manager.get_pic_path(),
            SUPPORTED_IMAGE_EXTENSIONS,
        )
        return random.choice(pic_files) if pic_files else None

    def get_random_acc(self) -> Optional[Path]:
        """获取随机音频"""
        acc_files = self.resource_manager.list_files(
            self.resource_manager.get_acc_path(),
            SUPPORTED_AUDIO_EXTENSIONS,
        )
        return random.choice(acc_files) if acc_files else None


class PokeSender:
    """戳一戳回复发送器"""

    def __init__(self):
        self.resource_manager = ResourceManager(config.get_poke_path())
        self.text_manager = TextManager(self.resource_manager, config.bot_nickname)
        self.media_manager = MediaManager(self.resource_manager)

    async def poke_send(self, event: PokeNotifyEvent, matcher: Matcher) -> None:
        """发送回戳"""
        await matcher.send(
            Message([MessageSegment("poke", {"qq": str(event.user_id)})]),
        )

    async def pic_send(self) -> Optional[Path]:
        """获取随机图片路径"""
        return self.media_manager.get_random_pic()

    async def text_send(self) -> str:
        """获取随机文本"""
        return await self.text_manager.get_random_text()

    async def acc_send(self, matcher: Matcher) -> None:
        """发送随机音频"""
        acc_file = self.media_manager.get_random_acc()
        if acc_file:
            await matcher.send(
                MessageSegment.record(file=f"file:///{acc_file.resolve()}"),
            )

    async def pic_or_text(
        self,
        send_pic: Optional[Path],
        send_text: Optional[str],
        matcher: Matcher,
    ) -> None:
        """发送图片或文本"""
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


async def poke_rule(event: Event) -> bool:
    """戳一戳事件规则"""
    if not isinstance(event, PokeNotifyEvent) or event.target_id != event.self_id:
        return False

    group = event.group_id
    group_str = str(group) if group else None

    if config.poke_black:
        # 黑名单模式
        return group_str not in set(config.poke_ban_group)

    # 白名单模式：如果白名单为空，则允许所有群
    if not config.poke_allow_group:
        return True

    return group_str in set(config.poke_allow_group)


PS = PokeSender()
