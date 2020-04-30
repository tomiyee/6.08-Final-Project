
// The server url
const SERVER_URL = "https://608dev-2.net/sandbox/sc/team033/bluffalo/server.py";
// The ms delay between sending messages
const DT = 1000;
// This will hold the HTML Room Code Input
let roomCodeInput;
// The string that the user entered as the Room Code
let roomCode;
// Makes sure that start() is called right away
window.onload = start;


/**
 * @function start - This function is called once, like the setup() function in
 * the ESP32 code. At the end of the function, it sets an interval to call the
 * loop every DT ms
 */
function start () {
  // Insert Start Code Here
  roomCodeInput = $("#room-code-input");
    $('#room-code-input').keypress(inputKeyPressHandler);
  $('#room-code-input').keydown(inputKeyDownHandler);
  $('.game-container').hide();
    $('.lobby-container').hide();
    $('.error-room').hide();
    $('.button-room-input').click(inputButtonPressHandler);
    $('.button-start-game').click(startGameButtonPressHandler);
    
    

  // Sets the loop to be called every DT ms
  setInterval (loop, DT);
}

/**
 * @function loop - This function will be called periodically, every DT ms
 */
async function loop () {
  // 0. Do nothing if the user has not entered a room code

  // 1. Send a request to the server for game data
  let resp = await sendHttpRequest("GET", SERVER_URL + "?action=in_lobby");

  // 2. Handle the response, displaying or hiding elements as necessary

}

/**
 * @function inputKeyDownHandler - Handles the key down event when someone is
 * typing into the input.
 *
 * @param  {KeyboardEvent} e Key Down Event data
 */
async function inputKeyDownHandler (e) {

  // If they pressed enter, clear the input
  if (e.keyCode == 13) {
      enterRoomCode();
  }
}

/**
 * @function inputKeyPressHandler - Whenever the user presses a button while
 * focused on the input.
 *
 * @param  {KeyboardEvent} e Key Down Event data
 */
async function inputKeyPressHandler (e) {
    if (e.keyCode >= 97 && e.keyCode <= 122) {
        if (!e.ctrlKey && !e.metaKey && !e.altKey) {
            let charCode = e.keyCode - 32;
            let start = e.target.selectionStart;
            let end = e.target.selectionEnd;
            e.target.value = e.target.value.substring(0, start) + String.fromCharCode(charCode) + e.target.value.substring(end);
            e.target.setSelectionRange(start+1, start+1);
            e.preventDefault();
        }
    }
}

async function inputButtonPressHandler () {
    enterRoomCode();
}

async function enterRoomCode () {

    // Sends the HTTP request to check if the room code exists
    roomCode = roomCodeInput.val();
    let response = await sendHttpRequest (
      "GET",
      SERVER_URL+"?action=room_code_check&room_code="+roomCode);

    // If the response is "true", proceed
    if (response.trim() == "true") {

        hideAllOthers('.game-container');
        $('.room-code').text(roomCode);
    
        response = await sendHttpRequest (
            "GET",
            SERVER_URL+"?action=in_lobby&room_code="+roomCode);
        if (response.trim() == "false") {
            displayPrompt();
        }
        else {
            hideAllOthers('.lobby-container');
            displayLobby();
        }
    }
    // If the room code does not exist, show the error
    else {
        $('.error-room').show();
    }

    roomCodeInput.val("");
}

async function startGameButtonPressHandler() {
    // Sends the HTTP request to check if the room code exists
    let response = await sendHttpRequest (
      "POST",
      SERVER_URL,
        "action=start_game&room_code="+roomCode
        
    );
    hideAllOthers('.game-container');
    displayPrompt();
}

async function displayPrompt () {
    let response = await sendHttpRequest (
        "GET",

        SERVER_URL+"?action=current_prompt&room_code="+roomCode);
    
    let whole_prompt = response.trim().split("=");
    let word = whole_prompt[0];
    let prompt = whole_prompt[1];

    $('.word').text(word);
    $('.prompt').text(prompt);
}

async function displayLobby () {
    let response = await sendHttpRequest (
        "GET",
        SERVER_URL+"?action=list_players&room_code="+roomCode);
    
    let all_players = response.trim().split(",");
    let left_players = [];
    let right_players = [];
    for (let i = 0; i < all_players.length; i++) {
        if (i % 2 == 0) {
            left_players.push(all_players[i]);
        }
        else {
            right_players.push(all_players[i]);
        }
    }
    
    $('.left-players')[0].innerHTML=left_players.join("<br>");
    $('.right-players')[0].innerHTML=right_players.join("<br>");
    
//    $('.players').text(all_players);
}

function hideAllOthers (container) {
    $('.game-container').hide();
    $('.lobby-container').hide();
    $('.error-room').hide();
    $(".input-container").hide();
    
    $(container).show();
}


/**
 * @function dump - Prints to console the entire contents of the game data db
 */
function dump () {
  sendHttpRequest(
    "GET",
    "https://608dev-2.net/sandbox/sc/team033/bluffalo/server.py?action=dump_data")
    .then((r) => console.log(r));
}


/**
 * @function sendHttpRequest - Handles sending HTTP Requests and wraps the process
 * into a Javascript Promise, which resolves once the response comes back from the
 * server, or rejects if something in the process went wrong.
 *
 * @param  {String} type   The kind of HTTP Request, "GET", "POST", etc.
 * @param  {String} url    The link to send the request to.
 * @param  {String} [body] The body of the POST request
 * @param  {String} [contentType="application/x-www-form-urlencoded"] The encoding of the body
 * @return {Promise}       Resolves to the response of the HTTP Request
 */
async function sendHttpRequest (type, url, body, contentType="application/x-www-form-urlencoded") {
  // Creates a new HTTP request
  const Http = new XMLHttpRequest();
  // Formats the header and bode and all that.
  Http.open(type, url, true)
  Http.setRequestHeader("Content-Type", contentType);

  // Prepares the Javascript Promise to wrap around the HTTP Request
  let p = new Promise ((res, rej) => {
    Http.onreadystatechange = (e) => {
      if (Http.readyState == XMLHttpRequest.DONE) {
        // Successfully received response
        if (Http.status == 200)
          res(Http.responseText);
        else
          rej("HTTP Request went wrong.");
      }
    }
  });
  // Sends the request to the server with the specified body
  Http.send(body);
  // Return the promise above
  return p;
}
