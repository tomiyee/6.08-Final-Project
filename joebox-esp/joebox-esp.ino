#include <WiFi.h> //Connect to WiFi Network
#include <SPI.h>
#include <TFT_eSPI.h>
#include <EEPROM.h>
#include <mpu6050_esp32.h>
#include<math.h>
#include<string.h>
#include "Button.h" //important fancy button class from Button.h file
#include "TextSlider.h"

TFT_eSPI tft = TFT_eSPI();
const int SCREEN_HEIGHT = 160;
const int SCREEN_WIDTH = 128;
const int BUTTON_PIN1 = 16;
const int BUTTON_PIN2 = 5;
const int LOOP_PERIOD = 40;

#define START 0
#define MAIN 1
#define LOBBY_HOST 2
#define JOIN 3
#define LOBBY_GUEST 4
#define BLUFFING 5
#define CREATE 6
#define INPUTUSER 7
#define VOTE 8
#define WAITINGSUBMISSION 10
#define WAITINGVOTES 11
#define OLD_USER 12
#define RESTART 13

MPU6050 imu; //imu object called, appropriately, imu

char network[] = "wavesandwarehouses";
char password[] = "G0PiggyTime99!";

//The followin are for ESP inputs via the gyro:

//Variables for the username input.
char user[100];
char old_user[100];

//Variable for the submission input.
char submission[100] = {0};
char old_submission[100] = {0};

//Variables for the roomKey input.
char roomKey[100] = {0};
char prevRoomKey[100] = {0};

//Variable used to keep track of whether the user is a host or not:
boolean isUserHost = false;


//The following is for the EEPROM functionality of the ESP:
char storedUser[100] = "";

//Contains the index of the subsection of the EEPROM memory we allocate to the token. 50 bytes.
int tokenLocation = 100;


//STATE MACHINE VARIABLE:
int stateMain = 0;


//Choice variable for the main Menu.
int choiceMain = 0;

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char old_response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP request

char host[] = "608dev-2.net";

//Variable for storing the prompt for redisplaying during voting rounds.
char old_prompt[150] = {0};

unsigned long primary_timer;
unsigned long lobby_timer = 7000;
unsigned long submission_timer = 60;
int last_post = millis();

int choice_vote = 1;
int num_players;

int old_val;

int roundNumber = 1;

//used to get x,y values from IMU accelerometer
void get_angle(float* x, float* y) {
  imu.readAccelData(imu.accelCount);
  *x = imu.accelCount[0] * imu.aRes;
  *y = imu.accelCount[1] * imu.aRes;
}

void lookup(char* query, char* response, int response_size) {
  char request_buffer[200];
  //CHANGE TO TARGET SERVER SCRIPT, to be determined later
  sprintf(request_buffer, "GET /sandbox/sc/person/wiki_getter.py?topic=%s HTTP/1.1\r\n", query);
  strcat(request_buffer, "Host: 608dev-2.net\r\n");
  strcat(request_buffer, "\r\n"); //new line from header to body

  do_http_request("608dev-2.net", request_buffer, response, response_size, RESPONSE_TIMEOUT, true);
}


class FibbageGetter {
    char alphabet[50] = " ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char message[400] = {0}; //contains previous query response
    char query_string[50] = {0};
    int char_index;
    int state;
    unsigned long scrolling_timer;
    const int scrolling_threshold = 150;
    const float angle_threshold = 0.3;
  public:
    FibbageGetter() {
      state = 0;
      memset(message, 0, sizeof(message));
      strcat(message, "Long Press 1 to Start!");
      char_index = 0;
      scrolling_timer = millis();
    }
    void reset(){
      state = 0;
      memset(message, 0, sizeof(message));
      strcat(message, "Long Press 1 to Start!");
      char_index = 0;
      scrolling_timer = millis();
      memset(query_string,0,sizeof(query_string));
    }
    void update(float angle, int button, char* output) {
      //Serial.print(state);
      char holder[20] = {0};
      if(state == 0){
        memset(output, 0, sizeof(output));
        strcat(output, message);
        if(button==2){ //long press
          scrolling_timer = millis();
          state = 1;
        }
      }
      else if(state == 1){
        memset(output, 0, sizeof(output));
        strcat(output, query_string);
        strncpy(holder, alphabet + char_index, 1);
        strcat(output, holder);
        if(button==0){
          if(angle >= angle_threshold){
            if (millis() - scrolling_timer >= scrolling_threshold){
              scrolling_timer = millis();
              char_index = (char_index +1)%27;
              memset(output, 0, sizeof(output));
              strcat(output, query_string);
              memset(holder, 0, sizeof(holder));
              strncpy(holder, alphabet + char_index, 1);
              strcat(output, holder);
            }
          }
          else if(angle <= (-1)*angle_threshold){
            if (millis() - scrolling_timer >=scrolling_threshold){
              scrolling_timer = millis();
              if(char_index > 0){
                char_index =(char_index-1 )%27;
              }
              else{
                char_index = 26;
              }
              memset(output, 0, sizeof(output));
              strcat(output, query_string);
              memset(holder, 0, sizeof(holder));
              strncpy(holder, alphabet + char_index, 1);
              strcat(output, holder);
            }
          }
        }
        if(button == 1){//short press, add new letter to query
          strcat(query_string, holder);
          char_index = 0;
        }
      }
      else if(state == 2){
        memset(output, 0, sizeof(output)); //resets the string
        strcat(output, "Waiting for other players to submit word");
        state = 3;
      }
      else if(state == 3){
        strcat(query_string, "&len=200");
        lookup(query_string, message, 200);
        memset(output, 0, sizeof(output)); //resets the string
        strcat(output, message);
        memset(query_string, 0, sizeof(query_string));
        state = 0;
      }
    }
};
FibbageGetter fibbage; //wikipedia object
FibbageGetter roomInputer;
FibbageGetter userInputer;

