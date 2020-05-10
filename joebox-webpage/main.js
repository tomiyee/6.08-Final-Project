
// The server url
const SERVER_URL = "https://608dev-2.net/sandbox/sc/team033/bluffalo/server.py";
// The ms delay between sending messages
const DT = 1000;
// This will hold the HTML Room Code Input
let roomCodeInput;
// The string that the user entered as the Room Code
let roomCode;
let roomData;
let animating = false;
let intervalId;

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
  hideAllOthers('.input-container');
  $('.button-room-input').click(inputButtonPressHandler);
  $('.button-start-game').click(startGameButtonPressHandler);

  // Sets the loop to be called every DT ms
  intervalId = setInterval (loop, DT);
}

/**
 * @function loop - This function will be called periodically, every DT ms
 */
async function loop () {
  // 0. Do nothing if the user has not entered a room code
  if (!roomCode)
    return;

  // 1. Send a request to the server for game data
  let resp = await sendHttpRequest("GET", SERVER_URL+"?action=dump_data&room_code=" + roomCode);
  let newRoomData = JSON.parse(resp);
  // For the initial fetch from the server
  if (!roomData) roomData = newRoomData;

  // 2. Check for Transitions to Animate
  if (!newRoomData['game_data']['waiting_for_votes'] && roomData['game_data']['waiting_for_votes'])
    onVoteEndHandler(roomData, newRoomData);
  if (newRoomData['game_data'].round_number > roomData['game_data'].round_number)
    onRoundEndHandler(roomData, newRoomData);
  if (newRoomData['game_data']['in_lobby'] && !roomData['game_data']['in_lobby'])
    onGameEndHandler(roomData, newRoomData);

  roomData = newRoomData;

  // 3a. If in lobby, update the list of players
  if (!animating && roomData['game_data']['in_lobby'] && roomData['game_data']['round_number'] != 3) {
    hideAllOthers('.lobby-container');
    displayLobby();
  }

  // 3b. If waiting for submissions, update list of waiting.
  if (!animating && (roomData['game_data']['waiting_for_submissions'] ||
      roomData['game_data']['waiting_for_votes'])) {
    hideAllOthers('.game-container');
    displayPrompt();
    displayPlayers();
    displayOptions();
    if (roomData['game_data']['waiting_for_votes'])
      $('.options-container').show();
    else
      $('.options-container').hide();
  }
}

/**
 * @function onVoteEndHandler - Triggers animations that happen after everyone
 * has voted, like showing how the rank has changed
 *
 * @param  {type} old  The old game data dictionary
 * @param  {type} _new The new game data dictionary
 */
function onVoteEndHandler (old, _new) {
  console.log(`onVoteEndHandler(${JSON.stringify(old)}, ${JSON.stringify(_new)})`);
  // Shows the container
  hideAllOthers(".score-container");
  $(".scoreboard").empty();

  let oldSortedScores = [];
  let newSortedScores = [];

  // Adds a row for the Correct Answer
  let r = old['game_data']['round_number'];
  let q = old['game_data']['question_number'];
  let ans = old['game_data']['all_prompts'][(r-1)*3+q-1][2];
  let ans_row = $(document.createElement('tr'))
    .append($(document.createElement('td')).text('ANSWER'))
    .append($(document.createElement('td')).text(ans))
    .append($(document.createElement('td')).text('+' + r*1000))
    .addClass("correct-answer")
    .addClass('scoreboard-row');
  $(".scoreboard").append(ans_row);
  // Adds a row for each of the other players
  for(let p in old['player_data']) {
    // If the player's nametag is not yet displayed, then create it
    let row = $(document.createElement('tr'));
    let name = $(document.createElement('td'));
    let bluff = $(document.createElement('td'));
    let score = $(document.createElement('td'));

    row.addClass('scoreboard-row');
    row.addClass('scoreboard-row-' + p);
    score.addClass('scoreboard-score-'+p);
    // Make the name and score elements a child of the row element
    row.append(name);
    row.append(bluff);
    row.append(score);
    // Append data to the lists we will sort
    oldSortedScores.push([p, old['player_data'][p]['score']]);
    newSortedScores.push([p, _new['player_data'][p]['score']]);
    // Updates the contents
    name.text(p);
    bluff.text(old['player_data'][p]['submission'])
    score.text(old['player_data'][p]['score']);

    $(".scoreboard").append(row);
  }

  oldSortedScores.sort(function(a,b) {return b[1]<a[1]?-1:1;});
  newSortedScores.sort(function(a,b) {return b[1]<a[1]?-1:1;});

  let ROW_HEIGHT = 40;
  animating = true;
  //Show old scores briefly for 2 seconds
  for(let i in oldSortedScores) {
    let playerName = oldSortedScores[i][0];
    let row = $('.scoreboard-row-' + playerName);
    row.css('top', i * ROW_HEIGHT + ROW_HEIGHT + 10 + 'px');
  }

  // Start the 2 second animation 2 seconds after the beginning
  setTimeout(function () {
    for(let i in newSortedScores) {
      let playerName = newSortedScores[i][0];
      let row = $('.scoreboard-row-' + playerName);
      row.css('top', i * ROW_HEIGHT + ROW_HEIGHT + 10 + 'px');
      $('.scoreboard-score-' + playerName).text(newSortedScores[i][1]);
    }
  }, 2000);

  // When we want to HIDE the score animation
  setTimeout(function () {
    animating = false;
  }, 6000);
}

