$(document).ready(function(){
    $( "#slider-range" ).slider({
        range: true,
        min: {{services.low_time}},
        max: {{services.high_time}},
        values: [ 6, 10 ],
        slide: function( event, ui ) {
          $( "#id_start_time" ).val(  ui.values[ 0 ] );
          $( "#id_end_time" ).val(  ui.values[ 1 ] );
        }
      });
});