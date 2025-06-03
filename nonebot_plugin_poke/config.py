from pathlib import Path
from typing import List

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
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


config = get_plugin_config(ConfigModel)
