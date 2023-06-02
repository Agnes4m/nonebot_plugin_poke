from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import  on_notice,on_command
from nonebot.adapters.onebot.v11 import PokeNotifyEvent,MessageSegment, Message,GroupMessageEvent

import random

from pathlib import Path


# __version__ = "0.0.1"
# __plugin_meta__ = PluginMetadata(
#     name="碧蓝航线攻略",
#     description='碧蓝航线井号榜等等攻略',
#     usage='碧蓝航线攻略',
#     type="application",
#     homepage="https://github.com/Agnes4m/nonebot_plugin_AL",
#     supported_adapters={"~onebot.v11"},
#     extra={
#         "version": __version__,
#         "author": "Agnes4m <Z735803792@163.com>",
#     },
# )
poke_ = on_notice(rule=to_me(), block=False)

poke_file_path = Path().joinpath("data/poke")
# 音乐部分
poke_acc_list = poke_file_path.joinpath('acc').iterdir()
acc_file_list = []
for acc_file in poke_acc_list:
    if acc_file.is_file() and acc_file.suffix.lower() in [".wav",".mp3",".acc"]:
        acc_file_list.append(str(acc_file))
poke_file_list = poke_file_path.iterdir()

@poke_.handle()
async def _(event: PokeNotifyEvent):
    group = event.group_id
    if group in [442098812,1040674922]:
        return
    if event.is_tome:
        probability = random.random() # 生成0-1之间的随机数
        # 1%概率回复莲宝的藏话
        if probability < 0.01:
            # 发送语音需要配置ffmpeg, 这里try一下, 不行就随机回复poke__reply的内容
            await poke_.send(MessageSegment.record(Path(aac_file_path)/random.choice(aac_file_list)))
        else:
            pass


@my.handle()
async def _(event:GroupMessageEvent):
    group = event.group_id
    if group in [442098812]:
        return
    voice_path = Path(os.path.join(os.path.dirname(__file__), "resources"))
    all_file_name = os.listdir(str(voice_path))
    voicefile = random.choice(all_file_name)
    await my.finish(MessageSegment.record(Path(aac_file_path/ voicefile)))
