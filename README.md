# 运行方法：
### 后端

1. 环境配置

backend中的requirements.txt已经包括所有的依赖项，直接安装到自己的python环境中便可运行。（由于开发环境为3.8，所以强烈建议使用>=3.8的版本）
```bash
pip install  -r requirements.txt
```

2. 程序运行
直接运行backend中的app.py

## 前端

1. 环境配置

vue的依赖项已经保存在了frontend中的package.json上。在确保自身拥有vue-cli的情况下直接运行`npm install`即可完成环境的构建。（注意，本项目的前端代码借鉴了[基础前端后台管理系统——完整版权限开发（附带教程及代码）](https://blog.csdn.net/nanchen_J/article/details/121477925)，所以使用的是vue2）

2. 程序运行
进入frontend文件夹，输入`npm run serve`即可开启前端
> 注：前端只有在后端开启的情况下才能正常使用。但后端开启的情况下可以直接通过网址来访问接口


# 效果演示
## 界面展示
## ![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505267348-368362e3-2681-4daa-b746-39cb5c29abec.png#averageHue=%23f2e8c8&clientId=ube801ec9-1f7d-4&from=paste&height=591&id=u345e17ed&originHeight=665&originWidth=1891&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=95329&status=done&style=none&taskId=uebe5a51b-639d-41f6-ae8d-2dc8f0e744d&title=&width=1680.888888888889)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505316304-06b71f7c-bfad-47b1-be1a-b341c072486a.png#averageHue=%23fefefe&clientId=ube801ec9-1f7d-4&from=paste&height=406&id=u39d9c737&originHeight=457&originWidth=1906&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=55503&status=done&style=none&taskId=u0e4dedfd-acc2-4dec-a729-4faaae333f6&title=&width=1694.2222222222222)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505326553-5b906e05-34a4-4e5e-8ad5-e1232e7075b0.png#averageHue=%23e7cfac&clientId=ube801ec9-1f7d-4&from=paste&height=475&id=u104132ff&originHeight=534&originWidth=1897&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=75459&status=done&style=none&taskId=u25080ae9-67dd-4c29-af48-cc08d970304&title=&width=1686.2222222222222)
## 功能展示
### 进货/下架
#### 低数量商品筛选
当商品的数量少于进货时设置的基准数时，将会被筛选至该页面中展示
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505426146-34604b1f-7013-4401-a2bf-86577a45675f.png#averageHue=%23f2f1d6&clientId=ube801ec9-1f7d-4&from=paste&height=330&id=u217efb68&originHeight=371&originWidth=1912&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=54188&status=done&style=none&taskId=u06b5319b-66ff-4bd1-a892-44de0e5b0a9&title=&width=1699.5555555555557)
#### 进货
当点击对应商品的进货按钮时，将自动读取当前行商品的信息，用户只需要填写进货数量即可
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505714268-7f06ec71-4818-4de8-a7be-66ad0da4678b.png#averageHue=%239d9c9c&clientId=ube801ec9-1f7d-4&from=paste&height=412&id=u0c469800&originHeight=463&originWidth=1902&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=64635&status=done&style=none&taskId=u036c5aeb-5058-4767-8b77-33115faeff5&title=&width=1690.6666666666667)
当点击确认后，商品数量将会更新。并且同步至数据库（后期应拆分为下单和正式入库）![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701507211681-ae08d554-ba7d-41b3-b2bb-5a8a1b54bd02.png#averageHue=%23979797&clientId=ube801ec9-1f7d-4&from=paste&height=379&id=u640e39d2&originHeight=426&originWidth=1897&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=77947&status=done&style=none&taskId=u548a7841-d292-4eda-b332-8e75d9f03c0&title=&width=1686.2222222222222)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505780852-5ace4b05-24f6-443b-9f01-3fef60b98289.png#averageHue=%23dec7a9&clientId=ube801ec9-1f7d-4&from=paste&height=332&id=ub168e7ba&originHeight=373&originWidth=1904&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=54098&status=done&style=none&taskId=u1688b673-2762-41af-b7f5-75a867d9359&title=&width=1692.4444444444443)

#### 下架
当物品已经销售完毕且用户并不认为该商品还有继续出售的必要时便可以对该商品进行下架处理
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701505855956-beef5ea4-4404-4f54-93bd-ef45c6c886dd.png#averageHue=%23999998&clientId=ube801ec9-1f7d-4&from=paste&height=444&id=u05a71c8f&originHeight=499&originWidth=1889&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=73076&status=done&style=none&taskId=udf66c750-c9e0-4f86-8568-44176728304&title=&width=1679.111111111111)
### 添加全新商品
当用户需要添加一种全新的商品时需要点击自主进货按钮。
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701508913843-98b32e5d-bbbf-4822-9700-4312a70b2433.png#averageHue=%23989898&clientId=ube801ec9-1f7d-4&from=paste&height=388&id=u698c7422&originHeight=436&originWidth=1909&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=63906&status=done&style=none&taskId=u4a7b1b56-7eb4-49da-875f-d4dc98402f4&title=&width=1696.888888888889)
在点击添加全新商品后将会进入如下界面
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701508920743-37637bc5-7f86-4a93-a4f8-9f3430e184bd.png#averageHue=%239b9b9b&clientId=ube801ec9-1f7d-4&from=paste&height=672&id=FD50i&originHeight=756&originWidth=1911&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=111854&status=done&style=none&taskId=u46a1422c-1733-406f-ac95-ee9340d80d4&title=&width=1698.6666666666667)
此时用户需要补全商品的信息，在补完信息后商品将被添加至仓库中（后期应添加验证功能来确保商品是真实存在的）
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701509075237-7540e5ab-3be0-4f48-befe-572ddc0a5e2f.png#averageHue=%239b9a9a&clientId=ube801ec9-1f7d-4&from=paste&height=690&id=u95060cad&originHeight=776&originWidth=1899&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=104510&status=done&style=none&taskId=ub00d6550-e810-4d23-8bb7-dfbed7d9cf3&title=&width=1688)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701510373527-7eb3cdca-2ee7-4afb-9f48-2ac73ea0314a.png#averageHue=%238f8f8f&clientId=ube801ec9-1f7d-4&from=paste&height=544&id=ubaf5af31&originHeight=612&originWidth=1854&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=109290&status=done&style=none&taskId=ube9adbe1-f701-407e-b14b-12bf459cb82&title=&width=1648)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40362764/1701510390228-c28de251-dbfb-4c47-ae35-fbb93491c3cd.png#averageHue=%23e0c6a6&clientId=ube801ec9-1f7d-4&from=paste&height=628&id=u85d679d9&originHeight=706&originWidth=1922&originalType=binary&ratio=0.9375&rotation=0&showTitle=false&size=101260&status=done&style=none&taskId=u61ab0149-c25d-4d46-b278-eaaf72647d0&title=&width=1708.4444444444443)


## 预期效果
1. 添加用户的登录系统，确认权限分级以及地区分管
2. 记录销售记录，并统计热度等信息进行制表。进行销售预测。
