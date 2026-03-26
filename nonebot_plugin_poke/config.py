from pathlib import Path
from typing import Annotated

from nonebot import get_plugin_config
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class ConfigModel(BaseModel):
    """插件配置模型"""

    bot_nickname: Annotated[
        str,
        Field(
            default="宁宁",
            description="机器人昵称",
        ),
    ]

    poke_black: Annotated[
        bool,
        Field(
            default=True,
            description="是否启用黑名单模式，False 则为白名单模式",
        ),
    ]

    poke_ban_group: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="黑名单群号列表",
        ),
    ]

    poke_allow_group: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="白名单群号列表",
        ),
    ]

    poke_send_pic: Annotated[
        bool,
        Field(
            default=False,
            description="是否发送图片",
        ),
    ]

    poke_send_poke: Annotated[
        bool,
        Field(
            default=False,
            description="是否回戳",
        ),
    ]

    poke_send_text: Annotated[
        bool,
        Field(
            default=True,
            description="是否发送文本",
        ),
    ]

    poke_send_acc: Annotated[
        bool,
        Field(
            default=False,
            description="是否发送语音",
        ),
    ]

    poke_path: Annotated[
        str,
        Field(
            default="data/poke",
            description="数据存储路径",
        ),
    ]

    poke_priority: Annotated[
        int,
        Field(
            default=1,
            description="事件响应优先级",
            ge=1,
        ),
    ]

    poke_block: Annotated[
        bool,
        Field(
            default=True,
            description="是否阻止事件继续传播",
        ),
    ]

    @field_validator("poke_ban_group", "poke_allow_group")
    @classmethod
    def validate_group_list(cls, v: list[str]) -> list[str]:
        """验证群号列表，去除空白并去重"""
        cleaned = [str(group).strip() for group in v if str(group).strip()]
        return list(dict.fromkeys(cleaned))  # 去重并保持顺序

    def get_poke_path(self) -> Path:
        """获取数据存储路径"""
        return Path(self.poke_path)

    def ensure_directories(self) -> None:
        """确保必要的目录存在"""
        base_path = self.get_poke_path()
        (base_path / "pic").mkdir(parents=True, exist_ok=True)
        (base_path / "acc").mkdir(parents=True, exist_ok=True)

    class Config:
        extra = "ignore"


config = get_plugin_config(ConfigModel)
config.ensure_directories()
