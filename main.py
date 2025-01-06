import json
import os
import traceback
import types

from amiyabot import Message, Chain, log

from core import bot as main_bot
from amiyabot.builtin.messageChain.element import Text,Voice
from core import AmiyaBotPluginInstance

curr_dir = os.path.dirname(__file__)

def handler(prompts):
    log.info('SDGPTIntegrationPluginInstance handler')
    return prompts

class  SDGPTIntegrationPluginInstance(AmiyaBotPluginInstance):
    def load(self):
        pass

    def generate_global_schema(self):

        filepath = f'{curr_dir}/accessories/global_config_schema.json'

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.debug_log(f"Failed to load JSON from {filepath}.")
            return None
        
        if 'amiyabot-blm-library' in main_bot.plugins.keys():
            blm_lib = main_bot.plugins['amiyabot-blm-library']
            
            if blm_lib is not None:
                model_list = blm_lib.model_list()

                try:     
                    data["properties"]["model_name"]["enum"] = [model["model_name"] for model in model_list]
                except KeyError as e:
                    stack_trace = traceback.format_exc()
                    self.debug_log(f"Expected keys not found in the JSON structure: {e}\n{stack_trace}")
                
        return data


def dynamic_get_global_config_schema_data():
    if bot:
        return bot.generate_global_schema()
    else:
        return f'{curr_dir}/global_config_schema.json'

bot : SDGPTIntegrationPluginInstance = None

def generate_global_schema(self):

        filepath = f'{curr_dir}/accessories/global_config_schema.json'

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.debug_log(f"Failed to load JSON from {filepath}.")
            return None
        
        if 'amiyabot-blm-library' in main_bot.plugins.keys():
            blm_lib = main_bot.plugins['amiyabot-blm-library']
            
            if blm_lib is not None:
                model_list = blm_lib.model_list()

                try:     
                    data["properties"]["high_cost_model_name"]["enum"] = [model["model_name"] for model in model_list]
                    data["properties"]["low_cost_model_name"]["enum"] =  [model["model_name"] for model in model_list if model["type"] == "low-cost"]
                    data["properties"]["vision_model_name"]["enum"] =  [model["model_name"] for model in model_list if model["supported_feature"].__contains__("vision")]
                except KeyError as e:
                    stack_trace = traceback.format_exc()
                    self.debug_log(f"Expected keys not found in the JSON structure: {e}\n{stack_trace}")
                
                asistant_list = blm_lib.assistant_list()

                try:
                    data["properties"]["assistant_id"]["enum"] =  [model["name"]+"["+model["id"]+"]" for model in asistant_list]
                except KeyError as e:
                    stack_trace = traceback.format_exc()
                    self.debug_log(f"Expected keys not found in the JSON structure: {e}\n{stack_trace}")


        return data

bot = SDGPTIntegrationPluginInstance(
    name='SD绘图+GPT整合插件',
    version='0.1.0',
    plugin_id='amiyabot-hsyhhssyy-sd-gpt-integration',
    plugin_type='',
    description='安装前请读一下插件文档',
    document=f'{curr_dir}/README.md',
    global_config_default=f'{curr_dir}/accessories/global_config_default.json',
    global_config_schema = dynamic_get_global_config_schema_data
)