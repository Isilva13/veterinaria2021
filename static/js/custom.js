/*global jQuery:false */
jQuery(document).ready(function($) {

   
    //esto es para mostrar y cargar el select de especie y luego el de raza en Agregar Mascota
    $("#descripcion").change(function() {
        var parametros = "id=" + $("#descripcion").val();
        $.ajax({
            data: parametros,
            url: '/raza',
            type: 'post',
            beforeSend: function() {

            },
            success: function(raza1) {

                // $("#raza").html(raza);
                $("#raza3").empty();
                for (var i = 0; i < raza1.length; i++) {
                    $("#raza3").append(
                        $("<option> </option>")
                        .attr("value", raza1[i][0])
                        .text(raza1[i][1])
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
                $("#raza3").empty();
                for (var i = 0; i < raza1.length; i++) {
                    $("#raza3").append(
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

 