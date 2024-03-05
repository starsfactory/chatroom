document.addEventListener('DOMContentLoaded', function() {
    // 设置缩放级别，可以根据需要调整为其他值
    document.body.style.zoom = "99%";

});

var sumline;
var mainemotion;

var subemotion;
var subemotionkey;
var subemotionvalue;

var sumtimecount;

var emotion;
var emotionkey;
var emotionvalue;

var membercount;
var membercountkey;
var membercountvalue;

var sumtimesentencescount;

var sentences;
// var sentenceskey;
// var sentencesvalue;


// 柱状图1模块
console.log('request')
const roomid = sessionStorage.getItem('historyroomid')
const filename = sessionStorage.getItem('filename')
const url = `/visualize?roomid=${roomid}&filename=${filename}`;
fetch(url)
    .then(response => response.json())
    .then(data => {
        if(data.success){
            sumline = data.sumline;
            mainemotion = data.mainemotion;
            sumtimecount = data.sumtimecount;
            subemotion = data.subemotion;

            emotion = data.emotion;
            membercount = data.membercount;
            sumtimesentencescount = data.sumtimesentencescount;
            sentences = data.sentences;
            // 选择需要修改内容的元素
            const mainNumberElement = document.getElementById('mainnumber');
            const mainEmotionElement = document.getElementById('mainemotion');
            // 修改元素内容
            mainNumberElement.textContent = sumline;
            mainEmotionElement.textContent = mainemotion;

            subemotionkey = Object.keys(subemotion);
            subemotionvalue = Object.values(subemotion);

             emotionkey = Object.keys(emotion);
             emotionvalue = Object.values(emotion);

             membercountkey = Object.keys(membercount);
             membercountvalue = Object.values(membercount);

             // sentenceskey = Object.keys(sentences);
             // sentencesvalue = Object.values(sentences);

             // = Object.keys();
             // = Object.values();
            console.log(sumtimecount);
            console.log(sumtimesentencescount);
            // 实例化对象
            var myChart = echarts.init(document.querySelector(".bar .chart"));
            // 指定配置和数据
            var option = {
                color: ["#2f89cf"],
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: "shadow"
                    }
                },
                grid: {
                    left: "0%",
                    top: "10px",
                    right: "0%",
                    bottom: "4%",
                    containLabel: true
                },
                xAxis: [
                    {
                        type: "category",
                        data: subemotionkey,
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: "10"
                            },
                            rotate: 45
                        },
                        axisLine: {
                            show: false
                        },
                    }
                ],
                yAxis: [
                    {
                        type: "value",
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: "12"
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.1)"
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.1)"
                            }
                        }
                    }
                ],
                series: [
                    {
                        name: "直接访问",
                        type: "bar",
                        barWidth: "35%",
                        data: subemotionvalue,
                        itemStyle: {
                            barBorderRadius: 5
                        }
                    }
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);

            var myChart = echarts.init(document.querySelector(".line .chart"));
            var option = {
                color: ["#00f2f1"],
                tooltip: {
                  // 通过坐标轴来触发
                  trigger: "axis"
                },
                legend: {
                  // 距离容器10%
                  right: "10%",
                  // 修饰图例文字的颜色
                  textStyle: {
                    color: "#4c9bfd"
                  }
                  // 如果series 里面设置了name，此时图例组件的data可以省略
                },
                grid: {
                  top: "20%",
                  left: "3%",
                  right: "4%",
                  bottom: "3%",
                  show: true,
                  borderColor: "#012f4a",
                  containLabel: true
                },

                xAxis: {
                  type: "category",
                  boundaryGap: false,
                  data: [1, 2, 3, 4, 5],
                  // 去除刻度
                  axisTick: {
                    show: false
                  },
                  // 修饰刻度标签的颜色
                  axisLabel: {
                    color: "rgba(255,255,255,.7)"
                  },
                  // 去除x坐标轴的颜色
                  axisLine: {
                    show: false
                  }
                },
                yAxis: {
                  type: "value",
                  // 去除刻度
                  axisTick: {
                    show: false
                  },
                  // 修饰刻度标签的颜色
                  axisLabel: {
                    color: "rgba(255,255,255,.7)"
                  },
                  // 修改y轴分割线的颜色
                  splitLine: {
                    lineStyle: {
                      color: "#012f4a"
                    }
                  }
                },
                series: [
                  {
                    name: "消极占比",
                    type: "line",
                    stack: "总量",
                    // 是否让线条圆滑显示
                    smooth: true,
                    data: sumtimecount,
                  },
                ]
              };
            myChart.setOption(option);

            var myChart = echarts.init(document.querySelector(".pie .chart"));
            option = {
                tooltip: {
                  trigger: "item",
                  formatter: "{a} <br/>{b}: {c} ({d}%)",
                  position: function (p) {
                    //其中p为当前鼠标的位置
                    return [p[0] + 10, p[1] - 10];
                  }
                },
                legend: {
                  top: "90%",
                  itemWidth: 10,
                  itemHeight: 10,
                  data: emotionkey,
                  textStyle: {
                    color: "rgba(255,255,255,.5)",
                    fontSize: "12"
                  }
                },
                series: [
                  {
                    name: "情绪分布",
                    type: "pie",
                    center: ["50%", "42%"],
                    radius: ["40%", "60%"],
                    color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6","#F80000", "#888800"],
                    label: { show: false },
                    labelLine: { show: false },
                    data: [
                        { value: emotionvalue[0], name: emotionkey[0] },
                        { value: emotionvalue[1], name: emotionkey[1] },
                        { value: emotionvalue[2], name: emotionkey[2] },
                    ]
                  }
                ]
              };
            myChart.setOption(option);

            var myChart = echarts.init(document.querySelector(".bar1 .chart"));

            var titlename = membercountkey;
            var data = membercountvalue;
            var valdata = Array(data.length).fill(""); // 生成与 data 长度相同的空字符串数组
            var myColor = ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6", "#F80000", "#888800"];
            console.log(data);
            option = {
                //图标位置
                grid: {
                  top: "10%",
                  left: "22%",
                  bottom: "10%"
                },
                xAxis: {
                  show: false
                },
                yAxis: [
                  {
                    show: true,
                    data: titlename,
                    inverse: true,
                    axisLine: {
                      show: false
                    },
                    splitLine: {
                      show: false
                    },
                    axisTick: {
                      show: false
                    },
                    axisLabel: {
                      color: "#fff",

                      rich: {
                        lg: {
                          backgroundColor: "#339911",
                          color: "#fff",
                          borderRadius: 15,
                          // padding: 5,
                          align: "center",
                          width: 15,
                          height: 15
                        }
                      }
                    }
                  },
                  {
                    show: true,
                    inverse: true,
                    data: valdata,
                    axisLabel: {
                      textStyle: {
                        fontSize: 12,
                        color: "#fff"
                      }
                    }
                  }
                ],
                series: [
                  {
                    name: "条",
                    type: "bar",
                    yAxisIndex: 0,
                    data: data,
                    barCategoryGap: 50,
                    barWidth: 10,
                    itemStyle: {
                      normal: {
                        barBorderRadius: 20,
                        color: function (params) {
                          var num = myColor.length;
                          return myColor[params.dataIndex % num];
                        }
                      }
                    },
                    label: {
                      normal: {
                        show: true,
                        position: "inside",
                        formatter: "{c}%"
                      }
                    }
                  },
                  {
                    name: "框",
                    type: "bar",
                    yAxisIndex: 1,
                    barCategoryGap: 50,
                    data: Array(data.length).fill(100),
                    barWidth: 15,
                    itemStyle: {
                      normal: {
                        color: "none",
                        borderColor: "#00c1de",
                        borderWidth: 3,
                        barBorderRadius: 15
                      }
                    }
                  }
                ]
              };
            myChart.setOption(option);

            var myChart = echarts.init(document.querySelector(".line1 .chart"));
            option = {
                tooltip: {
                  trigger: "axis",
                  axisPointer: {
                    lineStyle: {
                      color: "#dddc6b"
                    }
                  }
                },
                legend: {
                  top: "0%",
                  textStyle: {
                    color: "rgba(255,255,255,.5)",
                    fontSize: "12"
                  }
                },
                grid: {
                  left: "10",
                  top: "30",
                  right: "10",
                  bottom: "10",
                  containLabel: true
                },

                xAxis: [
                  {
                    type: "category",
                    boundaryGap: false,
                    axisLabel: {
                      textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 12
                      }
                    },
                    axisLine: {
                      lineStyle: {
                        color: "rgba(255,255,255,.2)"
                      }
                    },

                    data: [1, 2, 3, 4, 5]
                  },
                  {
                    axisPointer: { show: false },
                    axisLine: { show: false },
                    position: "bottom",
                    offset: 20
                  }
                ],

                yAxis: [
                  {
                    type: "value",
                    axisTick: { show: false },
                    axisLine: {
                      lineStyle: {
                        color: "rgba(255,255,255,.1)"
                      }
                    },
                    axisLabel: {
                      textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 12
                      }
                    },

                    splitLine: {
                      lineStyle: {
                        color: "rgba(255,255,255,.1)"
                      }
                    }
                  }
                ],
                series: [
                  {
                    name: "总浏览量",
                    type: "line",
                    smooth: true,
                    symbol: "circle",
                    symbolSize: 5,
                    showSymbol: false,
                    lineStyle: {
                      normal: {
                        color: "#0184d5",
                        width: 2
                      }
                    },
                    areaStyle: {
                      normal: {
                        color: new echarts.graphic.LinearGradient(
                          0,
                          0,
                          0,
                          1,
                          [
                            {
                              offset: 0,
                              color: "rgba(1, 132, 213, 0.4)"
                            },
                            {
                              offset: 0.8,
                              color: "rgba(1, 132, 213, 0.1)"
                            }
                          ],
                          false
                        ),
                        shadowColor: "rgba(0, 0, 0, 0.1)"
                      }
                    },
                    itemStyle: {
                      normal: {
                        color: "#0184d5",
                        borderColor: "rgba(221, 220, 107, .1)",
                        borderWidth: 12
                      }
                    },
                    data: sumtimesentencescount
                  },
                ]
              };
            myChart.setOption(option);

            var myChart = echarts.init(document.querySelector(".pie1  .chart"));
            var option = {
                legend: {
                  top: "90%",
                  itemWidth: 10,
                  itemHeight: 10,
                  textStyle: {
                    color: "rgba(255,255,255,.5)",
                    fontSize: "12"
                  }
                },
                tooltip: {
                  trigger: "item",
                  formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                // 注意颜色写的位置
                color: [
                  "#006cff",
                  "#60cda0",
                  "#ed8884",
                  "#ff9f7f",
                  "#0096ff",
                ],
                series: [
                  {
                    name: "点位统计",
                    type: "pie",
                    // 如果radius是百分比则必须加引号
                    radius: ["10%", "70%"],
                    center: ["50%", "42%"],
                    roseType: "radius",
                    data: [
                      { value: sentences[0], name: "0~10" },
                      { value: sentences[1], name: "11~15" },
                      { value: sentences[2], name: "16~20" },
                      { value: sentences[3], name: "21~25" },
                      { value: sentences[4], name: "25~30" },
                    ],
                    // 修饰饼形图文字相关的样式 label对象
                    label: {
                      fontSize: 10
                    },
                    // 修饰引导线样式
                    labelLine: {
                      // 连接到图形的线长度
                      length: 10,
                      // 连接到文字的线长度
                      length2: 10
                    }
                  }
                ]
              };

              // 3. 配置项和数据给我们的实例化对象
            myChart.setOption(option);

        }
    });

