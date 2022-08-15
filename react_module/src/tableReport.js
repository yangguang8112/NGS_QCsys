import React, { useState, useEffect, Component } from 'react';
import './App.css';
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
import "echarts-wordcloud";

import { ScatterChart } from 'echarts/charts';
echarts.use([ScatterChart]);




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
                        // console.log(data);
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



function WordCloud() {
    const [flask_data, setdata] = useState([]);

    useEffect(
        () => {
            fetch("get_wordcloud_data").then(
                (res) => res.json().then(
                    (data) => {
                        console.log(data);
                        setdata(data);
                    }
                )
            );
        }, []);

    
    
    
    return (
        <div>
            <div className='WordCloud'>
            <Plotting_wordcloud data={flask_data}/>
            </div>
        </div>
    );
}

function Plotting_wordcloud(props) {
    useEffect(
        () => {
            // console.log(props.data)
            if (props.data) {
                var chart = echarts.init(document.getElementById('wordcloud'));
                chart.setOption({
                    series: [{
                        type: 'wordCloud',

                        // The shape of the "cloud" to draw. Can be any polar equation represented as a
                        // callback function, or a keyword present. Available presents are circle (default),
                        // cardioid (apple or heart shape curve, the most known polar equation), diamond (
                        // alias of square), triangle-forward, triangle, (alias of triangle-upright, pentagon, and star.

                        shape: 'circle',

                        // Keep aspect ratio of maskImage or 1:1 for shapes
                        // This option is supported from echarts-wordcloud@2.1.0
                        keepAspect: false,

                        // A silhouette image which the white area will be excluded from drawing texts.
                        // The shape option will continue to apply as the shape of the cloud to grow.

                        // maskImage: maskImage,

                        // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                        // Default to be put in the center and has 75% x 80% size.

                        left: 'center',
                        top: 'center',
                        width: '70%',
                        height: '80%',
                        right: null,
                        bottom: null,

                        // Text size range which the value in data will be mapped to.
                        // Default to have minimum 12px and maximum 60px size.

                        sizeRange: [12, 60],

                        // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45

                        rotationRange: [-90, 90],
                        rotationStep: 45,

                        // size of the grid in pixels for marking the availability of the canvas
                        // the larger the grid size, the bigger the gap between words.

                        gridSize: 8,

                        // set to true to allow word being draw partly outside of the canvas.
                        // Allow word bigger than the size of the canvas to be drawn
                        drawOutOfBound: false,

                        // If perform layout animation.
                        // NOTE disable it will lead to UI blocking when there is lots of words.
                        layoutAnimation: true,

                        // Global text style
                        textStyle: {
                            fontFamily: 'sans-serif',
                            fontWeight: 'bold',
                            // Color can be a callback function or a color string
                            color: function () {
                                // Random color
                                return 'rgb(' + [
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160)
                                ].join(',') + ')';
                            }
                        },
                        emphasis: {
                            focus: 'self',

                            textStyle: {
                                textShadowBlur: 10,
                                textShadowColor: '#333'
                            }
                        },

                        // Data is an array. Each array item must have name and value property.
                        data: props.data
                    }]
                });
            }
        }, [props.data]
    );

    return (
        <div id="wordcloud" style={{width: '100%', height: 400}}></div>
    );
}


function Sample_date() {
    const [flask_data, setdata] = useState();

    useEffect(() => {
        fetch("get_sample_date").then(
            (res) => res.json().then(
                (data) => {
                    // console.log(data);
                    setdata(data);
                }
            ) 
        )
    }, [])

    return (
        <Plotting_bars data={flask_data} />
    );
}


function Plotting_bars(props) {
    useEffect(() => {
        if (props.data) {
            // console.log(props.data);
            var accepted_count = props.data["yes_count"];
            var failed_count = props.data["no_count"];
            var all_count = props.data["all_count"];
            var date_list = props.data["date_list"];
            var max_count = props.data["max_count"];
            // var min_count = props.date["min_count"];
            var min_count = 100;
            var chart = echarts.init(document.getElementById('barline'));
            chart.setOption({
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                      type: 'cross',
                      crossStyle: {
                        color: '#999'
                      }
                    }
                  },
                  toolbox: {
                    feature: {
                      dataView: { show: true, readOnly: false },
                      magicType: { show: true, type: ['line', 'bar'] },
                      restore: { show: true },
                      saveAsImage: { show: true }
                    }
                  },
                  legend: {
                    // data: ['Evaporation', 'Precipitation', 'Temperature']
                    data: ['Accepted', 'Failed', 'All']
                  },
                  xAxis: [
                    {
                      type: 'category',
                      data: date_list,
                      axisPointer: {
                        type: 'shadow'
                      }
                    }
                  ],
                  yAxis: [
                    {
                      type: 'value',
                      name: 'Sample nums',
                      min: min_count,
                      max: max_count,
                      interval: parseInt((max_count-min_count)/10),
                      axisLabel: {
                        formatter: '{value}'
                      }
                    },
                    {
                      type: 'value',
                      name: 'All',
                      min: min_count,
                      max: max_count,
                      interval: parseInt((max_count-min_count)/10),
                      axisLabel: {
                        formatter: '{value}'
                      }
                    }
                  ],
                  series: [
                    {
                      name: 'Accepted',
                      type: 'bar',
                      tooltip: {
                        valueFormatter: function (value) {
                          return value + ' samples';
                        }
                      },
                      data: accepted_count
                    },
                    {
                      name: 'Failed',
                      type: 'bar',
                      tooltip: {
                        valueFormatter: function (value) {
                          return value + ' samples';
                        }
                      },
                      data: failed_count
                    },
                    {
                      name: 'All',
                      type: 'line',
                      yAxisIndex: 1,
                      tooltip: {
                        valueFormatter: function (value) {
                          return value + ' samples';
                        }
                      },
                      data: all_count
                    }
                  ]
            })
        }
    }, [props.data]);

    return (
        <div id="barline" style={{width: '100%', height: 400}}></div>
    )
}

function DotPlotData() {
    const [flask_data, setdata] = useState();

    useEffect(() => {
        fetch('get_dot_data').then(
            (res) => res.json().then(
                (data) => {
                    console.log(data);
                    setdata(data);
                }
            )
        )
    }, []);

    return (
        <Plotting_dot data={flask_data} />
    );
}

function Plotting_dot(props) {
    useEffect(() => {
        if(props.data) {
            var good_coord = props.data['good_coord'];
            var bad_coord = props.data['bad_coord'];
            console.log(bad_coord.length);
            var chartDom = document.getElementById('tsne');
            var myChart = echarts.init(chartDom);
            var option;

            option = {
            legend: {
            data: [
                {name: "Accepted"},
                {name: "Failed"}
            ]
            },
            xAxis: {},
            yAxis: {},
            series: [
                {
                name: "Accepted",
                symbolSize: 5,
                data: good_coord,
                type: 'scatter'
                },
                {
                name: "Failed",
                symbolSize: 8,
                data: bad_coord,
                type: 'scatter'
                },
            ]
            };

            option && myChart.setOption(option);
        }
    }, [props.data]);

    return (
        <div id="tsne" style={{width: '100%', height:400}}></div>
    );
}


export default function ReportPage() {
    return (
        <div>
            <div id="container">
                <div id='left'>
                    <DistrSelect />
                </div>
                <div id='right'>
                    <DotPlotData />
                </div>
                {/* <div id='right'>
                    <WordCloud />
                </div> */}
            </div>
            <div id='container2'>
                
                <div id='right2'>
                    <Sample_date />
                </div>
            </div>
        </div>
    )
}


