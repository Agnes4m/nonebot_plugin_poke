from pathlib import Path

from nonebot import load_plugin

dir_ = Path(__file__).parent
_ = load_plugin(str(dir_ / "nonebot_plugin_poke"))
