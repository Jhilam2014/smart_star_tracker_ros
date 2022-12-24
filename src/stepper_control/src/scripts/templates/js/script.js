$(document).ready(function() {
    $("#clock-img").hide();
    $("#anti-clock-img").hide();
    $("#c-button").click(function(){
        $("#clock-img").show();
        $("#anti-clock-img").hide();
      });
    $("#ac-button").click(function(){
        $("#clock-img").hide();
        $("#anti-clock-img").show();
      });


    $("button").click(function(){
        if($(this).attr('data-type') == 'plus'){
            var val = parseInt($('#input-text-speed').val()) + 10
            console.log(val);
            document.getElementById('input-text-speed').value=String(val) ; 
        }
        if($(this).attr('data-type') == 'minus'){
            var val = parseInt($('#input-text-speed').val()) - 10
            console.log(val);
            document.getElementById('input-text-speed').value=String(val) ; 
        }
    });

});