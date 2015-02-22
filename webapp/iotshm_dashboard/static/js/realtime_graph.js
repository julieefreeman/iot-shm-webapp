$(document).ready(function() {
    if ($("#real-time-chart").length) {
        $('#real-time-chart').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQuery
              }
          },
          title: {
              text: 'Live chart'
          },
          subtitle: {
              text: 'Irregular data in Highcharts JS'
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
                  text: 'Means nothing'
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
                name: 'Random data',
                data: []
            }]
      });
        real_interval = setInterval(executeRealTimeQuery, 1000)
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
      //data: $('a[id=active_building]').attr("value"),
      success: function(data){
          updateRealTimeChart(data);
        },
      error: function(data){
          $("#testing").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}
function updateRealTimeChart(json) {
    var index = 0;
    $.each(json, function (sensor, data) {
        //$("#testing").append("<h2>value: " + data['data'] + "</h2>");
        $.each(data['data'], function (key,value) {
            var chart = $('#real-time-chart').highcharts();
            var series = chart.series[index];
            var shift = series.data.length > 50;
            //$("#testing").append("<h2>time: " + value['time'] + "</h2>");
            //$("#testing").append("<h2>value: " + value['value'] + "</h2>");
            //$("#testing").append("<h2>shift: " + shift + "</h2>");
            chart.series[index].addPoint([value['time'],value['value']],true,shift)
        });
        index++;
    });
}