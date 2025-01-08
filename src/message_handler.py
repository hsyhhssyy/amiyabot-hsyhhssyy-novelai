import io
import json
import os
import re
import zipfile

import aiohttp
from amiyabot import Message, Chain

from amiyabot.network.httpRequests import http_requests
from core.util import get_resource_dir

curr_dir = os.path.dirname(__file__)

novelai_request = {
  "action": "generate",
  "input": "rating:general, best quality, very aesthetic, absurdres",
  "model": "nai-diffusion-4-curated-preview"
}

RESOURCE_TEMPLATE_DIR = f'{curr_dir}/../accessories/default_params/'
RESOURCE_DIR = os.path.join(get_resource_dir(),"/novelai/default_params')")

os.makedirs(RESOURCE_DIR, exist_ok=True)

async def get_params(bot, model_name, prompt):    
    # 判断RESOURCE_DIR下是否有 model_name.json
    # 如果没有，检查RESOURCE_TEMPLATE_DIR下是否有 model_name.json
    try:
        if not os.path.exists(os.path.join(RESOURCE_DIR, f'{model_name}.json')):            
            if os.path.exists(os.path.join(RESOURCE_TEMPLATE_DIR, f'{model_name}.json')):
                with open(os.path.join(RESOURCE_TEMPLATE_DIR, f'{model_name}.json'), 'r') as f:
                    params = json.load(f)
            else:
                bot.logger.info(f'NovelAI绘图: 未找到模型参数文件 {model_name}.json 请阅读插件说明提供该文件。')
                return None
        else:
            with open(os.path.join(RESOURCE_DIR, f'{model_name}.json'), 'r') as f:
                params = json.load(f)
        
        if params is None:
            return None
        
        if 'parameters' not in params:
            bot.logger.info(f'NovelAI绘图: 模型参数文件 {model_name}.json 内容有误。 请阅读插件说明提供该文件。')
            return None

        old_prompt = params['input']

        old_prompt_json = json.dumps(old_prompt)
        prompt_json = json.dumps(prompt)
        old_json = json.dumps(params)

        new_json = old_json.replace(old_prompt_json,prompt_json)

        return json.loads(new_json)


    except Exception as e:
        bot.logger.info(f'NovelAI绘图: 获取模型参数失败: {e}')
        return None
    
async def handle_message(bot, data):    

    match = re.search(r'兔兔绘1图[:：]\s?([\s\S]*)', data.text)
    if match:
        prompt = match.group(1)

    await data.send(Chain(data, at=False).text(f'开始绘图，请稍候...'))

    api_key = bot.get_config("api_key")

    headers = {
        "Authorization": f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }

    model = bot.get_config("model_name")

    params = await get_params(bot, model, prompt)

    if params is None:
        await data.send(Chain(data, at=False).text("参数错误: " + str(e)))
        return

    url = 'https://image.novelai.net/ai/generate-image'

    bot.debug_log(f'NovelAI请求:{json.dumps(params)}')
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(params)) as response:
            if response.status != 200:       
                try:
                    res_json = json.loads(response.text())
                    if res_json:
                        bot.debug_log(f'NovelAI报错(WithJson):{res_json}')
                        if 'message' in res_json:
                            message = res_json['message']
                            await data.send(Chain(data, at=False).text("NovelAI报错: " + message))
                            return
                        else:
                            await data.send(Chain(data, at=False).text("NovelAI报错。"))
                            return
                except Exception as e:
                    # 解不出来是对的,继续走
                    pass

                bot.debug_log(f'NovelAI报错(WithoutJson):{response}')
                await data.send(Chain(data, at=False).text("NovelAI报错。"))
                return

            file_content = await response.read()
                        
            # 将文件内容读入内存中的字节流
            file_stream = io.BytesIO(file_content)

            # 解压缩 ZIP 文件到内存
            with zipfile.ZipFile(file_stream, 'r') as zip_ref:
                bot.debug_log(zip_ref.namelist())
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.png'):
                        with zip_ref.open(file_name) as png_file:
                            png_bytes = png_file.read()
                            
                            await data.send(Chain(data, at=False).image(png_bytes))
                            return
                
    await data.send(Chain(data, at=False).text("NovelAI返回意外的结果。"))
    




