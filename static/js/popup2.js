var btnAbrirPopup2 = document.getElementById('btn-abrir-popup2'),
	overlay2 = document.getElementById('overlay2'),
	popup2 = document.getElementById('popup2'),
	btnCerrarPopup2 = document.getElementById('btn-cerrar-popup2');

btnAbrirPopup2.addEventListener('click2', function(){
	overlay2.classList.add('active2');
	popup2.classList.add('active2');
});

btnCerrarPopup2.addEventListener('click2', function(e){
	e.preventDefault();
	overlay2.classList.remove('active2');
	popup2.classList.remove('active2');
});