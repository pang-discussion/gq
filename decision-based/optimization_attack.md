#! https://zhuanlan.zhihu.com/p/507218545
[TOC]

##  Query-Efficient Hard-label Black-box Attack: An Optimization-based Approach

### 1、背景介绍

这篇论文是hard-label攻击的第二篇论文，发表于ICLR2019，相比于第一篇boundary attack论文借助于几何边界和随机游走思想，这篇论文采用了优化的思想。更确切的说，他将hard-label问题转换为一个实值优化问题，然后用零阶优化方法来求解（里面采用了部分梯度估计的思想）。

论文代码：https://github.com/cmhcbb/attackbox

笔记参考：https://zhuanlan.zhihu.com/p/378599021

（图片加载不出来可以在 https://github.com/pang-discussion/black_box-attack 中寻找）

### 2、方法理论

<img src="https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack.png?raw=true" alt="optimization_attack.png" style="zoom:80%;" />

### 3、算法实现

（1）求解$g(\theta)$的值：

![optimization_attack (1).png](https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack%20(1).png?raw=true)

（2）具体的步骤

![optimization_attack(2).png](https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack(2).png?raw=true)

这一个有一点注意的是，对$u_t$的采样进行了p（原文当中给定的是20）次，求解平均值得到$\hat{g}$。

### 4、实验

数据集采用了MNIST、CIFAR10和ImageNet-1000，每个里面选取其中分类正确的100张图片进行实验。试验指标采用的是L2来判断失真程度以及查询次数。

（1）无目标攻击

![optimization_attack (3).png](https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack%20(3).png?raw=true)

本文的方法比起开山鼻祖有更低的失真，并且查询次数下降了三倍左右（但是还是需要几万几十万的查询）。当然，本文的失真比起CW攻击，还有一定的差距，毕竟CW里面可以用到的东西比hard-label多得多。

（2）有目标攻击

![optimization_attack (4).png](https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack%20(4).png?raw=true)

有目标攻击比起无目标攻击来说，失真程度更大了一点（无目标可以看做向最近的目标攻击）。

![optimization_attack(5).png](https://github.com/pang-discussion/black_box-attack/blob/main/image/optimization_attack(5).png?raw=true)

这个是有目标攻击的一个例子，将目标9攻击成8，先选了一个8，然后一步步迭代，使得它看起来更像9，但是内容还是8.

### 5、总结

这篇论文采用的思想是将不能优化的目标函数转换为可以优化的目标函数，这也是可以借鉴的一种思路，等到后面多看几篇，比较一下代码实现，再来进一步总结。

