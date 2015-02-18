var x = 0;
$(document).ready(function() {
    // run the first time; all subsequent calls will take care of themselves
    if ($("#myChart").length) {
        //interval = setInterval(function() {executeQuery(document.getElementById("myChart"));}, 1000);
        interval = setInterval(executeQuery, 1000, document)
    }
    else {
        clearInterval(interval);
    }
    
//$('#thisbutton').click( function(e){
//    var c = document.getElementById("myChart");
//    var ctx = c.getContext("2d");
//    ctx.fillStyle = "#FF0000";
//    ctx.fillRect(0,0,250,150);
//});
});

function executeQuery(document) {
  $.ajax({
      url: '/iotshm/real_time_ajax/',
      data: $('a[id=active_building]').attr("value"),
      success: function(data) {
          //var dataset = {
          //    'id': 'temp-data',
          //    'label': 'Temperature',
          //    'units': 'C',
          //    'list': [{'date': '2013-09-26', 'value': 26}, {'date': '2013-09-27', 'value': 23}] };
          //var svg = d3.select('svg#myChart');
          //var svg = d3.select('#myChart');
          //var plot = chart.timeSeries()
          //    .width(800)
          //    .height(300);
          //svg.datum([data]).call(plot);
            var c = document.getElementById("myChart");
            var ctx = c.getContext("2d");
            ctx.fillStyle = "#FF0000";
            ctx.fillRect(0,0,250,150);
            //ctx.moveTo(x,x);
            //ctx.lineTo(x+5,x+5);
            //ctx.stroke();
          x+=5;
    }
  });
}