/**
 * @function onRoundEndHandler - Triggers animations that happen after a round
 * ends, like displaying the announcement of a new round
 *
 * @param  {type} old  The old game data dictionary
 * @param  {type} _new The new game data dictionary
 */
function onRoundEndHandler (old, _new) {
  setTimeout(() => {
    animating = true;
    // Insert some animation

    // ...
  }, 6000);

  // Finished Animations
  setTimeout(() => {
    animating = false;
  }, 7000); // TODO add the duration of the animation
}

/**
 * @function onGameEndHandler - Triggers animations that happen when the game
 * ends like displaying the rankings
 *
 * @param  {type} old  The old game data dictionary
 * @param  {type} _new The new game data dictionary
 */
function onGameEndHandler (old, _new) {
  setTimeout(() => {
    hideAllOthers(".score-container");
    animating = true;
  }, 6100);
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

/**
 * @function inputButtonPressHandler - When the user presses the join room
 * button, run the enterRoomCode function
 */
async function inputButtonPressHandler () {
    enterRoomCode();
}

/**
 * @function enterRoomCode - Using the text in the room code input,
 * 1. Send an HTTP request to check if the room code is valid
 * 2. If it is, then we will join it.
 * 3. If it is NOT, then we display the error message
 *
 * @return {type}  description
 */
async function enterRoomCode () {

    // Sends the HTTP request to check if the room code exists
    roomCode = roomCodeInput.val();
    let response = await sendHttpRequest (
      "GET",
      SERVER_URL+"?action=room_code_check&room_code="+roomCode);

    // If the response is "false", she the error
    if (response.trim() != "true") {
        $('.error-room').show();
        roomCodeInput.val("");
        return;
    }
    // Otherwise, move on
    $('.room-code').text(roomCode);

    // Request the complete JSON data for the game
    response = await sendHttpRequest (
        "GET",
        SERVER_URL+"?action=dump_data&room_code="+roomCode);
    try {
      roomData = JSON.parse(response);
    } catch (e) {
      console.log(response);
      $('.error-room').show();
      return;
    }
    // If in lobby, show the players.
    if (roomData['game_data']['in_lobby']) {
      hideAllOthers('.lobby-container');
      displayLobby();
    }
    // Otherwise enter the game
    else {
      hideAllOthers('.game-container');
      displayPrompt();
    }
}

async function startGameButtonPressHandler() {
    // Sends the HTTP request to check if the room code exists
    let response = await sendHttpRequest (
      "POST",
      SERVER_URL,
      "action=start_game&room_code=" + roomCode
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

async function displayOptions () {
  // Get the bluffs and sorts them
  let sortedOptions = [];
  let playerData = roomData['player_data'];
  for (let p in playerData)
    sortedOptions.push(playerData[p]["submission"]);
  // Adds the correct answer to the lsit
  let gameData = roomData['game_data'];
  let promptIndex = (gameData['round_number']-1)*3+gameData['question_number']-1;
  sortedOptions.push(gameData['all_prompts'][promptIndex][2]);

  sortedOptions.sort();
  // Display the options in sorted order
  let optionsList = $(".options-container");
    optionsList.empty();
  for (let i in sortedOptions) {
    let li = $(document.createElement('li'));
      li.text(sortedOptions[i]);
      optionsList.append(li);
  }
}

function displayPlayers () {
  // Find out who has and has not voted
  let playerRow = $(".player-voting-rows");

  for(let p in roomData['player_data']) {
    // If the player's nametag is not yet displayed, then create it
    if ($('.player-nametag-' + p).length == 0) {
      let nametag = $(document.createElement('span'));
        nametag.addClass("player-nametags");
        nametag.addClass("player-nametag-" + p);
        nametag.text(p);
        playerRow.append(nametag);
    }
    let nametag = $('.player-nametag-' + p);
      nametag.removeClass('done').addClass('not-done');
    // If game state is submitting, color names based on if they have submitted
    if (roomData['game_data']['waiting_for_submissions'])
      if (roomData['player_data'][p]['submitted'])
        nametag.addClass("done").removeClass('not-done');
    // If game state is voting, color names based on if they have voted
    if (roomData['game_data']['waiting_for_votes'])
      if (roomData['player_data'][p]['voted'])
        nametag.addClass('done').removeClass('not-done');
  }
}

function hideAllOthers (container) {
    $('.game-container').hide();
    $('.lobby-container').hide();
    $('.error-room').hide();
    $(".input-container").hide();
    $(".score-container").hide();

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
