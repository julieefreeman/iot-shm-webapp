$(document).ready(function() {
    if (!$("#xcollapse").hasClass('collapsed')) {
        $('#real-time-chart-x').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryX
              }
          },
          title: {
              text: 'X Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent results for this building'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              }
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: [{
                name: 'Frequency',
                data: []
            }]
      });
        real_interval_x = setInterval(executeRealTimeQueryX, 1000);
    }
    else {
        clearInterval(real_interval_x);
    }
    if (!$("#ycollapse").hasClass('collapsed')) {
        $('#real-time-chart-y').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryY
              }
          },
          title: {
              text: 'Y Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent results for this building'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              }
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: [{
                name: 'Frequency',
                data: []
            }]
      });
        real_interval_y = setInterval(executeRealTimeQueryY, 1000);
    }
    else {
        clearInterval(real_interval_y);
    }
    if (!$("#zcollapse").hasClass('collapsed')) {
        $('#real-time-chart-z').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryY
              }
          },
          title: {
              text: 'Z Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent results for this building'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              }
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: [{
                name: 'Frequency',
                data: []
            }]
      });
        real_interval_z = setInterval(executeRealTimeQueryZ, 1000);
    }
    else {
        clearInterval(real_interval_z);
    }
});

function executeRealTimeQueryX() {
  $.ajax({
      url: '/iotshm/real_time_ajax_x/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChartX(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}

function updateRealTimeChartX(json) {
    var index = 0;
    chart.setTitle({text: json["time"]});
    $.each(json["data"], function (sensor, data) {
        var chart = $('#real-time-chart-x').highcharts();
        chart.series[index].setData(data['x_data']);
        //$.each(data['x_data'], function (key,value) {
        //    var chart = $('#real-time-chart-x').highcharts();
        //    var series = chart.series[index];
        //    var shift = series.data.length > 50;
        //    chart.series[index].addPoint([value['frequency'],value['magnitude']],true,shift)
        //});
        index++;
    });
}

function executeRealTimeQueryY() {
  $.ajax({
      url: '/iotshm/real_time_ajax_y/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChartY(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}
function updateRealTimeChartY(json) {
    var index = 0;
    $.each(json, function (sensor, data) {
        var chart = $('#real-time-chart-y').highcharts();
        chart.series[index].setData(data['y_data']);
        //$.each(data['y_data'], function (key,value) {
        //    var chart = $('#real-time-chart-y').highcharts();
        //    var series = chart.series[index];
        //    var shift = series.data.length > 50;
        //    chart.series[index].addPoint([value['frequency'],value['magnitude']],true,shift)
        //});
        index++;
    });
}

function executeRealTimeQueryZ() {
  $.ajax({
      url: '/iotshm/real_time_ajax_z/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      //data: $('a[id=active_building]').attr("value"),
      success: function(data){
          updateRealTimeChartZ(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}
function updateRealTimeChartZ(json) {
    var index = 0;
    $.each(json, function (sensor, data) {
        var chart = $('#real-time-chart-z').highcharts();
        chart.series[index].setData(data['z_data']);
        //$.each(data['z_data'], function (key,value) {
        //    var chart = $('#real-time-chart-z').highcharts();
        //    var series = chart.series[index];
        //    var shift = series.data.length > 50;
        //    chart.series[index].addPoint([value['frequency'],value['magnitude']],true,shift)
        //});
        index++;
    });
}