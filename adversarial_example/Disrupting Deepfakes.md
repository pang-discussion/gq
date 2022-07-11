## </center>Disrupting Deepfakes: Adversarial Attacks Against Conditional Image Translation Networks and Facial Manipulation Systems
### 一、相关知识

&emsp;&emsp;本文是ECCV2020年的一篇论文，关于对抗样本和deepfake的，是一篇开山之作，讲的是如何使用对抗样本作为一种防御手段来防御图片被deepfake破坏。在传统方法上，人们是通过二分类的思路来判断一张图片是否被deepfake过，这篇论文首次提出可以通过在原始图片上加入对抗噪声，来防止图片被deepfake。难点在于：

* deepfake中的属性操作等需要用到**条件类**，但是在现实情况下，我们不知道攻击者到底想要控制图片做什么，这样给防御造成了困难。

* deepfake可以使用**模糊操作**之后的图片进行，但是对抗样本经过模糊之后往往会失去其作用。（因为不知道模型的模糊操作类型和幅度，因此这种被作者称之为灰盒场景）

&emsp;&emsp;为了解决上面两个问题，本文提出了以下的方法：

* 迭代类迁移扰动和联合类迁移扰动
* 扩频扰乱（spread-spectrum disruption）

&emsp;&emsp;本文的代码地址为：https://github.com/natanielruiz/disrupting-deepfakes。本文所采用的攻击模型为**GANimation 、StarGAN 、pix2pixHD  和 CycleGAN**，所使用的数据集为**CelebA**，选择的攻击方法为**FGSM、I-FGSM和PGD**。

### 二、方法

#### 1. Image Translation Disruption

&emsp;&emsp;这个场景是没有条件类的情况下，只需要简单的将基于图片的对抗攻击扩展到对图像翻译任务的对抗攻击，具体的方法如公式（2-1）所示，其中$\boldsymbol{r}$是一个目标类别，我们需要的是让生成器生成的图片尽可能的原理目标类别，因此可以选择deepfake的输出作为$\boldsymbol{r}$。
$$
\max _{\boldsymbol{\eta}} L(\boldsymbol{G}(\boldsymbol{x}+\boldsymbol{\eta}), \boldsymbol{r}), \quad \text { subject to }\|\boldsymbol{\eta}\|_{\infty} \leq \boldsymbol{\epsilon} \tag{2-1}
$$
&emsp;&emsp;同时，我们也可以进行有目标的攻击，如公式（2-2）所示，此时的$\boldsymbol{r}$可以选择原始图片，这样做的目的是使得deepfake的输出尽可能的接近原始图片，也就是说使得deepfake失效
$$
\min _{\boldsymbol{\eta}} L(\boldsymbol{G}(\boldsymbol{x}+\boldsymbol{\eta}), \boldsymbol{r}), \quad \text { subject to }\|\boldsymbol{\eta}\|_{\infty} \leq \boldsymbol{\epsilon} \tag{2-2}
$$
&emsp;&emsp;接下来就可以直接使用FGSM、I-FGSM和PGD等方法进行优化（也就是基于梯度的方法生成对抗样本，L使用的是均方误差）。

#### 2. Conditional Image Translation Disruption

&emsp;&emsp;在某些情况下，deepfake的输入不光包括了图像，还包括了需要操作的类别，这种情况可以表示为$y=G(x,c)$。在这种情况下，当$i\ne j$时，我们不能够保证$(x, c_i)$生成的对抗样本可以成功的迁移到$(x,c_j)$中，因此本文的作者提出了一种集成的方案，如公式（2-3）所示。
$$
\boldsymbol{\eta}=\underset{\boldsymbol{\eta}}{\arg \min } \sum_{\boldsymbol{c}}[L(\boldsymbol{G}(\boldsymbol{x}+\boldsymbol{\eta}, \boldsymbol{c}), \boldsymbol{r})], \quad \text { subject to }\|\boldsymbol{\eta}\|_{\infty} \leq \boldsymbol{\epsilon} \tag{2-3}
$$
&emsp;&emsp;在这种方案下，作者又提出了两种优化方法，一种是迭代类迁移扰动，另一种是联合类迁移扰动。这两种方案都是在I-FGSM的基础上改编的。

1. 迭代类迁移扰动

&emsp;&emsp;这种方案是说，每次迭代的过程中选择其中一个类别来更新$\eta$。

2. 联合类迁移扰动

&emsp;&emsp;这种方案是说，每次迭代的过程中使用所有的类别的梯度的和作为方向来更新$\eta$。

