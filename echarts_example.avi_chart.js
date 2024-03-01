echarts
    .init(document.getElementById('avi_chart'))
    .setOption({
        title: {
            text: 'A vs. I',
        },
        xAxis: {
            type: 'value',
            name: 'Instability (I)',
            nameLocation: 'middle',
            nameGap: 25,
        },
        yAxis: {
            type: 'value',
            name: 'Abstractness (A)',
            nameLocation: 'middle',
            nameGap: 25,
        },
        series: [
            {
                type: 'line',
                lineStyle: {
                    color: '#aaa',
                    type: 'dotted',
                    opacity: 0.3,
                },
                data: [
                    [ 0, 1 ],
                    [ 1, 0 ],
                ],
            },
            {
                name: 'A vs. I',
                type: 'scatter',
                itemStyle: {
                    color: '#39f',
                },
                data: [
                    { value: [ 0.21, 0.73 ], name: 'com.jeantessier.classreader' },
                    { value: [ 0.98, 0.08 ], name: 'com.jeantessier.classreader.impl' },
                    { value: [ 0.54, 0.36 ], name: 'com.jeantessier.commandline' },
                    { value: [ 0.76, 0.22 ], name: 'com.jeantessier.dependency' },
                    { value: [ 0.81, 0.00 ], name: 'com.jeantessier.dependencyfinder' },
                    { value: [ 1.00, 0.08 ], name: 'com.jeantessier.dependencyfinder.ant' },
                    { value: [ 1.00, 0.17 ], name: 'com.jeantessier.dependencyfinder.cli' },
                    { value: [ 1.00, 0.00 ], name: 'com.jeantessier.dependencyfinder.gui' },
                    { value: [ 0.90, 0.30 ], name: 'com.jeantessier.diff' },
                    { value: [ 0.90, 0.22 ], name: 'com.jeantessier.metrics' },
                    { value: [ 0.75, 0.00 ], name: 'com.jeantessier.text' },
                ],
            },
        ],
    })
