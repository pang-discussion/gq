## Restricted Black-box Adversarial Attack Against DeepFake Face Swapping
### 一、相关知识

&emsp;&emsp;本文发表于2022年4月份的arxiv上。现有的工作当中，针对deepfake的对抗样本攻击往往采用的是白盒设置，或者是大量查询驱动的黑盒设置，这两者情况都与真实的deepfake场景存在一定的差异。因此本文考虑了**受限黑盒场景**（我们事先不知道对方会采用什么样的deepfake模型，我们甚至不能够访问deepfake模型。）传统的防御deepfake的方法有两种，第一种是采用检测算法判断是否是deepfake，但是这种方法存在一定的时间延迟；第二种方法便是采用对抗样本破坏deepfake的生成阶段，这种方法往往更有效。

&emsp;&emsp;本文采用的方法是：使用**替代模型**生成对抗样本，然后利用对抗样本的**迁移能力**将生成的对抗样本迁移到黑盒的deepfake模型上。

&emsp;&emsp;数据集：（1）自建数据集，含有6274张图片，包含40个不同的男人和38个不同的女人。（2）CelebA

&emsp;&emsp;攻击的deepfake模型：StarGAN、GANimation、SaGAN、AttGAN

&emsp;&emsp;评价指标：SSIM（结构相似度）、FSIM（特征相似度）和BRISQUE（该指标越小越好）

&emsp;&emsp;本文的贡献为：

* 第一个受限黑盒场景
* TCA-GAN：可迁移循环对抗生成对抗网络。后正则化模块：用来增强生成的对抗样本的可迁移性
* 进一步提高了deepfake检测器的性能，可以作为一个辅助器件。

### 二、方法

#### 1. 替代模型

&emsp;&emsp;本文采用的替代模型是autoencoder，用此模型模拟人脸的重建过程。替代模型的训练期间采用的损失函数是重建损失，具体的表达形式如公式（2-1）所示。其中，$\hat{x}$表示对$x$进行随机变换后的图片（包括随机旋转、缩放和平移），这样做的原因是使得替代模型更鲁棒，从而让对抗样本有更好的迁移能力。
$$
\mathcal{L}_{\text {recons }}=\|S(x)-x\|_{1}+\|S(\hat{x})-\hat{x}\|_{1} \tag{2-1}
$$


#### 2. TCA-GAN

&emsp;&emsp;TCA-GAN是在替代模型训练好之后再构建的。它包括两个生成器和两个判别器，其中循环体现在一个GAN生成器用来生成对抗扰动，一个GAN生成器用来消除对抗扰动。具体的流程如图一所示。

<img src="F:\学习\论文笔记\图片\image-20220702135030510.png" alt="image-20220702135030510" style="zoom:67%;" />

<center>图一:TCA-GAN模块</center>

&emsp;&emsp;TCA-GAN包括三个损失函数。

1. 扰动损失$\mathcal{L}_{\text {disr}}$

&emsp;&emsp;扰动损失主要有两个作用，第一个是破坏替代模型的重建过程，也就是使得对抗样本失效，第二个是破坏替代模型的中间潜在变量（这个注意来自于CVPR2019的一篇论文，说的是对特征空间的扰动可以生成可迁移性更好的对抗样本）。扰动损失的具体表达式如公式（2-2）所示。
$$
\begin{aligned}
\mathcal{L}_{d i s r} &=\exp \left\{-\left\|S_{e}(x)-S_{e}\left(G_{P}(x)+x\right)\right\|_{1}\right\} \\
&+\exp \left\{-\left\|S(x)-S\left(G_{P}(x)+x\right)\right\|_{1}\right\}
\end{aligned} \tag{2-2}
$$

2. 循环一致性损失$\mathcal{L}_{\text {cyc}}$

&emsp;&emsp;循环一致性损失的思想是使得生成的对抗扰动和去除的对抗扰动尽可能的接近，这样做是为了更好的监督生成的扰动（这个注意来自于cyclegan）。具体的损失函数如公式（2-3）所示。
$$
\mathcal{L}_{c y c}=\left\|G_{R}\left(x+G_{P}(x)\right)-G_{P}(x)\right\|_{1} \tag{2-3}
$$

3. 对抗损失$\mathcal{L}_{\text {cyc}}$

&emsp;&emsp;本文主要采用了两个GAN，一个用来生成对抗扰动，另一个用来删除对抗扰动，因此对抗损失由这两部分共同构成。具体的损失函数如公式（2-4）所示。
$$
\begin{aligned}
\mathcal{L}_{a d v} &=D_{L}\left(x_{a d v}\right)-D_{L}(x) \\
&+D_{A}\left(x_{a d v}-G_{R}\left(x_{a d v}\right)\right)-D_{A}\left(x_{a d v}\right)
\end{aligned} \tag{2-4}
$$

#### 3. 后正则化阶段

&emsp;&emsp;这一过程的主要目的是从生成的最优的对抗样本中稍微转移一下，找到一个次优的对抗样本，从而实现更好的泛化能力（已经有论文指出越是针对特定模型最好的对抗样本，迁移能力越差）。具体的步骤如图二所示，其思想如公式（2-5）所示。

<img src="F:\学习\论文笔记\图片\image-20220702141103591.png" alt="image-20220702141103591" style="zoom:67%;" />

<center>图二：后正则化操作</center>

$$
\begin{array}{cl}
\max _{x_{r a d v}} & {\left[S_{e}\left(x_{r a d v}\right)-S_{e}(S(x))\right] \circ\left[S_{e}\left(x_{a d v}\right)-S_{e}(S(x))\right]} \\
\text { s.t. } & \left\|x_{r a d v}-x\right\|_{\infty}<\epsilon
\end{array} \tag{2-5}
$$

#### 4. 整体算法流程

<img src="F:\学习\论文笔记\图片\image-20220702141434158.png" alt="image-20220702141434158" style="zoom:67%;" />

&emsp;&emsp;训练阶段：通过添加对抗扰动和去除对抗扰动来分别模拟对抗攻击和防御。

&emsp;&emsp;应用阶段：用单个人脸图像生成对抗扰动，然后利用后正则化来找到迁移性更好的对抗样本。

### 三、实验

1. 白盒测试结果

<img src="F:\学习\论文笔记\图片\image-20220702141905920.png" alt="image-20220702141905920" style="zoom:80%;" />

2. 迁移结果

<img src="F:\学习\论文笔记\图片\image-20220702142626597.png" alt="image-20220702142626597" style="zoom:80%;" />

&emsp;&emsp;另外，本文发现本文生成的同一个对抗样本可以针对不同类型的图像翻译任务。

### 四、想法

&emsp;&emsp;本文的对替代模型的攻击来生成对抗样本，然后利用对抗样本的迁移能力攻击黑盒模型是一个很常用的思路。但是本文没有考虑图片质量被压缩的情况下如何成功的攻击模型，这个一个可以继续研究的方向。