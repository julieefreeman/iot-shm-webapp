$(document).ready(function() {
    //if(document.getElementById("health")!=null) {
    //if($('a[id=active_building]')!=null){
    health_interval = setInterval(executeHealthQuery, 1000);
    //}
    //else{
    //    health_interval = setInterval(executeHealthQuery9, 500);
    //}

    //}
    //else{
    //    clearInterval(health_interval);
    //}
});

function executeHealthQuery() {
  $.ajax({
      url: '/iotshm/health/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      success: function(data){
          if (data['healthy'] == true) {
              document.getElementById("health").innerHTML = "Healthy";
              document.getElementById("health").style.backgroundColor = "limegreen";
          }
          else if (data['healthy'] == false) {
              document.getElementById("health").innerHTML = "Unhealthy";
              document.getElementById("health").style.backgroundColor = "darkred";
          }
          else {
              document.getElementById("health").innerHTML = "N/A";
              document.getElementById("health").style.backgroundColor = "gray";
          }
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}