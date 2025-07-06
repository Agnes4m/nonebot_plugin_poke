from pathlib import Path
from typing import List

from nonebot import get_plugin_config
from pydantic import BaseModel, model_validator


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

    @model_validator(mode="before")
    def ensure_path(self, data: dict):
        if isinstance(data.get("poke_path"), str):
            data["poke_path"] = Path(data["poke_path"])
        return data

    class Config:
        extra = "ignore"


config = get_plugin_config(ConfigModel)
# 初始化
Path(config.poke_path.joinpath("pic")).mkdir(parents=True, exist_ok=True)
Path(config.poke_path.joinpath("acc")).mkdir(parents=True, exist_ok=True)