Button button1(BUTTON_PIN1); //button object!
Button button2(BUTTON_PIN2);


void setup() {
  // Prepares the Console for Debu
  Serial.begin(115200);
  // Loads the Wifi Module
  load_wifi();
  // Initialize the TFT Screen
  init_tft();
  // Initialize the accelerometer
  init_imu();

  pinMode(BUTTON_PIN1, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);
  primary_timer = millis();
  printStartScreen();
  stateMain = START;
  EEPROM.begin(150);
}

/*----------------------------------
 * read_from_storage Function: Reads the string
 * Arguments:
 *    int start_index: The index of EEPROM to start reading data from
 * Return value:
 *    char*: The resulting charstar
 */
void read_from_storage (char* output, int start_index=0) {
  // Empty the input
  output[0] = '\0';
  // Begin reading the EEPROM from the index
  int index = start_index;
  while (EEPROM.read(index) != 255){
    char temp[5] = {(char) EEPROM.read(index)};
    strcat(output,temp);
    index++;
  }
}

/*----------------------------------
 * save_to_storage Function: Reads the string
 * Arguments:
 *    char* word: The word to store to the memory
 *    int start_index: The index of EEPROM to start saving the data to
 * Return value:
 *    char*: The resulting char array
 */
void save_to_storage (char* input_string, int start_index=0) {
  // Saves the Token
  for(int i = start_index; i < strlen(input_string) + start_index;i++) {
    EEPROM.write(i, (uint8_t) response [i - start_index]);
    EEPROM.commit();
  }
  // Write a blank at the end so you can use the read_from_storae
  EEPROM.write(strlen(input_string) + start_index, 255);
  EEPROM.commit();
}


