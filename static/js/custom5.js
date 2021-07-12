/*global jQuery:false */
jQuery(document).ready(function($) {

   
    //esto es para mostrar y cargar el select de especie y luego el de raza en Agregar Mascota
    $("#addraza").change(function() {
        var parametros = "id=" + $("#addraza").val();
        $.ajax({
            data: parametros,
            url: '/especie',
            type: 'post',
            beforeSend: function() {

            },
            success: function(especie) {

                // $("#raza").html(raza);
                $("#espe").empty();
                for (var i = 0; i < especie.length; i++) {
                    $("#espe").append(
                        $("<option> </option>")
                        .attr("value", especie[i][0])
                        .text(especie[i][1])
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
        var parametros = "especie=" + $("#descrip").val();
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
                $("#raza2").empty();
                for (var i = 0; i < raza1.length; i++) {
                    $("#raza2").append(
                        $("<option> </option>")
                        .attr("value", raza1[i][0])
                        .text(raza1[i][1])
                    )
                };
                endfor
            },
        })
    })

});

 