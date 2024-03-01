echarts
    .init(document.getElementById('d_chart'))
    .setOption({
        title: {
            text: 'D\'',
        },
        xAxis: {
            type: 'category',
            show: false,
        },
        yAxis: {
            type: 'value',
            name: 'D\'',
            nameLocation: 'middle',
            nameGap: 25,
            min: -1,
            max: 1,
        },
        series: [
            {
                type: 'line',
                data: [
                    { value: -0.25, name: 'com.jeantessier.text' },
                    { value: -0.19, name: 'com.jeantessier.dependencyfinder' },
                    { value: -0.10, name: 'com.jeantessier.commandline' },
                    { value: -0.06, name: 'com.jeantessier.classreader' },
                    { value: -0.02, name: 'com.jeantessier.dependency' },
                    { value:  0.00, name: 'com.jeantessier.dependencyfinder.gui' },
                    { value:  0.06, name: 'com.jeantessier.classreader.impl' },
                    { value:  0.08, name: 'com.jeantessier.dependencyfinder.ant' },
                    { value:  0.12, name: 'com.jeantessier.metrics' },
                    { value:  0.17, name: 'com.jeantessier.dependencyfinder.cli' },
                    { value:  0.20, name: 'com.jeantessier.diff' },
                ],
            },
        ],
    })
