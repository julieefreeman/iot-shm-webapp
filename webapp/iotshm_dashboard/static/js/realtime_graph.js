$(document).ready(function() {
    if (!$("#xcollapse").hasClass('collapsed')) {
        $('#real-time-chart').highcharts({
            chart: {
                type: 'spline',
                events: {
                load: executeRealTimeQuery
                }
            },
            title: {
                text: 'Magnitude vs Time'
            },
            subtitle: {
                text: 'Most recent readings for this building'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 5
            },
            yAxis: {
                title: {
                    text: 'Magnitude'
                },
                min: 0,
                max: 170
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                    Highcharts.numberFormat(this.y, 2);
                }
            },
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        states: {
                            hover: {
                                enabled: true,
                                radius: 3
                            }
                        }
                    }
                }
            },
            series: []
      });
        var real_interval = setInterval(executeRealTimeQuery, 1000);
    }
    else {
        clearInterval(real_interval);
    }
});

function executeRealTimeQuery() {
  $.ajax({
      url: '/iotshm/real_time_ajax/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChart(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}

function updateRealTimeChart(json) {
    var index = 0;
    var chart = $('#real-time-chart').highcharts();
    $.each(json, function (sensor, data) {
        // $("#debugging").append("<h2>data: "+data+"</h2>");
        var chart = $('#real-time-chart').highcharts();
        var series = chart.series[index];
        var shift = false;
        if (series!=null) {
            shift = series.data.length > 500;
        }
        else{
            chart.addSeries({
                name: sensor,
                data: data
            });
        }
        data.forEach(function(d) {
            chart.series[index].addPoint([d[0],d[1]],true,shift);
        });
        //$.each(data['data'], function (key,value) {
        //    $("#debugging").append("<h2>key: "+key+"</h2>");
        //    $("#debugging").append("<h2>value: "+value+"</h2>");
        //    var chart = $('#real-time-chart').highcharts();
        //    var series = chart.series[index];
        //    var shift = series.data.length > 50;
        //    chart.series[index].addPoint(value,true,shift);
        //});
        index++;
    });
}