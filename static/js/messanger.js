


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

let show_receive_msg = (message) => {


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
  date.innerText = "    |    TODAY";


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

let show_send_mes = (message) => {


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

  date.innerText = "    |    TODAY";


  outgoing.appendChild(sent);
  sent.appendChild(mes_container);
  sent.appendChild(date);


  var div_history = document.getElementById('msg_history');

  div_history.appendChild(outgoing);
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
