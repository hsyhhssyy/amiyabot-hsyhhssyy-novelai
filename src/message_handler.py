import io
import json
import re
import zipfile
from amiyabot.log import LoggerManager
from amiyabot import Message, Chain

from amiyabot.network.httpRequests import http_requests

logger = LoggerManager('NovelAI')

novelai_request = {
  "action": "generate",
  "input": "rating:general, best quality, very aesthetic, absurdres",
  "model": "nai-diffusion-4-curated-preview"
}

# Authorization: Bearer [PresistentToken]

async def handle_message(bot, data):    

    match = re.search(r'兔兔绘1图[:：]\s?([\s\S]*)', data.text)
    if match:
        prompt = match.group(1)

    await data.send(Chain(data, at=False).text(f'开始绘图，请稍候...'))

    api_key = bot.get_config("api_key")

    headers = {
        "Authorization": f"Bearer api_key"
    }

    model = bot.get_config("model_name")

    extra_model = bot.get_config("extra_model")

    if extra_model is not None and extra_model != "":
        model = extra_model

    extra_params = bot.get_config("extra_params")

    request_json_obj = {
        "action": "generate",
        "input": prompt,
        "model": model,
        "parameters": extra_params
    }

    url = 'https://image.novelai.net/ai/generate-image'
    
    res_raw = await http_requests.post(url,request_json_obj, headers)

    try:
        res_json = json.loads(res_raw)
        if res_json:
            logger.info(res_json)
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

    response = res_raw.response
    file_content = await response.read()
                
    # 将文件内容读入内存中的字节流
    file_stream = io.BytesIO(file_content)

    # 解压缩 ZIP 文件到内存
    with zipfile.ZipFile(file_stream, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.png'):
                with zip_ref.open(file_name) as png_file:
                    png_bytes = png_file.read()
                    
                    await data.send(Chain(data, at=False).image(png_bytes))
                    return
                
    await data.send(Chain(data, at=False).text("NovelAI返回意外的结果。"))
    




