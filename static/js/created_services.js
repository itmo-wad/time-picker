let createCard = (task) => {


  let card_href = document.createElement('a');
  card_href.setAttribute("href", 'http://' + document.domain + ':' + location.port+"/service?id="+task._id)
  card_href.style = "text-decoration: inherit; color: black;"

  let card = document.createElement('div');
  card.className = 'card mb-3';
  card.style = "max-width: 540px;"

  let cardInside = document.createElement('div');
  cardInside.className = 'row no-gutters';

  let cardImg = document.createElement('div');
  cardImg.className = 'col-md-4';
  let imgsrc = document.createElement("img");
  imgsrc.className = 'card-img';
  imgsrc.src = 'data:image/png;base64, '+task.service_logo;


  let cardBody = document.createElement('div');
  cardBody.class = 'col-md-8';

  let cardBodyInside = document.createElement('card-body');


  let title = document.createElement('h5');
  title.innerText = task.service_name;
  title.className = 'card-title';

  let description = document.createElement('p');
  description.innerText = task.addit_info;
  description.className = 'card-text';

  let master_name = document.createElement('p');
  master_name.innerText = task.username;
  master_name.className = 'card-text';

  let destination = document.createElement('p');
  destination.className = 'card-text';

  let destinationInside = document.createElement('small');
  destinationInside.innerText = "Coordinates lt: "+task.lt;
  destinationInside.className = 'text-muted';

  let middle_price = document.createElement('p');
  middle_price.className = 'card-text';

  let middle_priceInside = document.createElement('small');
  middle_priceInside.innerText = 'Middle price: '+task.middle_price;
  middle_priceInside.className = 'text-muted';








  //cardResult = document.getElementById('search-result');
  //cardResult.appendChild(card);
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

  $( 'div.search_res' ).append(card_href);
  console.log("last mesaage");

}


let initListOfTasks = (search_result) => {
  $('div.search_res').empty();
  search_result.forEach((task) => {
    createCard(task);
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

find_services()
