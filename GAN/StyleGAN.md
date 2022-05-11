# </center>A Style-Based Generator Architecture for Generative Adversarial Networks

[TOC]

### 一、背景

这篇论文是NVIDIA在2018年末的时候发表的，用于生成更加可以控制的高清的人脸图像，是在之前NVIDIA的ProGAN的基础上改编的。主要解决图片生成领域当中隐空间里不同特征纠缠在一起这个问题。

### 二、思想

本文的思想来源于风格迁移，采用了风格迁移中的AdaIN归一化方法（这个方法在GAN里面用的挺多的，simswap里面也有这个方法）。在风格迁移中认为，图像的风格主要跟图像的均值和方差有关，然后提出了AdaIN。本文另一个用来解纠缠的方法是不使用服从某种分布的随机变量z作为输入，而是采用了转换之后的w作为合成网络的输入。（这是因为z是符合均匀分布或者高斯分布的随机变量，所以变量之间的耦合性比较大。举个例子，比如特征：头发长度和男子气概，如果按照z的分布来说，那么这两个特征之间就会存在交缠紧密的联系，头发短了你的男子气概会降低或者增加，但其实现实情况来说，短发男子、长发男子都可以有很强的男子气概。所以我们需要将latent code z进行解耦，才能更好的后续操作，来改变其不同特征）。

### 三、方法

<img src="https://github.com/pang-discussion/gq/blob/main/image/StyleGAN.png?raw=true" alt="StyleGAN.png" style="zoom: 50%;" />

### 四、流程

<img src="https://img-blog.csdnimg.cn/20190325145141281.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2EzMTI4NjMwNjM=,size_16,color_FFFFFF,t_70" alt="StyleGAN流程" style="zoom:150%;" />

### 五、总结

- StyleGAN可以用来控制生成图片的特征，后面有很多基于它的改进。后面会重点看一篇论文——styleCLIP
- 里面的AdaIN需要知道原理，以后可能会用到
- 官方的代码是使用TensorFlow写的，正在艰难的阅读中
  