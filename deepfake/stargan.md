## StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation[^1]
### 一、相关知识

本文发表于CVPR2018年，**现有的GAN模型为了实现在k个不同的风格域上进行迁移，需要构建k∗(k−1)个生成器，并且还不能跨数据集训练**（标注不能复用）。StarGAN正是为了解决跨多个域、多个数据集的训练而提出的。在StarGAN中，并不使用传统的fixed translation（(e.g., black-to-blond hair），**而是将域信息和图片一起输入进行训练，并在域标签中加入mask vector，便于不同的训练集进行联合训练**。具体的差距如图一所示。代码链接[^2]

![image-20220709165114341](F:\学习\论文笔记\图片\image-20220709165114341.png)

<center>
    图一：原始的GAN模型在跨域上需要使用多个模型，而StarGAN却只需要一个
</center>

### 二、方法

为了能够将StarGAN运用到多个域上，本文对传统的GAN做了如下的更改：

* 在G的输入中**添加目标领域信息c**，即把图片翻译到哪个领域这个信息告诉生成模型。
* D除了具有判断图片是否真实的功能外，还要**有判断图片属于哪个类别的能力**。这样可以保证G中同样的输入图像，随着目标领域的不同生成不同的效果。
* 除了上述两样以外，还需要保证图像翻译过程中图像内容要保存，只改变领域差异的那部分。图像重建可以完整这一部分，**图像重建**即将图像翻译从领域A翻译到领域B，再翻译回来，不会发生变化。

具体的方法如图二所示。首先对于输入的图片（不论是正样本还是生成的样本），判别器不光需要知道图片的真假，还需要判别图片所属的域。将原始图片和所属的域一起送给生成器来生成假图片，假图片也需要使用判别器判断是否是假图片以及假图片所属的域。最后还需要将假图片和真图片所属的域一起给生成器来重建真图片。

<img src="F:\学习\论文笔记\图片\image-20220709171324833.png" alt="image-20220709171324833" style="zoom:80%;" />

<center>
    图二：StarGAN流程
</center>



具体包括三个损失函数：

1. 对抗损失

StarGAN采用的是GAN来解决问题，因此必不可少的就是对抗损失，如公式2-1所示。
$$

\mathcal{L}_{a d v}= \mathbb{E}_{x}\left[\log D_{s r c}(x)\right]+\mathbb{E}_{x, c}\left[\log \left(1-D_{s r c}(G(x, c))\right)\right]\tag{2-1}
$$

2. 域分类损失

StarGAN的判别器除了需要判别一张图片是真实图片还是假图片之外，还需要判断图片所属的域，此时需要分别考虑真实图片，如公式2-2所示，和假图片，如公式2-3所示。
$$
\mathcal{L}_{c l s}^{r}=\mathbb{E}_{x, c^{\prime}}\left[-\log D_{c l s}\left(c^{\prime} \mid x\right)\right]\tag{2-2}
$$

$$
\mathcal{L}_{c l s}^{f}=\mathbb{E}_{x, c}\left[-\log D_{c l s}(c \mid G(x, c))\right]\tag{2-3}
$$

3. 重建损失

在做完图片转换之后，我们需要保证图片只有一部分经过了变换，其他的部分需要保持原样，这个可以使用重建损失来实现，重建损失是通过循环一致性损失来实现的，具体的如公式2-4所示。本文的循环一致性损失是通过同一个判别器来做的。
$$
\mathcal{L}_{r e c}=\mathbb{E}_{x, c, c^{\prime}}\left[\left\|x-G\left(G(x, c), c^{\prime}\right)\right\|_{1}\right]\tag{2-4}
$$
最终的生成器和判别器损失分别如公式2-5和公式2-6所示。
$$
\mathcal{L}_{D}=-\mathcal{L}_{a d v}+\lambda_{c l s} \mathcal{L}_{c l s}^{r}\tag{2-5}
$$

$$
\mathcal{L}_{D}=-\mathcal{L}_{a d v}+\lambda_{c l s} \mathcal{L}_{c l s}^{r}\tag{2-6}
$$

为了能够同时使用多个数据集来训练，作者使用了Mask vector。具体的方法如图三所示。

![image-20220709192227939](F:\学习\论文笔记\图片\image-20220709192227939.png)

<center>
    图三：mask vector示意图
</center>

### 三、实验

数据集采用的是CelebA和RaFD，具体的实验结果不太重要。

### 四、想法

本文可以同时训练多个域和多个数据集，主要靠的是mask vector和域分类器的作用。另一个很重要的思想是循环一致性损失，特别的本文的循环一致性损失是通过一个生成器和判别器来实现的，这也可以运用到对抗样本的生成当中（通过GAN生成对抗样本，同时需要可以还原回去）。

-------

[^1]:[StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation](https://arxiv.org/abs/1711.09020)
[^2]:[代码](https://github.com/yunjey/StarGAN)