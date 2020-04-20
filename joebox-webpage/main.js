
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
  $('#room-code-input').keydown(inputKeyDownHandler);
  $('.game-container').hide();

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
 * @param  {Event} e Key Down Event data
 */
async function inputKeyDownHandler (e) {
  // If they pressed enter, clear the input
  if (e.keyCode == 13) {
    $(".input-container").hide();
    $('.game-container').show();
    $('.room-code').text(roomCodeInput.val());

    roomCodeInput.val("");
    // Temporarily sends a response to this server.
    let response = await sendHttpRequest ("GET", "http://608dev-2.net/sandbox/sc/theng/lab08a/lab08a.py");
  }
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
