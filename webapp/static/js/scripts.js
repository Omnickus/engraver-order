document.getElementById('slider-left').onclick = sliderLeft;
document.getElementById('slider-right').onclick = sliderRight;
	var left = 0;


	function sliderLeft(){
		var polosa = document.getElementById('polosa');
		left = left -256;
		if (left <= -512 ) {
			left= 0;
		}
		polosa.style.marginLeft = left + "px" ;
	}

	function sliderRight(){
		var polosa = document.getElementById('polosa');
		left = left + 256;
		if (left = 0 ) {
			left= 0;
		}
		polosa.style.marginLeft = left + "px" ;
	}