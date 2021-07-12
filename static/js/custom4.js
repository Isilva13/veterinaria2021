/*global jQuery:false */
jQuery(document).ready(function($) {

   
    //esto es para mostrar y cargar el select de especie y luego el de raza en Agregar Mascota
    $("#descripcioncategoria").change(function() {
        var parametros = "id=" + $("#descripcioncategoria").val();
        $.ajax({
            data: parametros,
            url: '/categoria',
            type: 'post',
            beforeSend: function() {

            },
            success: function(radio) {

                // $("#raza").html(raza);
                $("#reditar").empty();
                for (var i = 0; i < radio.length; i++) {
                    $("#reditar").append(
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
        $( function() {
            $("#descripcioncategoria").change( function() {
                if ($(this).val() === "P") {
                    $("#id_input").prop("hidden", false);
                    
                    
                } else {
                    $("#id_input").prop("hidden", true);
                    
                    
                }
                
                    
                
            });
        });

        $( function() {
            $("#descripcioncategoria").change( function() {
                if ($(this).val() === "P") {
                    $("#id_input").prop("required", true);
                    
                    
                } else {
                    $("#id_input").prop("required", false);
                    
                    
                }
                
                    
                
            });
        });
        $( function() {
            $("#descripcioncategoria").change( function() {
                if ($(this).val() === "P") {
                    $("#id_label").prop("hidden", false);
                   
                    
                } else {
                    $("#id_label").prop("hidden", true);
                    
                    
                }
                
                    
                
            });
        });
                
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

 