var score_bar = echarts.init(document.getElementById("score_bar"));
var bar_option = {
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
        dataView: {show: true, readOnly: false},
        magicType: {show: true, type: ['line', 'bar']},
        restore: {show: true},
        saveAsImage: {show: true}
    }
},
  title: {
    text: "作业成绩分布",
    left: "left",
    textStyle: {
      color: "grey"
    }
  },
  xAxis: {
    type: "category",
    data: ["60以下", "60-69", "70-79", "80-89", "90-100"],
    axisPointer: {
      type: 'shadow'
  }
  },
  yAxis: [{
    type: "value",
    name: "人数"
  },
  {
      type: 'value',
      name: '平均分'
  }],
  series: [
    {
      name: "人数",
      data: [5,10,25,15,10],
      type: "bar"
    },
    {
      name: "区间平均分",
      yAxisIndex: 1,
      data: [58,66,78,85,91],
      type: "line"
    }
  ]
};
score_bar.setOption(bar_option);

var sentiment = echarts.init(document.getElementById("sentiment"));
var sentiment_option = {
    title: {
      text: "评论区情感",
      left: "left",
      top: 20,
      textStyle: {
        color: "grey"
      }
    },
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: false
            },
            saveAsImage: {
                pixelRatio: 2
            }
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        bottom: 90
    },
    dataZoom: [{
        type: 'inside'
    }, {
        type: 'slider'
    }],
    xAxis: {
        data: ['负面','中性','正面'],
        silent: false,
        splitLine: {
            show: false
        },
        splitArea: {
            show: false
        }
    },
    yAxis: {
        splitArea: {
            show: false
        }
    },
    series: [{
        type: 'bar',
        data: [21,34,11],
        
    }]
};
sentiment.setOption(sentiment_option);

var key_word = echarts.init(document.getElementById("key_word"));
var keyword_option = {
  title: {
    text: "评论区关键词",
    left: "left",
    top: 20,
    textStyle: {
      color: "grey"
    }
  },
  series: [
    {
      type: "wordCloud",
      rotationRange:[-45,0,45,90],
      textStyle:{
        normal:{
            color: function(){
                return 'rgb('+Math.round(Math.random()*255)+','+
                Math.round(Math.random()*255)+','+Math.round(Math.random()*255)+')'
            }
        }
      },
      data: [{'name':'难','value':'120'}, {'name':'C++','value':'200'}, {'name':'通过了','value':'100'}, 
      {'name':'求解析','value':'102'}, {'name':'呵呵呵呵','value':'100'}, {'name':'java','value':'220'}, 
      {'name':'作业','value':'120'},{'name':'bug','value':'210'},{'name':'python','value':'250'},
      {'name':'大佬','value':'150'},{'name':'循环','value':'190'},{'name':'编译错误','value':'160'},
      {'name':'好坑','value':'137'},{'name':'编程','value':'141'},{'name':'类','value':'125'}]
    }
  ]
};
key_word.setOption(keyword_option);

var score_pie = echarts.init(document.getElementById("score_pie"));
pie_option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    title: {
        text: "提交次数统计",
        left: "left",
        top: 20,
        textStyle: {
            color: "grey"
        }
    },
    series: [
        {
            name: '提交次数',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '20',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [
                { value: 1, name: "1次通过" },
                { value: 3, name: "2次尝试后通过" },
                { value: 2, name: "3-5次尝试后通过" },
                { value: 1, name: "6-10次尝试后通过" },
                { value: 1, name: "10次以上" }
            ]
        }
    ]
};
score_pie.setOption(pie_option);


function get_score_data(){
  var hwprobInput = $('input[name="hwprob_id"]');
  var hwprob_id = hwprobInput.val();
  zlajax.post({
    url:"/homework/getscore/"+String(hwprob_id),
    success: function(data){
      bar_option.series[0].data=data['count']
      bar_option.series[1].data=data['avg']
      score_bar.setOption(bar_option)

      pie_option.series[0].data = data['submit']
      score_pie.setOption(pie_option)
    }
  })
}
get_score_data()


