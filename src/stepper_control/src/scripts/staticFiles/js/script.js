$(document).ready(function() {
    $("#clock-img").show();
    $("#anti-clock-img").hide();
    document.getElementById('direction').value=0
    $("#c-button").click(function(){
        $("#clock-img").show();
        $("#anti-clock-img").hide();
        document.getElementById('direction').value=0
      });
    $("#ac-button").click(function(){
        $("#clock-img").hide();
        $("#anti-clock-img").show();
        document.getElementById('direction').value=1
      });


    $("button").click(function(){
        if($(this).attr('data-type') == 'plus'){
            var val = parseInt($('#input-text-'+$(this).attr('type-val')).val()) + 10
            console.log(val);
            document.getElementById('input-text-'+$(this).attr('type-val')).value=String(val) ; 
        }
        if($(this).attr('data-type') == 'minus'){
            var val = parseInt($('#input-text-'+$(this).attr('type-val')).val()) - 10
            console.log(val);
            document.getElementById('input-text-'+$(this).attr('type-val')).value=String(val) ; 
        }
    });


    $("#run_button").click(function(){
        

        var get_data = {
            'dif' : $("#textAreaExample").attr('value'),
            'speed': $("#input-text-speed").val(),
            'direction': document.getElementById('direction').value
        }

        var obj =  JSON.stringify(get_data);

        var saveData = $.ajax({
            type: 'POST',
            url: "/run",
            contentType: 'application/json;',
            data: obj,
            success: function(resultData) { 
                console.log(resultData);
                dt = JSON.stringify(resultData['data'], null, 4)
                document.getElementById('textAreaExample').textContent = dt; 
                document.getElementById('textAreaExample').setAttribute('value',JSON.stringify(resultData['data'])); 
            
            }
      });
      saveData.error(function() { alert("Something went wrong"); });
      });

});