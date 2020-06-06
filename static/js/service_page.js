console.log("HI");
var service= {'services_prices':{"first": "100"},"dates": {"06.06.2020": ["13:30-15:00", "15:00-16:30"], "07.06.2020": ["13:30-15:00", "15:00-16:30"]}};

function init_service (service, price) {


  let tr_row = document.createElement("tr")

  let row = document.createElement('th');
  row.setAttribute("scope", "row");
  row.innerText = "#";

  let service_name = document.createElement("td");

  let select_service_but = document.createElement("button");
  select_service_but.onclick = function() { select_service(service);};
  select_service_but.innerText = service;

  let service_price = document.createElement("td");
  service_price.innerText = price;



  var divslot = document.getElementById("select_service");

  tr_row.appendChild(row);
  tr_row.appendChild(service_name);
  service_name.appendChild(select_service_but);
  tr_row.appendChild(service_price);



  divslot.appendChild(tr_row);
}


function iterate_services () {
  //how to get??

  Object.keys(service['services_prices']).forEach(function(service_name) {
    init_service(service_name, service['services_prices'][service_name]);
});
}






iterate_services();

function select_service(service_name) {

  //var service = {"dates": {"06.06.2020": ["13:30-15:00", "15:00-16:30"], "07.06.2020": ["13:30-15:00", "15:00-16:30"]}};
  console.log(service);
  var table_services = document.getElementById("table_services");
  table_services.style = "display:none;"

  var table_services = document.getElementById("select_date_time");
  table_services.style = "display:block;"

  var list_of_dates = [];
  Object.keys(service['dates']).forEach(function(day) {
    console.log(day);
    list_of_dates.push(day);
  });

  console.log(service['dates']);
  for (var i = 0; i<service['dates'][list_of_dates[0]].length; i++){
          console.log(list_of_dates[0]);
          console.log(service['dates'][list_of_dates[0]][i]);
          init_work_hour(list_of_dates[0], service['dates'][list_of_dates[0]][i]);
      }

//  Object.keys(service['dates']).forEach(function(day) {
//    console.log(day);
//    for (var i = 0; i<service['dates'][day].length; i++){
//        console.log(day);
//        console.log(service['dates'][day]);
//        init_work_hour(day, service['dates'][day]);
//    }
//    break
//  });


}


function init_work_hour (selected_day, time) {
    let tr_row = document.createElement("tr")

    let row = document.createElement('th');
    row.setAttribute("scope", "row");
    row.innerText = "#";

    let service_time = document.createElement("td");

    let select_time_but = document.createElement("button");
    select_time_but.onclick = function() { select_time(time);};
    select_time_but.innerText = time;



    var divslot = document.getElementById("select_time");
    var day = document.getElementById("day");
    day.innerText = selected_day;

    tr_row.appendChild(row);
    tr_row.appendChild(service_time);
    service_time.appendChild(select_time_but);




    divslot.appendChild(tr_row);
}







function back_select_date() {
  console.log("shbnsrhg");
  var table_services = document.getElementById("table_services");
  table_services.style = "display:block;"

  var table_services = document.getElementById("select_date_time");
  table_services.style = "display:none;"
}

function next_day() {
  var day = document.getElementById("day");
  var next_button = document.getElementById("next_button")
  var previous_button = document.getElementById("previous_button")
  previous_button.style = "display:block";

  var list_of_dates = [];
  Object.keys(service['dates']).forEach(function(day) {
    console.log(day);
    list_of_dates.push(day);
  });


  for (var i = 0; i<list_of_dates.length; i++) {
    if (list_of_dates[i] == day.innerText) {
      var next_elem = i+1;
      if (next_elem <= list_of_dates.length) {
        remove_times()
        for (var k = 0; k<service['dates'][list_of_dates[next_elem]].length; k++){
                console.log(list_of_dates[next_elem]);
                console.log(service['dates'][list_of_dates[next_elem]][k]);
                init_work_hour(list_of_dates[next_elem], service['dates'][list_of_dates[next_elem]][k]);
            }


      } else {
        next_button.style = "display:none:"

      }
      break
    }

  }


}


function previous_day() {
  var day = document.getElementById("day");
  var previous_button = document.getElementById("previous_button");
  var next_button = document.getElementById("next_button");
  next_button.style = "display:block";

  var list_of_dates = [];
  Object.keys(service['dates']).forEach(function(day) {
    console.log(day);
    list_of_dates.push(day);
  });


  for (var i = 0; i<list_of_dates.length; i++) {
    if (list_of_dates[i] == day.innerText) {
      var next_elem = i-1;
      if (next_elem >= 0) {
        console.log(next_elem);
        console.log("here");
          remove_times()
        for (var k = 0; k<service['dates'][list_of_dates[next_elem]].length; k++){
                console.log(list_of_dates[next_elem]);
                console.log(service['dates'][list_of_dates[next_elem]][k]);
                init_work_hour(list_of_dates[next_elem], service['dates'][list_of_dates[next_elem]][k]);
            }


      } else {
        previous_button.style = "display:none:"

      }
      break
    }

  }
}

function remove_times() {
  const select_time = document.getElementById("select_time");
  while (select_time.firstChild) {
    select_time.removeChild(select_time.lastChild);
    }
}




async function select_time(time) {
  console.log(time);
  var day = document.getElementById("day");
  console.log(day.innerText);
  let message = {};
  message["day"] = day.innerText;
  message["time"] =time;
  message["service_id"] = window.location.href.split("service/")[1]
    url = 'http://' + document.domain + ':' + location.port+'/request_booking'

    let request_for_booking = await fetch(url,{
      method: 'POST',
      headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
      redirect: 'follow',
      body: JSON.stringify(message)
    })
    .then(response => {
      // HTTP 301 response
      // HOW CAN I FOLLOW THE HTTP REDIRECT RESPONSE?
      console.log(response)
      if (response.redirected) {
          window.location.href = response.url;
      }
  });

  }