void loop() {
  // Load the Inputs to the Finite State Machine
  float x, y;
  get_angle(&x, &y); //get angle values
  int btn1 = button1.update(); //get button value
  int btn2 = button2.update();

  char body[100];

  switch(stateMain) {
    case START:
      // Ignore absense of input on the main screen
      if (!btn2 && !btn1)
        break;

      // Read the first word stored in the memory, save it to old_user
      read_from_storage(storedUser, 0);

      // No old history
      if (strlen(storedUser) == 0) {
        stateMain = INPUTUSER;
        tft.fillScreen(TFT_WHITE);
        tft.setTextSize(1);
        tft.setCursor(3,3);
        tft.println("Input Username:");
        tft.println("1: Select");
        tft.println("2: Submit");
        break;
      }
      // There is history
      stateMain = OLD_USER;

      tft.fillScreen(TFT_WHITE);
      tft.setTextSize(1);
      tft.setCursor(3,3);
      tft.println("Would you like to");
      tft.println("use the name:\n");

      tft.println(storedUser);
      tft.print("\n");
      tft.println("1: Yes");
      tft.println("2: No");

      break;
    case MAIN:
      // When btn 1 clicked, change selection
      if (btn1 == 1){
        choiceMain = (choiceMain+1) % 2;
        printMenu (choiceMain);
        break;
      }
      // When btn 2 clicked, confirm selection
      if (btn2 == 1) {
        // Enter the Create State
        if (choiceMain == 0) {
          stateMain = CREATE;
          isUserHost = true;
          tft.setCursor(3,3);
          tft.print("Fetching room key...");
        }
        // Enter the Join State
        else {
          stateMain = JOIN;
          tft.fillScreen(TFT_WHITE);
          tft.setTextSize(2);
          tft.setCursor(5,3);
          tft.println("Input Key:");
          tft.setTextSize(1);
          tft.setCursor(3,80);
          tft.println("1: Select");
          tft.setCursor(3,90);
          tft.println("2: Delete");
        }
      }
      break;
    case CREATE:
      tft.fillScreen(TFT_WHITE);

      // POST create a room
      server_post("create_room", "");

      // Saves the for character response to roomKey
      strcpy(roomKey,response);
      memset(response,0,sizeof(response));
      delay(1000);

      roomKey[strlen(roomKey)-1]='\0';

      // Sends a POST request to join the room
      body[0] = '\0';
      add_key(body, "user", user);
      add_key(body, "room_code", roomKey);
      server_post("join_room", body);

      // Transition to the Lobby_Host State
      stateMain = LOBBY_HOST;
      tft.setCursor(35,3);
      tft.setTextSize(2);
      tft.print(roomKey);
      tft.setTextSize(1);
      tft.setCursor(3,20);
      tft.println("Long 1: Start Game");
      break;
    case JOIN:
      if (strlen(roomKey) == 5){
        tft.fillScreen(TFT_WHITE);
        roomKey[strlen(roomKey)-1] = '\0';

        // Sends a POST request to join the room
        body[0] = '\0';
        add_key(body, "user", user);
        add_key(body, "room_code", roomKey);
        server_post("join_room", body);

        // Saves the Token
        for(int i = tokenLocation; i < strlen(response)+tokenLocation;i++){
          EEPROM.write(i,(uint8_t)response[i-tokenLocation]);
          EEPROM.commit();
        }

        // Transition
        stateMain = LOBBY_GUEST;
        tft.setCursor(35,3);
        tft.setTextSize(2);
        tft.print(roomKey);
        tft.setTextSize(1);
        tft.setCursor(3,30);
      }
      else if (btn2 == 1){
        memset(roomKey+(strlen(roomKey)-1),0,1);
        if (strcmp(roomKey,prevRoomKey)){
          tft.fillRect(0,50,128,20,TFT_WHITE);
          tft.setTextSize(2);
          tft.setCursor(30,50);
          tft.print(roomKey);
        }
        memset(prevRoomKey,0,sizeof(prevRoomKey));
        strcat(prevRoomKey,roomKey);
        while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
        primary_timer = millis();
      }
      roomInputer.update(-y,btn1,roomKey);
      if (strcmp(roomKey,prevRoomKey) != 0){
        tft.fillRect(0,50,128,20,TFT_WHITE);
        if (strcmp(roomKey,"Long Press 1 to Start!") != 0){
          tft.setTextSize(2);
          tft.setCursor(30,50);
        }
        else {
          tft.setTextSize(1);
          tft.setCursor(3,50);
        }

        tft.print(roomKey);
        tft.setTextSize(1);
      }

      memset(prevRoomKey,0,sizeof(prevRoomKey));
      strcat(prevRoomKey,roomKey);
      while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
      primary_timer = millis();
      break;
    case LOBBY_HOST:
      if ((millis() - last_post) > lobby_timer){
        memset(response,0,sizeof(response));
        last_post = millis();

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';
        // GET request to check the list
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("list_players", body);

        char * pointer;
        num_players = 0;
        char output[100];
        pointer = strtok(response,",");
        tft.setCursor(0,30);
        while (pointer != NULL) {
          memset(output,0,sizeof(output));
          num_players++;
          sprintf(output,"%d: %s",num_players,pointer);
          tft.println(output);
          pointer = strtok(NULL,",");
        }
      }

      if (btn1 == 2){
        stateMain = BLUFFING;

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';

        // Sends the Start Game Action
        body[0] = '\0';
        sprintf(body,"room_code=%s",roomKey);
        server_post("start_game", body);

        // Sends a request to the same room for the current prompt
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("current_prompt", body);

        tft.fillScreen(TFT_WHITE);
        tft.setCursor(3,3);
        tft.print("Round: ");
        tft.println(roundNumber);
        tft.println(response);
        tft.println("Input Response:");
        tft.println("1: select");
        tft.println("2: submit");
      }
      break;
    case LOBBY_GUEST:
      if ((millis() - last_post) > lobby_timer){
        memset(response,0,sizeof(response));
        last_post = millis();

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';

        // Sends the list_players Request
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("list_players", body);

        char * pointer;
        num_players = 0;
        char output[100];
        pointer = strtok(response,",");
        tft.setCursor(0,30);
        while (pointer != NULL) {
          memset(output,0,sizeof(output));
          num_players++;
          sprintf(output,"%d: %s",num_players,pointer);
          tft.println(output);
          pointer = strtok(NULL,",");
        }

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';

        // Sends a Get Request to check if in lobby
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("in_lobby", body);

        if (strcmp(response,"false") == 0){
          stateMain = BLUFFING;

          // Remove trailing white space from the room key
          if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
            roomKey[strlen(roomKey)-1] = '\0';

          // Sends the Current Prompt Request
          body[0] = '\0';
          add_key(body, "room_code", roomKey);
          server_get("current_prompt", body);

          tft.fillScreen(TFT_WHITE);
          tft.setCursor(3,3);
          memset(old_prompt,0,sizeof(old_prompt));
          strcpy(old_prompt,response);
          tft.print("Round: ");
          tft.println(roundNumber);
          tft.println(response);
          tft.println("Input Response:");
          tft.println("1: select");
          tft.println("2: submit");

        }
      }
      break;
    case BLUFFING:
      if(millis()-last_post > 1000){
        last_post = millis();
        submission_timer= submission_timer-1;
      }

      fibbage.update(-y,btn1,submission);
      if (strcmp(submission,old_submission) != 0){
        tft.fillRect(0,50,128,20,TFT_WHITE);
        tft.setTextSize(1);
        tft.setCursor(3,50);
        tft.print(submission);
      }

      tft.setCursor(0,130);
      tft.print(submission_timer);

      memset(old_submission,0,sizeof(old_submission));
      strcat(old_submission,submission);
      while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
      primary_timer = millis();


      if (btn2 == 1 || submission_timer <=0){
        submission_timer = 60;
        stateMain = WAITINGSUBMISSION;

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';
        // Sends a Submit Bluff request
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        add_key(body, "user", user);
        add_key(body, "bluff", submission);
        server_post("submit_bluff", body);

        tft.fillScreen(TFT_WHITE);
        tft.setCursor(3,10);
        tft.println(response);
        last_post=millis();
      }
      break;
    case INPUTUSER:
      userInputer.update(-y,btn1,user);
      if (strcmp(user,old_user) != 0){
        tft.fillRect(0,50,128,20,TFT_WHITE);
        tft.setTextSize(1);
        tft.setCursor(3,50);
        tft.print(user);
      }

      if (btn2 == 1){
        user[strlen(user)-1]='\0';

        for (int i =0; i < strlen(user);i++){
          EEPROM.write(i,(uint8_t)user[i]);
          EEPROM.commit();
        }

        stateMain = MAIN;
        tft.fillScreen(TFT_WHITE);
        tft.setTextSize(2);
        tft.setCursor(10,3);
        tft.println("Main Menu");
        tft.setTextSize(1);
        printMenu(choiceMain);
      }
      memset(old_user,0,sizeof(old_user));
      strcat(old_user,user);
      while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
      primary_timer = millis();
      break;
    case VOTE:

      if(millis() - last_post > 1000){
        last_post = millis();
        submission_timer= submission_timer-1;
      }

      if (btn1 == 1){
        choice_vote = choice_vote-1;
        if (choice_vote == 0){
          choice_vote = num_players;
        }
      }
      else if (btn2 == 1){
        choice_vote = choice_vote +1;
        if (choice_vote > num_players){
          choice_vote = 1;
        }
      }
      tft.setCursor(0,10*num_players+60);
      tft.print("Vote: ");
      tft.println(choice_vote);
      tft.setCursor(0,130);
      tft.print(submission_timer);

      // On a Long Press, transition to waiting for votes
      if (btn1 == 2){
        submission_timer = 60;
        stateMain = WAITINGVOTES;

        // Convert the choice into string format
        char choice[6];
        sprintf(choice, "%d", choice_vote-1);

        // Remove trailing white space from the room key
        if(strlen(roomKey) == 5) roomKey[strlen(roomKey)-1] = '\0';

        // Sends the choice to the server as a post request
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        add_key(body, "user", user);
        add_key(body, "choice", choice);
        server_post("vote", body);

        tft.fillScreen(TFT_WHITE);
        tft.setCursor(3,10);
        tft.println(response);
        last_post = millis();
      }
      break;
    case WAITINGVOTES:
      if ((millis() - last_post) > lobby_timer){
        last_post = millis();

        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';

        // Checks if we are waiting for votes
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("waiting_for_votes", body);

        if (strcmp(response,"false") == 0 && roundNumber < 7){
          stateMain = BLUFFING;

          // Remove trailing white space from the room key
          if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
            roomKey[strlen(roomKey)-1] = '\0';

          // GET the current_prompt
          body[0] = '\0';
          add_key(body, "room_code", roomKey);
          server_get("current_prompt", body);

          roundNumber++;
          tft.fillScreen(TFT_WHITE);
          tft.setCursor(3,3);
          tft.print("Round: ");
          tft.println(roundNumber);
          tft.println(response);
          tft.println("Input Response:");
          tft.println("1: select");
          tft.println("2: submit");
          fibbage.reset();
          memset(submission,0,sizeof(submission));
        }

        else if (strcmp(response,"false") == 0 && roundNumber == 7){

          // Remove trailing white space from the room key
          if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
            roomKey[strlen(roomKey)-1] = '\0';

          // Checks if we are waiting for votes
          body[0] = '\0';
          add_key(body, "room_code", roomKey);
          server_get("score_rank", body);

          char players[20][20];
          int scores[20];
          char * pointer;
          int index = 0;
          int player_num = 0;
          char temp[20];
          stateMain = RESTART;
          Serial.println(response);
          pointer = strtok(response,",");
          while (pointer != NULL)
          {
            player_num++;
            memset(temp,0,sizeof(temp));
            sprintf(temp,"%s",pointer);
            strcpy(players[index],temp);
            Serial.println(pointer);
            pointer = strtok(NULL,",");
            Serial.println(pointer);
            scores[index] = atoi(pointer);
            pointer = strtok(NULL,",");
            index++;
          }
          tft.fillScreen(TFT_WHITE);
          printScoreScreen(player_num,scores,players);
          tft.setCursor(0,120);
          tft.println("Play Again?");
          tft.println("Yes: 1");
          tft.println("No: unplug me idk");
        }
      }
      break;
    case WAITINGSUBMISSION:
      if ((millis() - last_post) > lobby_timer){
        last_post = millis();


        // Remove trailing white space from the room key
        if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
          roomKey[strlen(roomKey)-1] = '\0';

        // GET waiting_for_submissions
        body[0] = '\0';
        add_key(body, "room_code", roomKey);
        server_get("waiting_for_submissions", body);


        if (strcmp(response,"false")==0){
          tft.fillScreen(TFT_WHITE);
          stateMain = VOTE;

          // Remove trailing white space from the room key
          if(strlen(roomKey) > 4 && roomKey[strlen(roomKey)-1] == ' ')
            roomKey[strlen(roomKey)-1] = '\0';

          // GET get_bluffs
          body[0] = '\0';
          add_key(body, "room_code", roomKey);
          add_key(body, "user", user);
          server_get("get_bluffs", body);

          char * pointer;
          int player_num = 0;
          char output[100];
          pointer = strtok(response,",");
          tft.setCursor(0,3);
          tft.println(old_prompt);
          tft.println("Cast your vote");
          tft.println("1: down");
          tft.println("2: up");
          tft.println("Long 1: submit");
          tft.println("");
          while (pointer != NULL)
          {
            memset(output,0,sizeof(output));
            player_num++;
            sprintf(output,"%d: %s",player_num,pointer);
            tft.println(output);
            pointer = strtok(NULL,",");
          }
        }
      }
      break;
    case OLD_USER:
      if (btn1 == 1){
        memset(user,0,sizeof(user));
        strcpy(user,storedUser);
        stateMain = MAIN;
        tft.fillScreen(TFT_WHITE);
        tft.setTextSize(2);
        tft.setCursor(10,3);
        tft.println("Main Menu");
        tft.setTextSize(1);
        printMenu(choiceMain);
      }
      if (btn2 == 1){
        stateMain = INPUTUSER;
        tft.fillScreen(TFT_WHITE);
        tft.setTextSize(1);
        tft.setCursor(3,3);
        tft.println("Input Username:");
        tft.println("1: Select");
        tft.println("2: Submit");
      }
      break;
    case RESTART:
      if (btn1 == 1 && isUserHost){
        roundNumber = 1;
        stateMain = LOBBY_HOST;
        tft.setCursor(35,3);
        tft.setTextSize(2);
        tft.print(roomKey);
        tft.setTextSize(1);
        tft.setCursor(3,20);
        tft.println("Long 1: Start Game");
      }
      else if(btn1 == 1 && !isUserHost){
        roundNumber = 1;
        stateMain = LOBBY_GUEST;
        tft.setCursor(35,3);
        tft.setTextSize(2);
        tft.print(roomKey);
        tft.setTextSize(1);
      }
      break;
  }
}
