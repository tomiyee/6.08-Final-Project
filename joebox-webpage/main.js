
// The server url
const SERVER_URL = "http://608dev-2.net/sandbox/sc/theng/bluffalo";
// The ms delay between sending messages
const DT = 1000;
// This will hold the input element that
let roomCodeInput;

// Makes sure that start() is called right away
window.onload = start;



/**
 * @function start - This function is called once, like the setup() function in the
 * arduino
 */
function start () {
  // Insert Start Code Here
  roomCodeInput = document.getElementById("room-code-input");
  roomCodeInput.addEventListener ('keydown', inputKeyDownHandler);


  // Sets the loop to be called every DT ms
  setInterval (loop, DT);
}



/**
 * @function loop - This function will be called periodically, every DT ms
 */
function loop () {

}

function inputKeyDownHandler (e) {
  // If they pressed enter, clear the input
  if (e.keyCode == 13) {
    roomCodeInput.value = "";
  }
}


/**
 * @function sendHttpRequest - description
 *
 * @param  {type} type description
 * @param  {type} url  description
 * @param  {type} body description
 * @return {type}      description
 */
async function sendHttpRequest (type, url, body) {
  const Http = new XMLHttpRequest();
  Http.open(type, url)
  Http.send();

  Http.onreadystatechange = (e) => {
    if (this.readyState == 4 && this.status == 200) {

    }
    console.log(Http.responseText);
  }
}
function test (url) {
  const Http = new XMLHttpRequest();
  Http.open('GET', url)
  Http.send();

  Http.onreadystatechange = (e) => {
    if (this.readyState == 4 && this.status == 200) {

    }
    console.log(Http.responseText);
  }
}