#### 3. GAN Adversarial Training

&emsp;&emsp;在这一小节中，作者提出了将分类网络的对抗训练扩展到GAN网络中。作者提出了G+D对抗训练，具体的表达式如公式（2-4）所示。
$$
\mathcal{L}=\mathbb{E}_{\boldsymbol{x}, \boldsymbol{\eta}_{1}}\left[\log \boldsymbol{D}\left(\boldsymbol{x}+\boldsymbol{\eta}_{1}\right)\right]+\mathbb{E}_{\boldsymbol{x}, \boldsymbol{c}, \boldsymbol{\eta}_{2}, \boldsymbol{\eta}_{3}}\left[\log \left(1-\boldsymbol{D}\left(\boldsymbol{G}\left(\boldsymbol{x}+\boldsymbol{\eta}_{2}, \boldsymbol{c}\right)+\boldsymbol{\eta}_{3}\right)\right)\right] \tag{2-4}
$$

#### 4. Spread-Spectrum Evasion of Blur Defenses

&emsp;&emsp;通过图片模糊操作可以有效的防范对抗样本的攻击，因此如果不知道模糊操作类别的话，我们生成的对抗样本很有可能会再次被deepfake攻击，因此本文提出了扩频扰乱，用于模糊操作的场景下。具体的优化公式如公式（2-5）所示。其中$\boldsymbol{f}_{k}$表示第k种模糊操作类别，这个方法跟前面的迭代类迁移扰动很相似。
$$
\tilde{\boldsymbol{x}}_{t}=\operatorname{clip}\left(\tilde{\boldsymbol{x}}_{t-1}-\boldsymbol{\epsilon} \operatorname{sign}\left[\nabla_{\tilde{\boldsymbol{x}}} L\left(\boldsymbol{f}_{k}\left(\boldsymbol{G}\left(\tilde{\boldsymbol{x}}_{t-1}\right)\right), \boldsymbol{r}\right)\right]\right) \tag{2-5}
$$

### 三、结果

1. 白盒情况下的攻击结果

<img src="F:\学习\论文笔记\图片\image-20220701195646067.png" alt="image-20220701195646067" style="zoom: 67%;" />

&emsp;&emsp;其中%dis表示的是攻击成功率，指标是$L_2$范数的值$\ge 0.05$。从表中可以看出GANimation最鲁棒。

2. $\boldsymbol{r}$的更改

<img src="F:\学习\论文笔记\图片\image-20220701200123529.png" alt="image-20220701200123529" style="zoom:67%;" />

&emsp;&emsp;由表可以看出$\boldsymbol{r}$的值采用deepfake的正常输出时的效果最好。其中的black、white、random noise表示的是将一张全黑的图片、全白的图片和随机的噪声图片作为目标。

3. 迭代类迁移扰动和联合类迁移扰动的结果

<img src="F:\学习\论文笔记\图片\image-20220701200558364.png" alt="image-20220701200558364" style="zoom:67%;" />

&emsp;&emsp;表4采用的方法是寻找一个扰动使得deepfake输出的结果与原来的deepfake输出的结果之间的差异越大越好；表5采用的方法是寻找一个扰动使得deepfake输出的结果与原来的输入图片的结果越接近越好。

4. 扩频扰动的作用

<img src="F:\学习\论文笔记\图片\image-20220701201005960.png" alt="image-20220701201005960" style="zoom:67%;" />

&emsp;&emsp;所用的实验设置是高斯模糊和box模糊，采用了EoT来对比，发现本文的方法还是比较好的

### 四、想法

&emsp;&emsp;作为使用对抗样本攻击deepfake的开山之作，本文是有一定的阅读价值的，本文的方法都比较简单，是基本的从图片对抗样本到deepfake对抗样本的过渡。本文所考略的两个难点也是很重要的。对于条件类的输入，本文只是简单的使用了集成的思路去解决，虽然可以解决部分情况，但是效果还可以提升。（能否使用动态的网络为不同的条件类动态的选择不同的路径去生成对抗样本）。对于模糊操作的情况，这种场景很适合实际情况，作者也是采用了集成的思路去解决，能否有更好的方法去解决尚待考虑。

&emsp;&emsp;另外，本文的场景基本上都是白盒场景，对于黑盒的deepfake攻击也需要进一步挖掘。还有，师兄的MagDR已经证明可以将对抗样本重建成可以再次被攻击的图片，因此通过对抗样本防御deepfake还有许多需要解决的地方。