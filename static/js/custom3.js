/*global jQuery:false */
jQuery(document).ready(function($) {

   
    //esto es para mostrar y cargar el select de especie y luego el de raza en Agregar Mascota
    $("#categoria").change(function() {
        var parametros = "id=" + $("#categoria").val();
        $.ajax({
            data: parametros,
            url: '/categoria',
            type: 'post',
            beforeSend: function() {

            },
            success: function(radio) {

                // $("#raza").html(raza);
                $("#r").empty();
                for (var i = 0; i < radio.length; i++) {
                    $("#r").append(
                        $("<option> </option>")
                        .attr("value", radio[i])
                        .text(radio[i])
                    )
                };
                endfor
            },
        })
    })
    function nobackbutton(){
        	
           window.location.hash="no-back-button";
        	
           window.location.hash="Again-No-back-button" //chrome
        	
           window.onhashchange=function(){window.location.hash="no-back-button";}
        	
        }

    //esto es para cargar el select de  raza 
    $("#cargarRaza").click(function() {
        alert("esto no funciona")
        var parametros = "especie=" + $("#categoria").val();
        "raza=" + $("#nuevaRaza").val();
        //  console.log(especie)
        //  console.log(raza)
        $.ajax({
            data: parametros,
            url: '/add_especie_raza',
            type: 'post',
            beforeSend: function() {

            },
            success: function(raza1) {

                // $("#raza").html(raza);
                $("#r").empty();
                for (var i = 0; i < radio.length; i++) {
                    $("#r").append(
                        $("<option> </option>")
                        .attr("value", radio[i][0])
                        .text(radio[i][1])
                    )
                };
                endfor
            },
        })
    })

});

 