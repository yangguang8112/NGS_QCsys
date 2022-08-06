import React, { useState, useEffect, Component } from 'react';

import Select from 'react-select';
import makeAnimated from 'react-select/animated';

import * as echarts from "echarts/lib/echarts";
// import "echarts/lib/animation";
import "echarts/lib/component/toolbox";
import "echarts/lib/component/title";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/legend";

import { GridComponent } from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { BarChart } from 'echarts/charts';


echarts.use([GridComponent]);
echarts.use([LineChart]);
echarts.use([BarChart]);


function DistrSelect() {
    const [colourOptions, setdata] = useState([]);
    const [selectedOption, setSelectedOption] = useState({value: 'TotalBases_Gb', label: 'TotalBases_Gb', color: '#009879', isFixed: true});

    useEffect(
        () => {
            fetch("select_features").then(
                (res) => res.json().then(
                    (data) => {
                        // console.log(data);
                        for (let i=0;i<data.length;i++) {
                            colourOptions.push(data[i]);
                        }
                        // setSelectedOption(data[3]);
                    }
                )
            );
        }, []);

    
    
    
    // console.log(colourOptions);
    return (
        <div>
            <div className='DistrSelect'>
            <Select
                // closeMenuOnSelect={false}
                // defaultValue={colourOptions[1]}
                // isMulti
                options={colourOptions}
                value={selectedOption}
                onChange={setSelectedOption}
            />
            </div>
            <div>
                <Plot_data features={selectedOption}/>
            </div>
        </div>
    );
}

function inArray(inputarray, check_data) {
    for (let i=0;i<inputarray.length;i++) {
        if (check_data == inputarray[i]) {
            return true;
        }
    }
    return false;
}


function Plot_data(props) {
    // console.log(props.features);
    const [plot_data, setPlotdata] = useState(null);
    const [flag, setFlag] = useState(0);

    useEffect(
        () => {
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ features: [props.features['value']] })
            };
            // console.log(requestOptions);
            fetch("react_features_data", requestOptions).then(
                (res) => res.json().then(
                    (data) => {
                        if (data) {
                            setPlotdata(data[0]);
                            setFlag(flag + 1);
                        } else {
                            setFlag(0);
                        }
                        
                    }
                )
            );
        }, [props.features]);
    

    // return (<Plotting mainid='main0' data={plot_data} feature={infeatures} flag={flag} />);
    if (flag > 0) {
        return (
            <div className='EchartsPlot'>
                <Plotting mainid={props.features['value']} data={plot_data} feature={props.features['value']} flag={flag} />
            </div>
        );
    } else {
    }
    
    
}


function Plotting(props) {
    useEffect(
        () => {
            // console.log(props.feature);
            if (props.feature) {
                var myChart = echarts.init(document.getElementById(props.mainid));
                var xAxisData = props.data[0];
                var data_item = props.data[1];
                var feature_name = props.feature;
                myChart.setOption({
                    title: {
                        // text: feature_name
                    },
                    // legend: {
                    //     data: [feature_name]
                    // },
                    toolbox: {
                        // y: 'bottom',
                        feature: {
                        magicType: {
                            type: ['stack']
                        },
                        dataView: {},
                        saveAsImage: {
                            pixelRatio: 2
                        }
                        }
                    },
                    tooltip: {},
                    xAxis: {
                        data: xAxisData,
                        splitLine: {
                        show: false
                        }
                    },
                    yAxis: {},
                    series: [
                        {
                        name: feature_name,
                        type: 'bar',
                        data: data_item,
                        emphasis: {
                            focus: 'series'
                        },
                        animationDelay: function (idx) {
                            return idx * 10;
                        }
                        },
                    ],
                    animationEasing: 'elasticOut',
                    animationDelayUpdate: function (idx) {
                        return idx * 5;
                    }
                });
            }
    }, [props.flag]);

    return (
        <div id={props.mainid} style={{width: '100%', height: 400}}></div>
    )
}



export default function ReportPage() {
    return (
        <div>
            <div style={{width: "50%", height: "20%"}}>
                <DistrSelect />
            </div>
        </div>
    )
}


