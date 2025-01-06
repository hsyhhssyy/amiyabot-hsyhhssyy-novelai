import json
import os
import traceback
import types

from amiyabot import Message, Chain, log

from core import bot as main_bot
from amiyabot.builtin.messageChain.element import Text,Voice
from core import AmiyaBotPluginInstance
from src.message_handler import handle_message

curr_dir = os.path.dirname(__file__)

class  NovelAIPluginInstance(AmiyaBotPluginInstance):
    def load(self):
        extra_params = self.get_config("extra_params")
        if extra_params is None or extra_params == "":
            # load from file
            paramsfile = f'{curr_dir}/accessories/default_param.json'
            with open(paramsfile, 'r', encoding='utf-8') as f:
                params = json.load(f)
                extra_params_obj = params["parameters"]
                extra_params_str = extra_params_obj
                self.set_config("extra_params", extra_params_str)

bot = NovelAIPluginInstance(
    name='NovelAI绘图',
    version='0.1.0',
    plugin_id='amiyabot-hsyhhssyy-novelai',
    plugin_type='',
    description='安装前请读一下插件文档',
    document=f'{curr_dir}/README.md',
    global_config_default=f'{curr_dir}/accessories/global_config_default.json',
    global_config_schema =f'{curr_dir}/accessories/global_config_schema.json',
)

def enabled_in_this_channel(channel_id:str) -> bool:
    black_list_mode:bool = bot.get_config("black_list_mode")
    black_white_list:list = bot.get_config("black_white_list")


    if black_list_mode:
        if black_white_list is not None and channel_id in black_white_list:
            return False
        else:
            return True
    else:
        if black_white_list is not None and channel_id in black_white_list:
            return True
        else:
            return False

@bot.on_message(keywords=['兔兔绘1图'],level=114514)
async def _(data: Message):

    if enabled_in_this_channel(data.channel_id) == False:
        return

    await handle_message(bot,data)