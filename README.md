# NovelAI绘图

注意：NovelAI需要科学上网才能访问。

注意：NovelAI的提示词仅支持英文。

注意：该插件也使用“兔兔绘图”作为关键词，因此和StableDiffusion冲突，请不要重复安装插件。
如果你同时还使用StableDiffusion.....那建议你用StableDiffusion，因为那边更新的勤快:-)。

### 如何使用

首先你需要获取Presistant API Token

在设置的Account中，点击Get Presistant API Token。

即便第一次使用时也会提示已有Token是否覆盖，不要怕。

![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/images/image-1.png)
![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/images/image.png)

复制token到插件的Persistent API Token配置项中。
然后选择一个模型。

这样就完成了！

## 调节参数/新的模型

如果你想调节生成参数，或者Novelai推出了新的模型，请你首先登录novelai页面，在图片生成的地方，按F12打开控制台，然后切换到网络标签。

![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/image-4.png)

保持控制台打开，回到图片生成页面，调节你的各项参数以及模型，然后点击生成。

切换回控制台，点击并找到网络中“generate-image”多个项目中，负载不为空的项目。
![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/image-5.png)

点击 查看源 按钮，显示源

![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/image-1.png)

复制这里面的所有内容，并保存到一个文本文件中，然后重命名为 model_name.json

![alt text](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-novelai/master/image-3.png)

其中model_name可以在文件中搜索关键字model找到，比如上图例子中，就把文件命名为 nai-diffusion-4-curated-preview.json

然后将这个文件放进兔兔的 resources/novelai/default_params 文件夹下

[缺一张windows下的配图，我不是windows部署截不了图]

然后再回到插件配置里，找到这个模型并选择。就可以使用你这一次的参数生成图片了（不包括提示词）

## 相关链接

[项目地址:Github](https://github.com/hsyhhssyy/amiyabot-hsyhhssyy-stable-diffusion/)

[遇到问题可以在这里反馈(Github)](https://github.com/hsyhhssyy/amiyabot-hsyhhssyy-stable-diffusion/issues/new/)

|  版本   | 变更  |
|  ----  | ----  |
| 0.1.0  | 最初的版本 |