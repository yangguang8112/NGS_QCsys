import React, {
    Component
} from "react";
// 引入ECharts主模块 
import * as echarts from "echarts/lib/echarts";
// 引入饼状图需要的模块 
import "echarts/lib/chart/pie";
import "echarts/lib/component/title";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/legend";
class App extends Component { // 初始化状态 
    async componentDidMount() {
        
        var myChart = echarts.init(document.getElementById("main"));
        myChart.setOption(
            {
                title: {
                    text: '高考理科分数占比',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                legend: {
                    left: 'center',
                    top: 'bottom',
                    data: ['语文', '物理', '数学', '化学', '英语', '生物']
                },
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {
                            show: true,
                            type: ['pie', 'funnel']
                        },
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                series: [
                    {
                        name: '分数',
                        type: 'pie',
                        radius: [30, 110],
                        center: ['50%', '50%'],
                        roseType: 'area',
                        data: [
                            {value: 150, name: '语文'},
                            {value: 110, name: '物理'},
                            {value: 150, name: '数学'},
                            {value: 100, name: '化学'},
                            {value: 150, name: '英语'},
                            {value: 90, name: '生物'},
                        ]
                    }
                ]
            }            
        );
    }
    render() {
            return <div id = "main" style = { {  width: 1000, height: 400 }}> </div>; 
    }
}
export default App;