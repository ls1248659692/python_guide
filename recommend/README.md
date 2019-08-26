## 推荐系统实例
#### 前言
 推荐系统构建三大方法：基于内容的推荐content-based，
                     协同过滤collaborative filtering，
                     隐语义模型(LFM, latent factor model)

#### 目录
* 基于协同过滤(UserCF)的模型
* 基于隐语义(LFM)的模型
* 基于关系图(PersonalRank)的模型

#### 快速开始
* 数据预处理
    python2 manage.py preprocess

* 模型运行
    python2 manage.py ["pre_process", "cf", "lfm", "personal_rank"]
