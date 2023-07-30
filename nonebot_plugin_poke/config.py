from pathlib import Path
from typing import List

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    bot_nickname: str = "宁宁"
    poke_black: bool = True
    poke_ban_group: List[str] = []
    poke_allow_group: List[str] = []
    poke_send_pic: bool = False
    poke_send_poke: bool = True
    poke_send_text: bool = False
    poke_send_acc: bool = False
    poke_path: Path = Path("data/poke")
    poke_priority: int = 1
    poke_block: bool = True

    class Config:
        extra = "ignore"


config = Config.parse_obj(get_driver().config)


if not config.poke_path.exists() or not config.poke_path.is_dir():
    config.poke_path.mkdir(0o755, parents=True, exist_ok=True)
