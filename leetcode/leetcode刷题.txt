> **前言**：算法有三种，**面试算法，竞赛算法和工程算法**， 针对不同的类型算法需要，采取不一样的策略和系统性练习，本文章主要针对**面试算法**， 至于竞赛算法不在讨论范围内，竞赛高手都是初高中生就开始训练，自认为比不了而且工作中也不需要没有收益。

> **竞赛算法**追求的是在一定的时间内，实现一定的算法和数据结构，以解决某一特定的、可能并不具有现实意义的问题，主要用于培养算法思维和逻辑思维。

> **工程算法**追求的是实现一定的算法和数据结构以解决某一特定的具有实际现实意义的问题，对代码的运行速度和内存占用有极致的追求会直接影响用户体验和服务器成本。

---
> **个人简介**： 化工转码全靠自学，目前在国内大厂工作，工作中有30%的时间在人才招聘和培养方面，本人在[力扣上传了数百道问题的解法](https://leetcode-cn.com/u/jam007/)，主要是为了总结算法套路与帮助和我一样转码少走弯路，**我虽然转码，但是比我同龄人在很多方面花的时间要多很多，因为互联网行业太内卷了，所以做事情也得讲究方法并提高效率，我能坚持下来进入大厂，很大的一方面也在于对事情的坚持，自我总结与规划，转行与科班最大的差别就在于专业知识的熟悉程度，这些都是可以空余时间自学补充的，决定人上限的还是对事情的坚持，坚持再坚持, 想放弃了就看看这个视频[Usain Bolt - Track & Training 博尔特坚持训练](https://www.bilibili.com/video/BV1Lf4y1T7vR?spm_id_from=333.337.search-card.all.click)**

> 刷题写代码环境, IDE选用 Pycharm 配置几个必要写代码插件 [Pycharm 写代码插件](https://github.com/ls1248659692/leetcode/blob/master/docs/pycharm_plugin.md) ，并配置 [leetcode 刷题插件](https://github.com/ls1248659692/leetcode/blob/master/docs/leetcode_plugin.md) 方便直接拉取 Leetcode 算法题，直接在 IDE 里面写代码和套用算法模板，提高刷题效率，选用 `Python` 作为刷 leetcode 算法题语言，主要原因也是刷题效率，不同语言解决同类问题思路类似，不用纠结语言的问题，编程语言根据工作需要学习就行。因为工作原因未回复相关消息请见谅，做啥事情如果没有收益不要去干，干久了就是浪费生命，有时间不如多去刷几题

---
**算法题分类思维导图：**

![image.png](https://pic.leetcode-cn.com/1651240775-VQXiOs-image.png)


1. 在 github 仓库的 spider 文件夹下 [spider/problems](https://github.com/ls1248659692/leetcode/tree/master/spider/problems) 都是基于 LeetCode 的题目和解法，已经获取了Leetcode 的全部算法练习题，并按照不同类型题目分类规整整理，方便后续算法题对比与总结 ，有助于帮助大家做到同类型题 **举一反三，一通百通**

>用数据分析的思路做题与分析，别人用一年时间做的题，我们用3个月完成并且形成自己的总结，并形成同类型对比，人与人的差距就是这样产生。[leetcode 所有题与题解文件](https://github.com/ls1248659692/leetcode/blob/master/spider/leetcode.sqlite3)
>在 idea 里面对比同类型题目，并自己总结刷题文档， 方便后续分析自己擅长和不擅长的，然后重点优化
![5f6bc1560e0f0a33fafa2c287913ecb.png](https://pic.leetcode-cn.com/1651239771-JgZoEb-5f6bc1560e0f0a33fafa2c287913ecb.png)
> 目前已经将 树相关的题和题解已经总结，感兴趣的可以自己学习
[leetcode树相关题目汇总总结](https://github.com/ls1248659692/leetcode/tree/master/spider/luken/tree)
![tree题目分类](https://pic.leetcode-cn.com/1651239109-zsyrAC-image.png)
![daa683b2e979a7546121081838e967c.jpg](https://pic.leetcode-cn.com/1651283268-DcKIsP-daa683b2e979a7546121081838e967c.jpg)
> 目前已经有好朋友加入到相关的专项刷题训练计划中，感兴趣的可以私聊我全部免费
![image.png](https://pic.leetcode-cn.com/1651498658-ThdkKq-image.png)

> 将获取到的 leetcode 所有题与题解数据导入 **navicat** 进行数据分析， 通过分析自己做题的历史纪录回溯问题与对比总结， 查看那些错的多。(**总结与提高**)
![image.png](https://pic.leetcode-cn.com/1651240829-vahHnZ-image.png)


2. github 仓库的 book 文件夹下 [算法体系化学习书籍和面试题](https://github.com/ls1248659692/leetcode/tree/master/book)有相关算法系统学习书籍和题目推荐, 主要是针对算法入门的小伙伴参考。

---
**Leetcode 刷题进阶，不仅仅只是ac 后面剩下的路还长不总结刷过的题, 一个月就会忘记**
> 阿里霜神大佬说过刷 leetcode 要追求提交的代码最起码时间上 beats 100% ，如果不能达到 beats 100%，纯粹只是追求AC，可能对该题的理解不会那么深刻。相关学习链接见 [阿里霜神 LeetCode](https://books.halfrost.com/leetcode/) 

> 为何要追求时间效率 beats 100%。霜神大佬认为优化到 beats 100% 才算是把这题做出感觉了。对不同的 Hard 题，大佬最开始都用暴力解法 AC 了，然后只 beats 了 5%，他感觉这题就如同没做一样。而且面试中如果给了这样的答案，面试官也不会满意，**“还有没有更优解？如果在线玩家请求并发量较大或者服务器cpu资源内存空间有限等等怎么优化”**。如果通过自己的思考能给出更优解，面试官会更满意一些。

---
### 面试技巧：
1. 确定和面试官沟通的是否一致，问清楚，题目要看清楚
2. 想所有可能的解法，找时间最优解法
3. coding（多刷多写面试刷多就习惯，写代码没有其他技巧，写多了就会了）
4. test cases（测试样例）

---
## Leetcode 科学刷题总结
1. 职业训练：拆分每题知识点、抽象题目、刻意练习、总结
2. 五毒神掌：做算法的最大误区，只刷一遍，等于刷了个寂寞， 为了ac每一道题，没有任何意义，刷题目的是为了提高自己的算法能力和分析问题能力
3. 新手建议先从简单题通过率逆序排完后开始刷起，从 **30min/题** 提升到 **5min/题**，就可以开始挑战刷中等难度题， 也可以按照一个月只刷同一类型的面试高频题，并总结自己的刷题模板和伪代码
4. 大厂面试只要你能不看答案在10min内刷出中等难度题，能够讲出在暴力破解的基础上的优化思路，再背下八股文，国内大厂基本向你敞开大门
5. 始终保持匀速前进，既不松懈倦怠，亦不急于求成，形成个人刷题套路，坚持坚持再坚持
6. [Usain Bolt - Track & Training 博尔特训练](https://www.bilibili.com/video/BV1Lf4y1T7vR?spm_id_from=333.337.search-card.all.click) 拥抱孤独， 强者都是孤独的

---
### 五毒神掌
#### 第一遍：
1. 读题：5分钟读题 + 思考（如果 10min 都没思路，别想了只是你没接触过这类问题，培养15min解决leetcode算法题的习惯）
2. 10min 写出题目的伪代码， 并暴力破解 AC 并对暴力破解方法进行优化
3. 在暴力求解的优化后看解法（理解多个解法）比较自己和高赞题解的区别并学习
4. 选择一个最简洁而且易懂的别人题解思路， 用自己的代码编写， 代码一定要简洁明了

#### 第二遍：
1. 马上自己写，提交leetcode，代码要简洁与优美，完全按照`pep8`规范
2. 多种解法比较，体会 -> 优化（执行时间对比分析）

#### 第三遍：（24小时之后）
1. 过了一天再重复思考和做题
2. 不同熟悉的解法程度-> 特定类型题目专项训练，leetcode 有训练计划专栏可以自学

#### 第四遍：（1周后）
1. 过了一周：再反复练习相同题目或者相同类型的题目
2. 专项训练回顾与总结不同类型题目求解的代码模板（伪代码）

#### 第五遍：（面试前一周）
1. 面试前一周恢复训练
2. 面试前一周复习算法模板与相应分类出现的题目

---
### 理解人的记忆规律，高频率高效复习
1. 短期记忆: 持续若干天或者一两周的记忆 
2. 中期记忆: 持续数周或者几个月的记忆 
3. 长期记忆: 持续数年甚至永世不会消逝的记忆

---
## 算法题汇总

20 个最常用的、最基础数据结构与算法，我都已经总结在 [算法题模板分类](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates)。欢迎大家观看，后面会把不同的算法的解题模板分享出来给大家。

10 个必考数据结构模板：数组、链表、栈、队列、散列表、二叉树、堆、跳表、图、Trie 树。

10 个必会算法模板：递归、排序、二分查找、搜索、哈希算法、贪心算法、分治算法、回溯算法、动态规划、字符串匹配算法。

### 不同算法类型总结与算法题代码模板
>1. [滑动窗口](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/sliding_window)
>2. [双指针](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/two_pointers)
>3. [快慢指针链表](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/linked_list)
>4. [集合查找](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/union_find)
>5. [二叉树](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/trie_tree)
>6. [字符串](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/string)
>7. [DFS](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/dfs)
>8. [BFS](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/bfs)
>9. [回溯法](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/backtracking)
>10. [双堆模式](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/heap)
>11. [二分法与二分法变种](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/binary_search)
>12. [前K大的数模式HEAP](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/heap)
>13. [分治思想](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/divide_conquer)
>14. [DP 动态规划](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/dynamic_programming)
>15. [排序算法](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/sort)
>16. [链表](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/linked_list)
>17. [二叉搜索树的构建](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/binary_tree)
>18. [位运算](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/bit_manipulation)
>19. [dict](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/dict)
>20. [stack](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/stack)/[queue](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/queue)
>21. [math](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/match)
>22. [array](https://github.com/ls1248659692/leetcode/blob/master/algorithm_templates/array/array_examples.py)
>23. [图](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/graph)
>24. [贪婪算法](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/greedy)
>25. [matrix](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/matrix)
>26. [一般算法题模板](https://github.com/ls1248659692/leetcode/tree/master/algorithm_templates/common)

**如果有小伙伴没看过第一期的分享，第一期分享围绕[怎么从零刷leetcode算法题和分析算法题](https://leetcode-cn.com/circle/discuss/do0HrW/)**
**想来网易的欢迎大家资讯[网易内推贴](https://leetcode-cn.com/circle/discuss/F0R4Iy/)**
**最后祝大家在接下来的找工作季，金三银四都能成为 offer 收割机，找到心仪的工作。**
