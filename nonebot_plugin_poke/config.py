from pathlib import Path

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    bot_nickname: str = "宁宁"
    poke_black: bool = True
    poke_ban_group: list[str] = []
    poke_allow_group: list[str] = []
    poke_send_pic: bool = False
    poke_send_poke: bool = False
    poke_send_text: bool = True
    poke_send_acc: bool = False
    poke_path: str = "data/poke"
    poke_priority: int = 1
    poke_block: bool = True

    def get_poke_path(self) -> Path:
        path = Path(self.poke_path)
        return path if path.is_absolute() else Path("data/poke")

    class Config:
        extra = "ignore"


config = get_plugin_config(ConfigModel)

config.get_poke_path().joinpath("pic").mkdir(parents=True, exist_ok=True)
config.get_poke_path().joinpath("acc").mkdir(parents=True, exist_ok=True)
