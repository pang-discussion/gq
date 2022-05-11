[TOC]



# </center> Learning Transferable Visual Models From Natural Language Supervision

### 一、背景

OpenAI2021年初的一篇论文，多模态领域的经典之作，用于文本-图像的预训练，论文最重要的点是CLIP摆脱了基础类的限制（不需要训练具有固定类别数目的分类器），在ZeroShot上做的很好（预训练好之后，不需要任何的后处理操作就可以在ImageNet上达到百分之八十多的准确率）。这篇论文的核心目标是将文本和图像使用图像编码器和文本编码器映射到同一个特征空间。

### 二、思想

这篇论文的idea来自于CMC(Contrastive Multivew Coding)，CMC证明了多模态对比学习的可行性。CLIP就采用了自然语言（文本）的监督信号来学习感知（图片的特征）。这样做的好处是不需要在标注数据了，并且是将文本和图像绑定在一起训练的，训练得到的特征是一个多模态特征。

### 三、方法

图片来自于github.com/pang-discussion/gq/image

<img src="https://github.com/pang-discussion/gq/blob/main/image/CLIP/CLIP_00.png?raw=true" alt="CLIP_00.png" style="zoom: 50%;" />

### 四、实验和局限性

<img src="https://github.com/pang-discussion/gq/blob/main/image/CLIP/CLIP_01.png?raw=true" alt="CLIP_01.png" style="zoom:50%;" />

### 五、思考总结

- 在我看来，本文的主要贡献点在于证明了文本和图像是可以在同一个特征空间的。CLIP给了一个用文本去操作图片的方法，同时作为一个预训练模型，CLIP为下游多模态任务提供了一个多模态特征（文本加图像）。后续的CLIPdraw（文本图像生成）、StyleCLIP(风格迁移图像生成)，还有目标检测等也用到了CLIP方法。
- CLIP 的训练方法是对比学习，这是无监督学习中常用的方法
- CLIP在分类过程中采用了prompt template，值得考虑。
- 最大的局限性在于训练数据集和模型规模都很大（采用了4亿个文本对，在592张A100上训练了18天），对于小实验室不友好，只能在此基础上做一些下游任务