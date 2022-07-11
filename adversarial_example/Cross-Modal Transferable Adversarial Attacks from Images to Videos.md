## Cross-Modal Transferable Adversarial Attacks from Images to Videos

### 一、相关知识

&emsp;&emsp;本文是CVPR2022年的一篇论文。从前的对抗样本的迁移能力都是在同类模型之间进行的（比如都是从图片分类模型到图片分类模型），这篇论文首次提出了一种新型的可迁移性——跨模态可迁移性（从图片分类模型生成的对抗样本迁移到视频分类模型上）。这个思想产生的主要来源是：**图像模型和视频模型之间的中间特征在一定程度上是相似的**，因此本文提出了一个新的对抗样本生成方法——I2V（image2video）， I2V 通过最小化良性帧和生成的对抗性帧之间的中间特征的余弦相似性来优化对抗性扰动。

&emsp;&emsp;代码位于：https://github.com/zhipeng-wei/Image-to-Video-I2V-attack

### 二、方法

&emsp;&emsp;本文的方法比较简单，采用的是PGD的改编。具体的损失函数如公式（2-1）所示，$g$表示图像分类模型，$g_l$表示图像分类模型的第$l$层，$x^i$表示视频样本$x$的第$i$帧，$\delta$即为添加的对抗性扰动帧。
$$
\underset{\delta}{\arg \min } \operatorname{Cos} \operatorname{Sim}\left(g_{l}\left(x^{i}+\delta\right), g_{l}\left(x^{i}\right)\right), \text { s.t. }\|\delta\|_{\infty} \leq \epsilon\tag{2-1}
$$
&emsp;&emsp;具体的算法流程如图1所示。

<img src="F:\学习\论文笔记\图片\image-20220705181657375.png" alt="image-20220705181657375" style="zoom:80%;" />

### 三、实验

**数据集：**UCF-101和kinetics-400

**图像分类模型：**Alexnet,resnet101,squeezenet1.1,vgg16

**视频分类模型：**Non-local，SlowFast，TPN

消融实验（步长$\alpha$、迭代次数$I$、攻击的层数$l$），对比实验.

### 四、想法

&emsp;&emsp;这篇论文可以跟陈志凯师兄的毕业论文的而第一个方法一起考虑。后续工作还可以考虑时间的影响，进一步提高对抗样本的迁移能力。可以考虑使用GAN来生成对抗样本，同时加入需要的损失函数。