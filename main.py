import json
import os
import traceback
import types

from amiyabot import Message, Chain, log

from core import bot as main_bot
from amiyabot.builtin.messageChain.element import Text,Voice
from core import AmiyaBotPluginInstance
from .src.message_handler import handle_message, RESOURCE_TEMPLATE_DIR, RESOURCE_DIR
from amiyabot.log import LoggerManager

curr_dir = os.path.dirname(__file__)

logger = LoggerManager('NovelAI')

class  NovelAIPluginInstance(AmiyaBotPluginInstance):
    def load(self):
        pass

    def debug_log(self, msg):
        if self.get_config("show_log"):
            logger.info(f'{msg}')

bot : NovelAIPluginInstance = None

def dynamic_get_global_config_schema_data():
    file = f'{curr_dir}/accessories/global_config_schema.json'
    obj = json.load(open(file, 'r', encoding='utf-8'))
    
    # 读取  RESOURCE_TEMPLATE_DIR, RESOURCE_DIR 目录下的以json结尾的文件
    models = ["..."]
    for file in os.listdir(RESOURCE_TEMPLATE_DIR):
        if file.endswith('.json'):
            models.append(file[:-5])
    
    for file in os.listdir(RESOURCE_DIR):
        if file.endswith('.json'):
            models.append(file[:-5])
    
    try:
        obj["properties"]["model_name"]["enum"] = models
    except Exception as e:
        logger.error(f'NovelAI绘图: 配置文件构造失败: {e} {obj}')

    return obj

bot = NovelAIPluginInstance(
    name='NovelAI绘图',
    version='0.1.0',
    plugin_id='amiyabot-hsyhhssyy-novelai',
    plugin_type='',
    description='安装前请读一下插件文档',
    document=f'{curr_dir}/README.md',
    global_config_default=f'{curr_dir}/accessories/global_config_default.json',
    global_config_schema = dynamic_get_global_config_schema_data,
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