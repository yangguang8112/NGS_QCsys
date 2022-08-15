# NGS_QCsys


### Install
``` shell
cd NGS_QCsys
mkdir uploads model
pip install -r requirement.txt

cd react_module
npm install
```

React 目录初始构造如下（不要执行仅作记录）
``` shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
nvm install node
npx create-react-app react_module
cd react_module
npm i --save react-select
npm i -S echarts
```


### TODO
- ~~上传页面的预测按钮~~
- ~~模型页面的比较功能、选择当前模型功能~~
- ~~美化各种框，比如上传框~~
- 页面布局美化
- ~~默认特征可选~~
- ~~当前模型在表中用图像或者高亮的方式展示~~
- ~~搜索框中支持空格分隔查找，因为从excel中复制粘贴出来就是空格分隔的~~
- ~~数据分布可视化~~
- ~~新建训练模型加入数据选择（可以直接用sample id来选择）~~，*上传页面也可以弹窗出来问是否训练以及数据选择(因为新建训练里有选择样本的功能，这里就不做了)*
- ~~在线报表~~
- ~~查看模型训练：样本平衡、参数，万例为什么预测完概率是一条直线分布~~一条直线是因为x+y=1，我用的正负label的概率作为横纵坐标，所以点图肯定都是落在x+y=1这条直线上的
- 特征相关性热图；分布图-点图 特征关联，分bin着色；模型性能，AUC图；select page 默认全选；词云放首页
- 上传数据核心特征check
- 万例降维
- 真正的线上部署
- 模型sample id导出；查找样本，完整数据导出(做条件选择，增加一个可新增的复选框功能，用户可在网页上通过增加条件，筛选数据，数据传入后端作为的where条件)