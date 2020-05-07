





void writeToBytes(char* inputArray, byte* outputArray){
  memset(outputArray,0,sizeof(outputArray));
  for (int i =0; i < strlen(inputArray);i++){
    outputArray[0] = (byte) inputArray[0];
  }
}

/*----------------------------------
  char_append Function:
  Arguments:
     char* buff: pointer to character array which we will append a
     char c:
     uint16_t buff_size: size of buffer buff

  Return value:
     boolean: True if character appended, False if not appended (indicating buffer full)
*/

void printMenu(int choice){
  tft.fillRect(3,40,10,10,TFT_WHITE);
  tft.fillRect(3,60,10,10,TFT_WHITE);
  if (choice == 0){
    tft.setCursor(3,40);
    tft.print("->");
    tft.print("Create Room");
    tft.setCursor(3,60);
    tft.print("  ");
    tft.print("Join Room");
  }
  else{
    tft.setCursor(3,40);
    tft.print("  ");
    tft.print("Create Room");
    tft.setCursor(3,60);
    tft.print("->");
    tft.print("Join Room");
  }

  tft.setCursor(3,80);
  tft.println("1: Scroll");
  tft.setCursor(3,90);
  tft.println("2: Select");
}



uint8_t char_append(char* buff, char c, uint16_t buff_size) {
  int len = strlen(buff);
  if (len > buff_size) return false;
  buff[len] = c;
  buff[len + 1] = '\0';
  return true;
}

/*----------------------------------
 * do_http_request Function:
 * Arguments:
 *    char* host: null-terminated char-array containing host to connect to
 *    char* request: null-terminated char-arry containing properly formatted HTTP request
 *    char* response: char-array used as output for function to contain response
 *    uint16_t response_size: size of response buffer (in bytes)
 *    uint16_t response_timeout: duration we'll wait (in ms) for a response from server
 *    uint8_t serial: used for printing debug information to terminal (true prints, false doesn't)
 * Return value:
 *    void (none)
 */
void do_http_request(char* host, char* request, char* response, uint16_t response_size, uint16_t response_timeout, uint8_t serial) {
  WiFiClient client; //instantiate a client object
  if (client.connect(host, 80)) { //try to connect to host on port 80
    if (serial) Serial.print(request);//Can do one-line if statements in C without curly braces
    client.print(request);
    memset(response, 0, response_size); //Null out (0 is the value of the null terminator '\0') entire buffer
    uint32_t count = millis();
    while (client.connected()) { //while we remain connected read out data coming back
      client.readBytesUntil('\n', response, response_size);
      if (serial) Serial.println(response);
      if (strcmp(response, "\r") == 0) { //found a blank line!
        break;
      }
      memset(response, 0, response_size);
      if (millis() - count > response_timeout) break;
    }
    memset(response, 0, response_size);
    count = millis();
    while (client.available()) { //read out remaining text (body of response)
      char_append(response, client.read(), OUT_BUFFER_SIZE);
    }
    if (serial) Serial.println(response);
    client.stop();
    if (serial) Serial.println("-----------");
  } else {
    if (serial) Serial.println("connection failed :/");
    if (serial) Serial.println("wait 0.5 sec...");
    client.stop();
  }
}

/*----------------------------------
 * initTft Function:
 *
 * Initializes the Screen and related variables
 */
void initTft () {
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(TFT_WHITE);
  tft.setTextColor(TFT_BLACK, TFT_WHITE);
}

/*----------------------------------
 * loadWifi Function:
 *
 * Handles logging in to the Wifi.
 */
void loadWifi () {
  WiFi.begin(network, password); //attempt to connect to wifi
  uint8_t count = 0; //count used for Wifi check times
  Serial.print("Attempting to connect to ");
  Serial.println(network);
  while (WiFi.status() != WL_CONNECTED && count < 12) {
    delay(500);
    Serial.print(".");
    count++;
  }
  delay(2000);
  if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    Serial.println("CONNECTED!");
    Serial.println(WiFi.localIP().toString() + " (" + WiFi.macAddress() + ") (" + WiFi.SSID() + ")");
    delay(500);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
}

/*----------------------------------
 * initImu Function:
 *
 * Handles initializing the Accelerometer
 */
void initImu () {
  if (imu.setupIMU(1)) {
    Serial.println("IMU Connected!");
  } else {
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart();
  }
}

/*----------------------------------
 * search Function:
 *   Searches a character array for the sequence of characters in the delimiter.
 *   It will then return a pointer to the first char after the first occurrence
 *   of the delimiter. If no such sequence exists in the source character array,
 *   it will simply return the source char array.
 *
 * Arguments:
 *    char* source: pointer to character array which we will search for the sequence
 *    char* delim: a character array we want to find in the source char array
 *
 * Return value:
 *    boolean: true if the source contains query
 */
boolean search (char* source, char* query) {
  for (int i = 0; i < strlen(source); i++) {
    boolean worked = true;
    for (int j = 0; j < strlen(query); j++) {
      if (source[i+j] != query[j]) {
        worked = false;
        break;
      }
    }
    // If we found the delim, return a ptr to the char after the delim
    if (worked)
      return true;
  }
  return false;
}

/*----------------------------------
 * server_post Function:
 *
 * Sends a POST request to the server with the provided
 * action and parameters.

 * Arguments:
 *    char* action: The string for what action we are doing
 *    char* body: a string for form-urlencoded parameters
 *
 * Example: server_post("get_bluffs","room_code=LBXF&user=Joe")
 *
 * The response is saved to the global response variable
 */
void server_post (char* action, char* body) {
  char request[500];
  sprintf(request, "POST /sandbox/sc/team033/bluffalo/server.py HTTP/1.1\r\n");
  sprintf(request + strlen(request), "Host: %s\r\n", host);
  strcat(request, "Content-Type: application/x-www-form-urlencoded\r\n");
  // Form the proper body
  char true_body[200];
  sprintf(true_body, "action=%s", action);
  if (strlen(body) != 0) {
    strcat(true_body, "&");
    strcat(true_body, body);
  }
  // Sends the POST request
  sprintf(request + strlen(request), "Content-Length: %d\r\n\r\n", strlen(true_body));
  strcat(request, true_body);

  do_http_request(host, request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
}

/*----------------------------------
 * server_get Function:
 *
 * Sends a GET request to the server with the provided
 * action and parameters.
 *
 * Arguments:
 *    char* action: The string for what action we are doing
 *    char* body: a string for form-urlencoded parameters
 *
 * Example: server_get("get_bluffs","room_code=LBXF&user=Joe")
 *
 * The response is saved to the global response variable
 */
void server_get (char* action, char* params) {
  char request[500];
  sprintf(request,"GET /sandbox/sc/team033/bluffalo/server.py?action=%s&%s HTTP/1.1\r\n",action,params);
  sprintf(request + strlen(request), "Host: %s\r\n\r\n", host);

  do_http_request(host, request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
  response[strlen(response)-1]='\0';
}


/*----------------------------------
 * add_key Function:
 *
 * Given a string, adds the key value pair to the string to help with making
 * the body/parameters  for the server_get and server_post helper functions.
 *
 * Example:
 *
 * char params[50] = "";
 * add_key(params, "room_code", "ABCD"); // "room_code=ABCD"
 * add_key(params, "user",      "TOM");  // "room_code=ABCD&user=TOM"
 */
void add_key (char*parameters, char*param_key, char*param_val) {
  if (strlen(parameters) > 0)
    strcat(parameters, "&");
  strcat(parameters, param_key);
  strcat(parameters, "=");
  strcat(parameters, param_val);
}
