#! https://zhuanlan.zhihu.com/p/505928759
[TOC]

# </center>SurFree: a fast surrogate-free black-box attack

### 1.笔记加代码

知乎笔记地址：https://zhuanlan.zhihu.com/p/386736751和https://zhuanlan.zhihu.com/p/385184107

代码：https://github.com/t-maho/SurFree

### 2.背景

这是<font size=5, face="黑体">**cvpr2021**</font>年的一篇论文，内容是关于黑盒攻击--决策攻击的。这种类型的攻击只知道top-1的标签，是黑盒设置中最难的情景。在前面的HSJA、QEBA、GeoDA这几篇决策攻击的论文当中，基本上都采用了替代的方法，也就是说，他们的方法步骤为：

1. 标记（找到一个样本点，这是一个已经成功攻击的点。在无目标当中，是将原始图片加上噪声，在有目标当中，是将目标类图片作为样本点）
2. 替代方法（最常采用的方法是梯度估计，也有一些采用了替代模型——迁移攻击，还有的将hard-label转换为score-based）
3. 对抗样本的更新（找到比当前更好的对抗样本）

本文的创新在于不再采用替代模型，而是利用了决策边界的几何属性。本文的方法可以在更少的查询量的条件下得到较好的对抗样本。本文的思想来源有图片加水印。

### 3.理论推导

<img src="http://github.com/pang-discussion/black_box-attack/blob/main/image/SurFree.png?raw=true" alt="公式推导" style="zoom: 67%;" />

> 显示不出来在http://github.com/pang-discussion/black_box-attack/blob/main/image/SurFree.png中查找。
### 4、算法步骤

![img](https://pic2.zhimg.com/80/v2-7e260ec1c64e82473c7c9395130917fd_1440w.png?raw=true)

大致的方法就是首先构造超平面，然后在该超平面上旋转角度找到更好的对抗样本，接着通过二分查找进一步细化。如果在该超平面上没有找到合适的对抗样本，就再随机找另一个超平面。（超平面的构造用到了离散余弦变换，这一部分还不是很了解）。

### 5、实验

采用的数据集是MNIST和ImageNet，网络采用的是resnet18，参数设置：$T=3,L=100,\theta_{max}=30,\kappa=0.02,二分搜索的\ell=10$，评价指标采用的是所有图片的L2损失取平均值。

在MNIST数据集上是查询数量和失真减少之间的一个权衡，如下面的两幅图所示：

![img](https://pic2.zhimg.com/80/v2-f76ebce47104c16e1a732b549148fab9_720w.jpg?raw=true)

![img](https://pic1.zhimg.com/80/v2-71e2a1f3b44a3a189835b4625d77433c_720w.jpg?raw=true)

下图显示了相对于查询的数量扰动的失真。![[公式]](https://www.zhihu.com/equation?tex=%5Cmathrm%7BSurFree%7D)呈现出一条平滑的曲线，这是对![[公式]](https://www.zhihu.com/equation?tex=350)多幅图像求平均值的结果。其他攻击仍然明显的阶梯形状。由此可以发现![[公式]](https://www.zhihu.com/equation?tex=%5Cmathrm%7BSurFree%7D)展现出更好的数学性质，这里主要特指梯度方面

![img](https://pic3.zhimg.com/80/v2-b2e5a5a602912008069e0b8224f6e35e_720w.jpg)

### 6、想法和总结

这是一个通过<font color='red'>决策边界的几何性质</font>进行攻击的算法，里面也采用了随机的思想，相对于估计梯度的攻击来说，它的每一步基本上都可以找到一个更好的结果，没有出现台阶的情况。

改进思路暂时没有，等到看更多相关方向论文再说。