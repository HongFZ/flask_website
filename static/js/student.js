
var calendar = echarts.init(document.getElementById("calendar"));
calendar_option = {
    title: {
        text: '活跃度'
    },
    visualMap: {
        show: false,
        min: 0,
        max: 10000
    },
    calendar: {
        range: '2020'
    },
    series: {
        type: 'heatmap',
        coordinateSystem: 'calendar',
        data: [['2020-01-01',100],['2020-2-14',150],['2020-3-10',50],['2020-3-16',550],['2020-4-1',250]]
    }
};
calendar.setOption(calendar_option);


var score = echarts.init(document.getElementById("score"));
score_option = {
    title: {
        text: '作业成绩趋势'
    },
    xAxis: {
        type: 'category',
        data: ['作业1', '作业2', '作业3', '作业4', '作业5']
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [89,91,92,92,96],
        type: 'line',
        smooth: true
    }]
};
score.setOption(score_option);


var radar = echarts.init(document.getElementById("radar"));
radar_option = {
    title: {
        text: '基础雷达图'
    },
    tooltip: {},
    radar: {
        name: {
            textStyle: {
                color: '#fff',
                backgroundColor: '#999',
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        indicator: [
            { name: '正确率', max: 100},
            { name: '程序耗时', max: 30000},
            { name: '程序占用内存', max: 38000},
            { name: '完成题目数', max: 1000},
            { name: '使用语言数', max: 10}
        ]
    },
    series: [{
        type: 'radar',
        data: [
            {
                value: [91,10000,20000,100,3]
            }
        ]
    }]
};
radar.setOption(radar_option);
