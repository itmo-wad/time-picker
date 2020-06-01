

find_services()


let createCard = (service_info) => {


  let card_with_buttons = document.createElement("div");
  card_with_buttons.className = "card_with_but";

  let card_href = document.createElement('a');
  card_href.setAttribute("href", 'http://' + document.domain + ':' + location.port+"/service?id="+service_info._id)
  card_href.style = "text-decoration: inherit; color: black;"
  card_href.className = "card_href"

  let card = document.createElement('div');
  card.className = 'card mb-3';
  card.style = "max-width: 100%;"
  card.style.display = "flex";

  let cardInside = document.createElement('div');
  cardInside.className = 'row no-gutters';



  let buttons = document.createElement('div');
  buttons.className = 'buttons'

  let delete_but = document.createElement('button');
  delete_but.className = "btn btn-raised btn-danger";
  delete_but.innerText = "Delete service";

  let correct_but = document.createElement('button');
  correct_but.className = "btn btn-raised btn-secondary";
  correct_but.innerText = "Change info / schedular";
  correct_but.onclick = "change"
  correct_but.setAttribute("onclick", "change_info("+service_info._id+")")

  let journal_but = document.createElement('button');
  journal_but.className = "btn btn-raised btn-success";
  journal_but.innerText = "View journal";

  let view_requests = document.createElement('button');
  view_requests.className = "btn btn-raised btn-info";
  view_requests.innerText = "Requests [0]";




  let cardImg = document.createElement('div');
  cardImg.className = 'col-md-4';

  let imgsrc = document.createElement("img");
  imgsrc.className = 'card-img';
  imgsrc.src = 'data:image/png;base64, '+service_info.service_logo;
  //imgsrc.style.width = '200px';
  //imgsrc.style.height = '200px';
  imgsrc.style.objectFit = 'cover';



  let cardBody = document.createElement('div');
  cardBody.class = 'col-md-8';

  let cardBodyInside = document.createElement('card-body');


  let title = document.createElement('h5');
  title.innerText = service_info.service_name;
  title.className = 'card-title';
  title.style.margin = "5%";

  let description = document.createElement('p');
  description.innerText = service_info.addit_info;
  description.className = 'card-text';
  description.style.marginLeft = "5%";

  let master_name = document.createElement('p');
  master_name.innerText = "Master: "+service_info.username;
  master_name.className = 'card-text';
  master_name.style.marginLeft = "5%";

  let destination = document.createElement('p');
  destination.className = 'card-text';
  destination.style.marginLeft = "5%";

  let destinationInside = document.createElement('small');
  destinationInside.innerText = "Coordinates lt: "+service_info.lt;
  destinationInside.className = 'text-muted';

  let middle_price = document.createElement('p');
  middle_price.style.marginLeft = "5%";
  middle_price.className = 'card-text';

  let middle_priceInside = document.createElement('small');
  middle_priceInside.innerText = 'Middle price: '+service_info.middle_price;
  middle_priceInside.className = 'text-muted';









  //cardResult = document.getElementById('search-result');
  //cardResult.appendChild(card);
  card.appendChild(buttons);
  buttons.appendChild(journal_but);
  buttons.appendChild(view_requests);
  buttons.appendChild(correct_but);
  buttons.appendChild(delete_but);
  card_href.appendChild(card);
  card.appendChild(cardInside);
  cardInside.appendChild(cardImg);
  cardInside.appendChild(cardBody);
  cardImg.appendChild(imgsrc);
  cardBody.appendChild(cardBodyInside);
  cardBodyInside.appendChild(title);
  cardBodyInside.appendChild(description);
  cardBodyInside.appendChild(master_name);
  cardBodyInside.appendChild(destination);
  destination.appendChild(destinationInside);
  cardBodyInside.appendChild(middle_price);
  middle_price.appendChild(middle_priceInside);

  $( 'div.search_res' ).append(card);
  console.log("last mesaage");

}


let initListOfTasks = (search_result) => {
  $('div.search_res').empty();
  search_result.forEach((service_info) => {
    createCard(service_info);
  });
};


async function find_services(){

request = 'http://' + document.domain + ':' + location.port+'/created_services';
let response = await fetch(request,{
  method: 'POST',
  headers: {
            'Content-Type': 'application/json;charset=utf-8'
            }
})
.then((response) => {
  return response.json();
})
.then((data) => {
  if (data.message != '200OK') {
    initListOfTasks(data.services);


  }
});
}


let initChangeButtons = (id) => {




  let change_buttons = document.createElement('div');
  change_buttons.className = 'card mb-3';
  change_buttons.style = "max-width: 100%;";

  let inside_change_buttons = document.createElement('div');
  inside_change_buttons.className = 'row no-gutters';

  let change_main_info = document.createElement('button');
  change_main_info.className = "btn btn-outline-secondary btn-block";
  change_main_info.innerText = "Change name, description or label";
  change_main_info.setAttribute("onclick", "window.location.href='/create_service?idc="+id+"'")

  let change_services = document.createElement('button');
  change_services.className = "btn btn-outline-secondary btn-block";
  change_services.innerText = "Change services, prices";
  change_services.setAttribute("onclick", "window.location.href='/create_service?idc="+id+"'")

  let change_mapAddress = document.createElement('button');
  change_mapAddress.className = "btn btn-outline-secondary btn-block";
  change_mapAddress.innerText = "Change location of service";
  change_mapAddress.setAttribute("onclick", "window.location.href='/create_service?idc="+id+"'")

  let back_button = document.createElement('button');
  back_button.className = "btn btn-outline-secondary btn-block";
  back_button.innerText = "Back to services";
  back_button.setAttribute("onclick", "show_services()")


  change_buttons.appendChild(inside_change_buttons)
  inside_change_buttons.appendChild(change_main_info)
  inside_change_buttons.appendChild(change_services)
  inside_change_buttons.appendChild(change_mapAddress)
  inside_change_buttons.appendChild(back_button)

  $( 'div.search_res' ).append(change_buttons)

}



function change_info(service_id){
  $( 'div.search_res' ).empty();
  initChangeButtons(service_id);
}
