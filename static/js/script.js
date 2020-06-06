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
var service_image;
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

//func return values to save
function get_services_prices () {
	var inputs = document.getElementsByTagName("input");
		var data = {};
		for (var i = 0; i<inputs.length; i++) {
			if (inputs[i].id == "filled_name") {
				data[inputs[i].value] = inputs[i+1].value
			}
		}
	return data
}




// Step 3
// Map code and all

//to save
var coords = "0";
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

					//!to save
					coords = data["coords"];

          divimage.appendChild(imgsrc);
          showMap();

        }});
      }



//STEP 4/4 date registration

function init_timeslots(time_slot) {

	//check for right format of time
	var start_time = time_slot.split("-")[0]
	var hours_start = plus_zero(start_time.split(":")[0])
	var minutes_start = plus_zero(start_time.split(":")[1])

	var end_time = time_slot.split("-")[1]
	var hours_end = plus_zero(end_time.split(":")[0])
	var minutes_end = plus_zero(end_time.split(":")[1])



	let button_slot = document.createElement('div');
	button_slot.className = "alert alert-secondary";
	button_slot.innerText = hours_start+":"+minutes_start+"-"+hours_end+":"+minutes_end;

	var divslot = document.getElementById("timeslots");

	divslot.appendChild(button_slot);
}

function plus_zero(num) {
	if (parseInt(num)<10) {
		//kostil
		if (num != "00") {
		num = "0"+num;
		}
	}
	console.log(num);
	return num;
}

function showslots() {


	var range_time = document.getElementById("range_time").value;
	var start_time = document.getElementById("start_time").value;
	var end_time = document.getElementById("end_time").value;
	//check filling
	var show_info = document.getElementById("show_info");
	if (range_time == "" || start_time == "" || end_time == "") {
		show_info.style = "display:block;";
		show_info.innerText = "You forget to fill hours inputs";
		return;
	} else {

		show_info.style = "display:none;";
	}

	var divslot = document.getElementById("timeslots");
	var call_button = document.getElementById("pick_slot_but");
	if (call_button.textContent == "Clear slots") {
		call_button.textContent = "Show slots";
		while (divslot.firstChild) {
    	divslot.removeChild(divslot.lastChild);
  	}
		return;
	}
	var save_slots = document.getElementById("save_work_hours");
	save_slots.style = "display:block;";

	call_button.textContent = "Clear slots";


	var start_hour = start_time.split(":")[0];
	var start_minutes = start_time.split(":")[1];

	var end_hour = end_time.split(":")[0];
	var end_minutes = end_time.split(":")[1];


	var range_hour = range_time.split(":")[0];
	var range_minutes = range_time.split(":")[1];

	var duration_in_minutes = (parseInt(end_hour)-parseInt(start_hour))*60+(parseInt(end_minutes)-parseInt(start_minutes))

	var range_time_in_minutes = parseInt(range_hour)*60+parseInt(range_minutes)

	var count_slots = Math.ceil(duration_in_minutes/range_time_in_minutes);

	var end_minute_slot = parseInt(start_minutes);
	var end_hour_slot = parseInt(start_hour);
	var time_slot = "00:00-00:00";
  for (var slot = 0; slot < count_slots; slot++) {
		console.log(start_hour);
		console.log(range_hour);
		console.log(parseInt(start_hour)+parseInt(range_hour));
		console.log((parseInt(start_minutes)+parseInt(range_minutes)).toString());
		end_minute_slot += parseInt(range_minutes);
		if (end_minute_slot >= 60) {
			end_minute_slot -= 60;
			end_hour_slot += 1;
			end_hour_slot += parseInt(range_hour);


			time_slot = start_hour+":"+start_minutes+"-"+end_hour_slot.toString()+":"+end_minute_slot.toString();

			init_timeslots(time_slot);
			console.log(time_slot);

			start_hour = end_hour_slot.toString();
			start_minutes = end_minute_slot.toString();
		} else {
			end_hour_slot += parseInt(range_hour);


			time_slot = start_hour+":"+start_minutes+"-"+end_hour_slot.toString()+":"+end_minute_slot.toString();

			init_timeslots(time_slot);
			console.log(time_slot);

			start_hour = end_hour_slot.toString();
			start_minutes = end_minute_slot.toString();
		}
	}

}


//to send from 4/4
var dates = {}
function saveWorkHours(){
	var show_info = document.getElementById("show_info");

	var work_hours = document.getElementById("timeslots").childNodes;
	var list_work_hours = []
	for (var i=0; i<work_hours.length; i++){
		list_work_hours.push(work_hours[i].innerText);
	}
	var day = document.getElementsByClassName("day active");
	var month = document.getElementsByClassName("picker-switch");
	dates[day[0].innerText+" "+month[0].innerText] = list_work_hours


	show_info.style = "display:block;";
	show_info.innerText = "Saved for "+day[0].innerText+" "+month[0].innerText;
}


//from 1 step

//service_image

//sending data func
var all_service_data = {}
async function register_service() {

	all_service_data["service_name"] = document.getElementById("serviceName").value;
	all_service_data["addit_info"] = document.getElementById("additional_information").value;
	all_service_data["service_image"] = document.getElementById("img-upload").src.split("base64, ")[1];
	all_service_data["services_prices"] = get_services_prices();
	all_service_data["coords"] = coords;
	all_service_data["dates"] = dates;

	//check filling
	var show_info = document.getElementById("show_info");
	if (missed_input(all_service_data["service_name"])||
			missed_input(all_service_data["addit_info"])||
			missed_input(all_service_data["services_prices"])||
			missed_input(all_service_data["coords"])||
			missed_input(all_service_data["dates"])) {
		show_info.style = "display:block;";
		show_info.innerText = "You forget to fill some inputs";
		return;
	} else {
		show_info.style = "display:none;";
	}



	url = 'http://' + document.domain + ':' + location.port+'/check_data';
  let request_register_service = await fetch(url,{
    method: 'POST',
    headers: {
              'Content-Type': 'application/json;charset=utf-8'
            },
		redirect: 'follow',
    body: JSON.stringify(all_service_data)
  })
	.then(response => {
		// HTTP 301 response
		// HOW CAN I FOLLOW THE HTTP REDIRECT RESPONSE?
		console.log(response)
		if (response.redirected) {
				window.location.href = response.url;
		}
		})
};


//check for input
function missed_input(arg) {
	if (arg === undefined || arg == ""){
		return true
	}
}
