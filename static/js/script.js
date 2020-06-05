// Next/Previous create service tabs logic
$('.btnNext').click(function(){
	$('.nav-tabs > .nav-item > .active').parent().next('li').find('a').trigger('click');
});

$('.btnPrevious').click(function(){
	$('.nav-tabs > .nav-item > .active').parent().prev('li').find('a').trigger('click');
});

// Step 1
// Service picture upload
// the name of the file appear on select
$(".custom-file-input").on("change", function() {
	var fileName = $(this).val().split("\\").pop();
	$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

// When picture is uploaded call preview func
$("#inputImage").change(function() {
  readURL(this);
});

// Picture preview func
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#img-upload').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}


// Step 2
// Add positions and price logic
// TODO: REWRITE???
function createNewService(id) {

		let bootstrap_input = document.createElement('div');
    bootstrap_input.className = 'input-group';
		bootstrap_input.id = id
		console.log("created with");
		console.log(id);

    let div_for_button = document.createElement('div');
    div_for_button.className = 'input-group-prepend';

    let button = document.createElement('button');
    button.className = 'input-group-text';
		button.setAttribute("onClick", "add_delete(this)");
		button.setAttribute("type", "button");
		button.innerText = "Add new service"

    let input_name = document.createElement("input");
    input_name.className = 'form-control';
		input_name.setAttribute("placeholder", "Service name (ex. haircut)");
		input_name.setAttribute("type", "text");


		let input_price = document.createElement("input");
    input_price.className = 'form-control';
		input_price.setAttribute("placeholder", "Price: (ex. 500₽)");
		input_price.setAttribute("type", "text");

    bootstrap_input.appendChild(div_for_button);
    div_for_button.appendChild(button);
    bootstrap_input.appendChild(input_name);
    bootstrap_input.appendChild(input_price);

    $( 'div.services' ).append(bootstrap_input);

	}

	function add_delete(button) {
		if (button.textContent == "Add new service") {

			var filled_inputs = document.getElementById(button.parentNode.parentNode.id).getElementsByTagName("input");//.disabled = true

			console.log(filled_inputs[0].value.length);
			if (filled_inputs[0].value.length != 0 && Number.isInteger(parseInt(filled_inputs[1].value,10))) {
				button.textContent = "Delete"
				filled_inputs[0].disabled = true;
				filled_inputs[1].disabled = true;
				filled_inputs[0].id = "filled_name";
				var childrens = document.getElementById("inputs").children;
				createNewService(parseInt(childrens[childrens.length-1].id,10)+1);
			} else {
				//here should show that should be filled and second is integer!!!!
			}


		} else {
			document.getElementById(button.parentNode.parentNode.id).remove();
			var childrens = document.getElementById("inputs").children;
			if (childrens[childrens.length] == 0) {
				createNewService(1);
			}
		}
	}


// Step 3
// Map code and all
function showMap() {
    document.getElementsByClassName('check')[0].style.display = "block";
    document.getElementsByClassName('mapContainer')[0].style.display = "block";
    document.getElementsByClassName('fill_address')[0].style.display = "none";
}
function hideMap(){
  //removing old img
  img = document.getElementById("map_image");
  img.parentNode.removeChild(img);

  document.getElementsByClassName('check')[0].style.display = "none";
  document.getElementsByClassName('mapContainer')[0].style.display = "none";
  document.getElementsByClassName('fill_address')[0].style.display = "block";
}


  async function sendLocation(){
  let city = document.getElementById('city').value;
  let street = document.getElementById('street').value;
  let building_num = document.getElementById('building_num').value;
  var width = document.getElementById('width').offsetWidth;
  var data = new FormData();
  data.append('city', city);
  data.append('street', street);
  data.append('building_num', building_num);
  data.append('width', width)
  let response = await fetch('http://' + document.domain + ':5000/get_address_image',{
        method: 'POST',
        body: data
      })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data.message);
        if (data.message != '200OK') {
          console.log(data["image"]);
          var divimage = document.getElementById('mapContainer');

          let imgsrc = document.createElement("img");
          imgsrc.id = "map_image"
          imgsrc.src = 'data:image/png;base64, '+data["image"];

          divimage.appendChild(imgsrc);
          showMap();

        }});
      }
