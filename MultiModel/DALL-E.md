# </center>Zero-Shot Text-to-Image Generation

[TOC]

### 一、背景

这篇论文也是OpenAI在2021年出的，它是用来仿照GPT产生一个生成模型，也可以看做是CLIP的应用。DALL-E通过**120亿**参数的模型，在**2.5亿图像文本对**上训练完成。它是一个两阶段的模型：它的第一个阶段是离散变分自编码器（Discrete Variance Auto-Encoder，dVAE），用于生成图像的token。它的第二个阶段是混合了图像和文本特征的，以Transformer为基础的自回归生成模型。

### 二、思想

DALL·E的目标是把文本token和图像token当成一个数据序列，通过Transformer进行自回归，这样后面就可以只通过文本token得到图像token，然后再使用图像解码器得到图像

### 三、方法

<img src="https://github.com/pang-discussion/gq/blob/main/image/DALL-E.png?raw=true" alt="DALL-E.png" style="zoom: 33%;" />

### 四、总结

- 这篇论文的思想也比较简单，就是将文本和图像的token拼接在一起，然后做自回归
- token之间的拼接没有看懂

