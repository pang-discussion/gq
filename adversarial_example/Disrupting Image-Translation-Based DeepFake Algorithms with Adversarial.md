## Disrupting Image-Translation-Based DeepFake Algorithms with Adversarial Attacks
### 一、相关知识

&emsp;&emsp;这篇论文是WACV2020年的一篇关于使用对抗样本防御deepfake的一篇论文，与Disrupting Deepfake发表的时间接近。论文的思想比较简单，在这篇论文中提出了两种攻击方法：Nullifying Attack（无效攻击）和Distorting Attack（扰乱攻击），并且文章提出了两个度量指标：similarity score和distortion score。这篇论文最重要的贡献在于证明了采用判别器构建损失函数来攻击deepfake模型是无效的，采用生成器构造损失函数来攻击deepfake模型可以得到较好的结果。本文的代码链接为： https://github.com/jimmy-academia/Adversarial-Attack-CycleGAN-and-pix2pix。

### 二、方法

1. Nullifying Attack

&emsp;&emsp;无效攻击的主要思想是使得deepfake输出的结果与原来的图片越接近越好。因此可以通过最小化deepfake的输出结果和原始图片之间的距离来构造损失函数。具体的公式表示如（2-1）所示。
$$
L_{Null }\left(\boldsymbol{x}_{t}^{*}\right)=-1 \cdot \mathcal{L}\left(G\left(\boldsymbol{x}_{t}^{*}\right)-\boldsymbol{x}\right)\tag{2-1}
$$

2. Distroting Attack

&emsp;&emsp;失真攻击的主要思想是使得deepfake的输出结果产生明显异常——人眼可以直接看出来或者可以轻松的通过分别器识别出来。因此可以通过最大化deepfake输出的结果与原来的结果之间的距离来构造损失函数，具体的公式表示如（2-2）所示。
$$
L_{\text {Dist }}\left(\boldsymbol{x}_{t}^{*}\right)=\mathcal{L}\left(G\left(\boldsymbol{x}_{t}^{*}\right)-G(\boldsymbol{x})\right)\tag{2-2}
$$

3. 度量指标

&emsp;&emsp;本文提出了两个新的定性度量指标，分别是similarity score和distortion score。similarity score是用来度量无效攻击的结果的，具体的公式如（2-3）所示；distortion score是用来度量失真攻击的结果的，具体的公式如（2-4）所示。**采用log的原因是：人类是以对数的方式感知图像变化的。**
$$
s_{\text {sim }}=\max \left(0, \frac{(\log \mathcal{L}(\boldsymbol{y}-\boldsymbol{x}))^{2}}{\log \mathcal{L}\left(\boldsymbol{y}^{*}-\boldsymbol{x}\right) \cdot \log \mathcal{L}\left(\boldsymbol{x}^{*}-\boldsymbol{x}\right)}-1\right)\tag{2-3}
$$

$$
s_{\text {dist }}=\max \left(0, \frac{\log \mathcal{L}\left(\boldsymbol{y}^{*}-\boldsymbol{y}\right)}{\log \mathcal{L}\left(\boldsymbol{x}^{*}-\boldsymbol{x}\right)}-1\right)\tag{2-4}
$$

### 三、实验

**数据集：**CelebA-HQ和CelebAMask-HQ

**攻击的deepfake模型：**CycleGAN、pix2pix和pix2pixHD

实验结果：

<img src="F:\学习\论文笔记\图片\image-20220707145328567.png" alt="image-20220707145328567" style="zoom:67%;" />

<img src="F:\学习\论文笔记\图片\image-20220707145353636.png" alt="image-20220707145353636" style="zoom:67%;" />

### 四、想法

&emsp;&emsp;这篇论文也是采用最简单的使用对抗样本来防御deepfake，考虑了两种场景。





