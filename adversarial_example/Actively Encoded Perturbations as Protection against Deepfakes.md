## Actively Encoded Perturbations as Protection against Deepfakes

### 一、相关知识

&emsp;&emsp;这篇论文是陈志凯师兄向MM里面投的论文，根据的是贺勇师兄的毕设论文改编的，后面需要详细看一看贺勇师兄的论文和毕设代码。这篇论文也是一篇通过对抗样本防御deepfake的论文，原来的使用对抗样本防御deepfake的论文[^1][^2]可以被方法MagDR[^3]攻破。因此本文考虑了一个新的思路，也就是利用了**视频数据不光含有空间信息——也就是单个图片，也含有时间信息**这个事实，通过增大对抗样本相邻帧之间的方差，使得相邻的视频帧之间存在明显的不一致性来生成新的对抗样本。本文需要做到三个方面：

* 对普通的deepfake模型有强大的扰动能力
* 可以攻破受保护的deepfake模型
* 对图片的转换操作和重建的图片很鲁棒

&emsp;&emsp;因此本文采用的方法是：增加相邻帧之间的方差——使得视频帧之间存在明显的不一致性。

* 两个最近帧之间的高方差可以增强对抗样本的破坏能力
* 高方差可以帮助对抗样本抵消图像变换方法的消除能力

&emsp;&emsp;本文攻击的模型是：表情交换(GANimation)、属性操作(StarGAN)、身份交换(SimSwap).

&emsp;&emsp;本文采用的数据集是：FF++和CelebA

### 二、方法

<img src="F:\学习\论文笔记\图片\image-20220708172058220.png" alt="image-20220708172058220" style="zoom:80%;" />

&emsp;&emsp;这篇论文主要包括两方面，第一部分是用于视频 Deepfake 中断的主动编码扰动、第二部分是通过重构代码进行 Deepfake 检测

#### 1. 用于视频 Deepfake 中断的主动编码扰动

&emsp;&emsp;这个部分的损失函数如公式（2-1）所示。其中$\mathbf{X}_{i}$表示视频数据的第$i$帧，$\delta_{i}$表示相应的对抗扰动，$\mathbf{C}_{T}^{\bmod (i, T)}$表示第$i$帧的扰动编码。其中code set$\mathbf{C}_{T}=\left \{\mathbf{C}_{T}^{1},...,\mathbf{C}_{T}^{T}\right \}$的生成包括两部分——code generation（生成code dictionary）和code distribution。
$$
\arg \min _{\delta_{i}} \mathcal{L}\left(\mathbf{G}\left(\mathbf{X}_{i}+\delta_{i}\right), \mathbf{C}_{T}^{\bmod (i, T)}\left(\mathbf{G}\left(\mathbf{X}_{i}\right)\right)\right)\tag{2-1}
$$
&emsp;&emsp;具体的步骤如下所示：

- 根据$f_{k}(\cdot)$定义code dictionary $\mathbf{C}=\left \{\mathbf{C}_{1},...,\mathbf{C}_{K}\right \}$,其中$K$是转换方法$f_{k}(\cdot)$的个数。
- $\delta_{ik}$生成之后（对于$X_{i}$，采用转换方式$f_{k}$）来定义失真度量$S_{code}(Y_i,\hat Y_{ik})$，其中$S_{code}$的计算公式如公式（2-2）所示（原论文的公式4）。其中$d_i$是正常输出与转换后输出之间的不同，常用的方法有SSIM, PSNR, MSE等。

$$
\mathrm{S}_{\text {code }}=\lambda_{1} \mathbf{d}_{1}+\lambda_{2} \mathbf{d}_{2}+\ldots+\lambda_{M} \mathbf{d}_{M}\tag{2-2}
$$

- 给每一个帧$X_i$分配一个$C_T^{i}$。（特别注意的是需要给相邻的帧不同的扰动）。

&emsp;&emsp;具体的实现代码如图2所示。

![image-20220708192520559](F:\学习\论文笔记\图片\image-20220708192520559.png)

<center>
    图2：code的生成和分配过程
</center>

#### 2. 通过重构代码进行 Deepfake 检测

&emsp;&emsp;有的deepfake在之前会通过防御方法先对图片进行重构（如采用方法MagDR）,这样的话通过对抗样本的攻击方法可能会失效，因此本文提出了通过code相似度来完成准确的检测的方法。

主要的步骤如图3所示：

<img src="F:\学习\论文笔记\图片\image-20220708193000754.png" alt="image-20220708193000754" style="zoom:80%;" />

<center>
    图3：code的重构过程
</center>
&emsp;&emsp;在重构得到$C_{rec}$之后，我们需要比较$C_{rec}$和$C_{ori}$之间的不同，得到$S_{compare}$，具体的公式如（2-3）所示。最后将$S_{compare}$与某个阈值比较来判断是够被deepfake过。
$$
\mathrm{S}_{\text {compare }}=\frac{1}{T} \sum_{t=0}^{T}\left(\mathrm{C}_{\text {ori }}^{t} \wedge \mathbf{C}_{\mathrm{rec}}^{t}\right)\tag{2-3}
$$

### 三、实验结果

#### 1. 不同防御方法的失真性比较

<img src="F:\学习\论文笔记\图片\image-20220708194034782.png" alt="image-20220708194034782" style="zoom:80%;" />

其中跨帧是用来表示一个视频相邻帧之间的差距。

#### 2. 三种 deepfake 任务的被动和主动检测器比较

<img src="F:\学习\论文笔记\图片\image-20220708194228906.png" alt="image-20220708194228906" style="zoom:80%;" />

其中H和L表示的是低质量和高质量

#### 3. 三种 deepfake 任务中不同 deepfake 增强方法下的检测性能

<img src="F:\学习\论文笔记\图片\image-20220708194343350.png" alt="image-20220708194343350" style="zoom:80%;" />

#### 4. 消融实验

帧个数T，不同的code分配策略，扰动大小$\epsilon$

### 四、想法

接下来可以考虑在图片质量下降的情况下，如何保证攻击的性能，以及如何提高对抗样本的迁移能力[^4]。另外这篇论文是在白盒条件下的对抗攻击，设计比较简单。最后，可以考虑如何通过对抗样本将deepfake后的图像还原为原始图像。





------

[^1]:[Disrupting Deepfakes: Adversarial Attacks Against Conditional Image Translation Networks and Facial Manipulation Systems](https://arxiv.org/abs/2003.01279)

[^2]:[Disrupting Image-Translation-Based DeepFake Algorithms with Adversarial Attacks](https://openaccess.thecvf.com/content_WACVW_2020/papers/w4/Yeh_Disrupting_Image-Translation-Based_DeepFake_Algorithms_with_Adversarial_Attacks_WACVW_2020_paper.pdf)
[^3]:[MagDR: Mask-guided Detection and Reconstruction for Defending Deepfakes](https://arxiv.org/abs/2103.14211)

[^4]:[Restricted Black-box Adversarial Attack Against DeepFake Face Swapping](https://arxiv.org/abs/2204.12347)
