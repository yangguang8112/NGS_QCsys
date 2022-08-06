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
    useEffect(
        () => {
            fetch("select_features").then(
                (res) => res.json().then(
                    (data) => {
                        // console.log(data);
                        for (let i=0;i<data.length;i++) {
                            colourOptions.push(data[i]);
                        }
                    }
                )
            );
        }, []);

    
    const [selectedOption, setSelectedOption] = useState(null);


    return (
        <div>
            <div className='DistrSelect'>
            <Select
                closeMenuOnSelect={false}
                defaultValue={[colourOptions[0]]}
                // isMulti
                options={colourOptions}
                value={selectedOption}
                onChange={setSelectedOption}
            />
            </div>
            <div>
                {/* <Plot_data features={selectedOption}/> */}
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
    const [show_plot, setdata] = useState([]);
    const [plot_data, setPlotdata] = useState(new Array());
    const [current_plot_data, setCurrentPlotData] = useState(new Array())
    const [infeatures, setInfeatures] = useState([]);
    const [current_features, setCurrentFeatures] = useState([]);
    const [need_fetch, setNeedFetch] = useState([]);
    const [flag, setFlag] = useState(0);

    useEffect(
        () => {
            need_fetch.length = 0;
            infeatures.length = 0;
            for(var k in current_plot_data){
                delete current_plot_data[k];
            }
            if (props.features) {
                for (let i=0;i<props.features.length;i++) {
                    if (! inArray(current_features, props.features[i]['value'])) {
                        need_fetch.push(props.features[i]['value']);
                        // console.log(current_features);
                        current_features.push(props.features[i]['value']);
                    } else {
                        current_plot_data[props.features[i]['value']] = plot_data[props.features[i]['value']]
                    }
                    // setInfeatures(infeatures => [...infeatures, props.features[i]['value']]);
                    infeatures.push(props.features[i]['value']);
                }
            }
            // console.log("==========infeatures===========")
            // console.log(infeatures);
            
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ features: need_fetch })
            };
            console.log(requestOptions);
            fetch("react_features_data", requestOptions).then(
                (res) => res.json().then(
                    (data) => {
                        if (data) {
                                    // return <Plotting mainid='main0' data={data[0]} feature={props.features[0]} />;
                            show_plot.push(data[0])
                            for (let i=0;i<data.length;i++) {
                                plot_data[need_fetch[i]] = data[i]
                                current_plot_data[need_fetch[i]] = data[i]
                            }
                        } else {
                            console.log("nooooo");
                        }
                        setFlag(flag + 1);
                        // console.log(current_plot_data);
                    }
                )
            );
        }, [props.features]);
    

    // return (<Plotting mainid='main0' data={plot_data} feature={infeatures} flag={flag} />);
    return (
        <div className='EchartsPlot'>
            {Object.keys(current_plot_data).map((f, idx) => (
                // <p>{f}</p>
                <Plotting mainid={f} data={plot_data[f]} feature={f} flag={flag} />
            ))}
        </div>
    );
    
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
                        text: feature_name + ' distribution'
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


