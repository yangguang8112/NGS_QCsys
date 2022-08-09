# NGS_QCsys


### Install
``` shell
pip install -r requirement.txt

cd react_module
npm install
```

React 目录初始构造如下（不要执行仅作记录）
``` shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
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