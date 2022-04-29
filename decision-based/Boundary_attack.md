# Decision-Based Adversarial Attacks: Reliable Attacks Against Black-Box Machine Learning Models

[TOC]

### 1、背景

这篇论文是黑盒攻击——hard-label attack的开山之作，发表于ICLR2018。提出这种攻击的目标是这种攻击更符合真实情况，例如无人驾驶。这篇论文的思想比较简单，就是从一个已经是对抗样本的图片中开始出发，然后减小扰动，但同时要保持对抗性。

论文代码：https://github.com/bethgelab/foolbox

（图片加载不出来可以在 https://github.com/pang-discussion/black_box-attack 中寻找）

### 2、算法思想

图片地址在上述GitHub中

![Boundary_attack_00.png](https://github.com/pang-discussion/black_box-attack/blob/main/image/Boundary_attack/Boundary_attack_00.png?raw=true)

### 3、算法步骤

![boundary_attack1.png](https://github.com/pang-discussion/black_box-attack/blob/main/image/Boundary_attack/boundary_attack1.png?raw=true)

算法步骤很简单，主要是里面的思想

### 4、实验

实验就不给了，这是一个开山之作，都是跟原来的方法比的，感兴趣自己看

### 5、总结

这篇论文作为开山之作，其方法也是从其他领域转换到对抗样本领域的，给后来者挖了坑。缺点就是查询次数太多，都是几万几十万。