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
              type: 'datetime',
              dateTimeLabelFormats: { // don't display the dummy year
                  month: '%e. %b',
                  year: '%b'
              },
              title: {
                  text: 'Date'
              }
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0
          },
          tooltip: {
              headerFormat: '<b>{series.name}</b><br>',
              pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
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
              type: 'datetime',
              dateTimeLabelFormats: { // don't display the dummy year
                  month: '%e. %b',
                  year: '%b'
              },
              title: {
                  text: 'Date'
              }
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0
          },
          tooltip: {
              headerFormat: '<b>{series.name}</b><br>',
              pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
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
              text: 'Y Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent results for this building'
          },
          xAxis: {
              type: 'datetime',
              dateTimeLabelFormats: { // don't display the dummy year
                  month: '%e. %b',
                  year: '%b'
              },
              title: {
                  text: 'Date'
              }
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0
          },
          tooltip: {
              headerFormat: '<b>{series.name}</b><br>',
              pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
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
      //data: $('a[id=active_building]').attr("value"),
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
    $.each(json, function (sensor, data) {
        //$("#testing").append("<h2>value: " + data['data'] + "</h2>");
        $.each(data['data'], function (key,value) {
            var chart = $('#real-time-chart-x').highcharts();
            var series = chart.series[index];
            var shift = series.data.length > 50;
            //$("#debugging").append("<h2>time: " + value['time'] + "</h2>");
            //$("#debugging").append("<h2>value: " + value['value'] + "</h2>");
            //$("#debugging").append("<h2>shift: " + shift + "</h2>");
            chart.series[index].addPoint([value['time'],value['value']],true,shift)
        });
        index++;
    });
}

function executeRealTimeQueryY() {
  $.ajax({
      url: '/iotshm/real_time_ajax_y/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      //data: $('a[id=active_building]').attr("value"),
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
        //$("#testing").append("<h2>value: " + data['data'] + "</h2>");
        $.each(data['data'], function (key,value) {
            var chart = $('#real-time-chart-y').highcharts();
            var series = chart.series[index];
            var shift = series.data.length > 50;
            //$("#debugging").append("<h2>time: " + value['time'] + "</h2>");
            //$("#debugging").append("<h2>value: " + value['value'] + "</h2>");
            //$("#debugging").append("<h2>shift: " + shift + "</h2>");
            chart.series[index].addPoint([value['time'],value['value']],true,shift)
        });
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
        //$("#testing").append("<h2>value: " + data['data'] + "</h2>");
        $.each(data['data'], function (key,value) {
            var chart = $('#real-time-chart-z').highcharts();
            var series = chart.series[index];
            var shift = series.data.length > 50;
            //$("#debugging").append("<h2>time: " + value['time'] + "</h2>");
            //$("#debugging").append("<h2>value: " + value['value'] + "</h2>");
            //$("#debugging").append("<h2>shift: " + shift + "</h2>");
            chart.series[index].addPoint([value['time'],value['value']],true,shift)
        });
        index++;
    });
}