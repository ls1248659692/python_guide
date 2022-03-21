#  第二版: Vue前台高仿 + Django3.1 + DjangoRestful Framework + Ant Design Pro V4 开发的在线教育网站及后台管理
使用TyAdmin(现代化的Xadmin替代品)生成管理后台前后端，并自动对接。✨ 强烈推荐使用:

>https://github.com/mtianyan/tyadmin_api_cli 


- v2版前台体验地址: https://imooc.funpython.cn
- v2版在线体验地址: https://imooc.funpython.cn/xadmin

>账号: mtianyan
密码: admin2020

# 前后台效果展示

![](http://cdn.pic.mtianyan.cn/blog_img/20201204233749.png)

![](http://cdn.pic.mtianyan.cn/blog_img/20201204233849.png)

>https://github.com/mtianyan/tyadmin_api_cli


Vue前台代码地址: https://github.com/mtianyan/vue-mooc
Vue前台代码原作者及文档: https://github.com/wangtunan/vue-mooc  https://wangtunan.github.io/vue-mooc/

## 运行指南:

### docker运行

```
git clone https://github.com/mtianyan/OnlineMooc.git
cd OnlineMooc
docker-compose up

# 导入数据
docker exec -it onlinemooc_mtianyan_mysql_1 bash
mysql -u root -p -D online_mooc < sql/online_mooc.sql
# 输入密码: mtianyanroot 
```

### 本地环境运行

后端项目运行:

```
git clone https://github.com/mtianyan/OnlineMooc.git
cd OnlineMooc
pipenv shell
pip install -r requirements.txt

# Navicat创建数据库，导入mxonline3.sql
# 修改settings.py 中数据库密码

python manage.py runserver
```




