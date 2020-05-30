


/*
OR "outgoing_msg"
<div class="incoming_msg">
  <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
  <div class="received_msg">
    <div class="received_withd_msg">
      <p>Test, which is a new approach to have</p>
      <span class="time_date"> 11:01 AM    |    Yesterday</span></div>
  </div>
</div>


<div class="outgoing_msg">
  <div class="sent_msg">
    <p>Apollo University, Delhi, India Test</p>
    <span class="time_date"> 11:01 AM    |    Today</span> </div>
</div>

*/

var img_link = "https://ptetutorials.com/images/user-profile.png"


function select_chat(chat_id){
  var div_history = document.getElementById('msg_history');
  div_history.innerHTML = '';
  msgs_from_chat(chat_id);

}

let init_chats = (chat_info) => {


  let chat_list = document.createElement('div');
  chat_list.className = 'chat_list';
  chat_list.setAttribute("onclick", "select_chat("+chat_info["chat_id"]+")")

  let chat_people = document.createElement('div');
  chat_people.className = 'chat_people';

  let chat_img = document.createElement('div');
  chat_img.className = 'chat_img';

  let image = document.createElement('img');
  image.src = "https://ptetutorials.com/images/user-profile.png";
  image.setAttribute("alt", "sunil")


  let chat_ib = document.createElement('div');
  chat_ib.className = 'chat_ib';

  let nickname = document.createElement('h5');
  nickname.innerText = chat_info["sender"];

  let date = document.createElement('span');
  date.className = 'chat_date';
  date.innerText = chat_info["date"];

  let mes_container = document.createElement('p');
  mes_container.innerText = chat_info["message_body"];


  chat_list.appendChild(chat_people);
  chat_people.appendChild(chat_img);
  chat_people.appendChild(chat_ib);
  chat_ib.appendChild(nickname);
  nickname.appendChild(date);
  chat_ib.appendChild(mes_container);


  var div_chats = document.getElementById('chats');

  div_chats.appendChild(chat_list);

}




let show_receive_msg = (message, time) => {


  let incoming = document.createElement('div');
  incoming.className = 'incoming_msg';

  let image_div = document.createElement('div');
  image_div.className = 'incoming_msg_img';

  let image = document.createElement('img');
  image.src = img_link;
  image.setAttribute("alt", "sunil")


  let receive_div = document.createElement('div');
  receive_div.className = 'received_msg';

  let inside_receive_div = document.createElement('div');
  inside_receive_div.className = 'received_withd_msg'


  let mes_container = document.createElement('p');
  mes_container.innerText = message;

  let date = document.createElement('span');
  date.className = 'time_date';
  var d = new Date();
  date.innerText = time;


  incoming.appendChild(image_div);
  image_div.appendChild(image);
  incoming.appendChild(receive_div);
  receive_div.appendChild(inside_receive_div);
  inside_receive_div.appendChild(mes_container);
  inside_receive_div.appendChild(date)


  var div_history = document.getElementById('msg_history');

  div_history.appendChild(incoming);
  //$( 'div.container.messaging.inbox_msg.mesgs.msg_history' ).append(outgoing);

}

let show_send_mes = (message, time) => {


  let outgoing = document.createElement('div');
  outgoing.className = 'outgoing_msg';

  let sent = document.createElement('div');
  sent.className = 'sent_msg';

  let mes_container = document.createElement('p');
  mes_container.innerText = message;
  mes_container.className = 'card-text';

  let date = document.createElement('span');
  date.className = 'time_date';
  var d = new Date();

  date.innerText = time;


  outgoing.appendChild(sent);
  sent.appendChild(mes_container);
  sent.appendChild(date);


  var history_messages = document.getElementById('msg_history');

  history_messages.appendChild(outgoing);
  //$( 'div.container.messaging.inbox_msg.mesgs.msg_history' ).append(outgoing);

}


async function sendMessage() {
  let message = document.getElementById('message').value;
  if (message.value.length == 0) {
    message.value = '';
    show_send_mes(message);
    console.log(message);


  }
}


async function msgs_from_chat(id){
  url = 'http://' + document.domain + ':' + location.port+'/get_messages?id='+id;
  let request_for_chats = await fetch(url,{
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

      var message = Object.keys(data);
      message.forEach( function(key) {
        var values = data[message]
        if (data[message]["sender"] == my_nick) {
          show_send_mes(data[message]["message_body"], data[message]["date"]);
        } else {
          show_receive_msg(data[message]["message_body"], data[message]["date"]);
        }
        // do stuff with "values"
      })


    }
  })
  };




async function append_chats() {
  url = 'http://' + document.domain + ':' + location.port+'/chatlist';
  let request_for_chats = await fetch(url,{
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

      var opened_chats = Object.keys(data);
      opened_chats.forEach( function(key) {
        var values = data[opened_chats]
        var href = data[opened_chats]["chat_id"]
        var date = data[opened_chats]["date"]
        var message = data[opened_chats]["message_body"]
        var sender = data[opened_chats]["sender"]
        init_chats(data[opened_chats])
        console.log(values)
        console.log(sender);
        // do stuff with "values"
      })


    }
  })
};

  append_chats()
