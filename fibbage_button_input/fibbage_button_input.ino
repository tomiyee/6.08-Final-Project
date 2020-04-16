amn #include <WiFi.h> //Connect to WiFi Network
#include <SPI.h>
#include <TFT_eSPI.h>
#include <mpu6050_esp32.h>
#include<math.h>
#include<string.h>

TFT_eSPI tft = TFT_eSPI();
const int SCREEN_HEIGHT = 160;
const int SCREEN_WIDTH = 128;
const int BUTTON_PIN = 5;
const int LOOP_PERIOD = 40;

MPU6050 imu; //imu object called, appropriately, imu

//char network[] = "NetGear_GMCK4";  //SSID 
//char password[] = ""; //Password 

char network[] = "NetGear_GMCK4";  //SSID for 6.08 Lab
char password[] = "gqym1024"; //Password for 6.08 Lab

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char old_response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP request

unsigned long primary_timer;

int old_val;

//used to get x,y values from IMU accelerometer!
void get_angle(float* x, float* y) {
  imu.readAccelData(imu.accelCount);
  *x = imu.accelCount[0] * imu.aRes;
  *y = imu.accelCount[1] * imu.aRes;
}

void lookup(char* query, char* response, int response_size) {
  char request_buffer[200];
  //CHANGE WHERE THIS IS TARGETED! IT SHOULD TARGET YOUR SERVER SCRIPT
  sprintf(request_buffer, "GET /sandbox/sc/person/wiki_getter.py?topic=%s HTTP/1.1\r\n", query);
  strcat(request_buffer, "Host: 608dev-2.net\r\n");
  strcat(request_buffer, "\r\n"); //new line from header to body

  do_http_request("608dev-2.net", request_buffer, response, response_size, RESPONSE_TIMEOUT, true);
}

class Button{
  public:
  uint32_t t_of_state_2;
  uint32_t t_of_button_change;    
  uint32_t debounce_time;
  uint32_t long_press_time;
  uint8_t pin;
  uint8_t flag;
  bool button_pressed;
  uint8_t state; // This is public for the sake of convenience
  Button(int p) {
  flag = 0;  
    state = 0;
    pin = p;
    t_of_state_2 = millis(); //init
    t_of_button_change = millis(); //init
    debounce_time = 10;
    long_press_time = 1000;
    button_pressed = 0;
  }
  void read() {
    uint8_t button_state = digitalRead(pin);  
    button_pressed = !button_state;
  }
  int update() {
    read();
    flag = 0;
    if (state==0) {
      if (button_pressed) {
        state = 1;
        t_of_button_change = millis();
      }
    } else if (state==1) {
      if (!button_pressed){
        state = 0;
        t_of_button_change = millis();
      }
      else if(button_pressed && millis()-t_of_button_change >= debounce_time){
        state = 2;
        t_of_state_2 = millis();
      }
    } else if (state==2) {
      if(button_pressed && millis() - t_of_state_2 >= long_press_time){
        state = 3;
      }
      else if(!button_pressed){
        state = 4;
        t_of_button_change = millis();
      }
    } else if (state==3) {
      if(!button_pressed){
        state = 4;
        t_of_button_change = millis();
      }
    } else if (state==4) {        
      if(!button_pressed && millis()- t_of_button_change >= debounce_time){
        state = 0;
        if(millis() - t_of_state_2 > long_press_time + debounce_time){
          flag = 2;
        }
        else{
          flag = 1;
        }
      }
      else if(button_pressed && millis() - t_of_state_2 < long_press_time){
        state = 2;
        t_of_button_change = millis();
      }
      else if(button_pressed && millis()-t_of_state_2 >= long_press_time){
        state = 3;
        t_of_button_change = millis();
      }
    }
    return flag;
  }
};

class WikipediaGetter {
    char alphabet[50] = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    char message[400] = {0}; //contains previous query response
    char query_string[50] = {0};
    int char_index;
    int state;
    unsigned long scrolling_timer;
    const int scrolling_threshold = 150;
    const float angle_threshold = 0.3;
  public:

    WikipediaGetter() {
      state = 0;
      memset(message, 0, sizeof(message));
      strcat(message, "Long Press to Start!");
      char_index = 0;
      scrolling_timer = millis();
    }
    void update(float angle, int button, char* output) {
      char holder[20] = {0};
      if(state == 0){
        memset(output, 0, sizeof(output));
        strcat(output, message);
        //memset(output, 0, sizeof(output));
        if(button==2){ //long press
          scrolling_timer = millis();
          state = 1;
        }
      }
      else if(state == 1){
        //memset(query_string, 0, 50);
        memset(output, 0, sizeof(output));
        strcat(output, query_string);
        strncpy(holder, alphabet + char_index, 1);
        strcat(output, holder);
        //strcat(output, alphabet[char_index]);
        //Serial.println(alphabet[char_index]);
        if(button==0){
          //Serial.println("hello");
          if(angle >= angle_threshold){
            if (millis() - scrolling_timer >= scrolling_threshold){
              //char_index++;
              scrolling_timer = millis();
              char_index = (char_index +1)%37;
              memset(output, 0, sizeof(output));
              strcat(output, query_string);
              memset(holder, 0, sizeof(holder));
              strncpy(holder, alphabet + char_index, 1);
              strcat(output, holder);
              //strcat(output, &alphabet[char_index]);
            }
          }
          else if(angle <= (-1)*angle_threshold){
            if (millis() - scrolling_timer >=scrolling_threshold){
              scrolling_timer = millis();
              if(char_index > 0){
                char_index =(char_index-1 )%37;
              }
              else{
                char_index = 36;
              }
              memset(output, 0, sizeof(output));
              strcat(output, query_string);
              memset(holder, 0, sizeof(holder));
              strncpy(holder, alphabet + char_index, 1);
              strcat(output, holder);
              //strcat(output, &alphabet[char_index]);
              
            }
          }
        }
        if(button == 1){//short press, add new letter to query
          strcat(query_string, holder);
          //strcat(output, query_string);
          //memset(output, 0, sizeof(output));
          //query_string = query_string + alphabet[char_index];
          char_index = 0;
        }
        else if(button == 2){//long press
          memset(output, 0, sizeof(output));
          state = 2;
        }
      }
      else if(state == 2){
        memset(output, 0, sizeof(output)); //resets the string
        strcat(output, "Sending Query");
        state = 3;
      }
      else if(state == 3){
        strcat(query_string, "&len=200");
        lookup(query_string, message, 200);
        memset(output, 0, sizeof(output)); //resets the string 
        strcat(output, message);
        //Serial.println(message);
        memset(query_string, 0, sizeof(query_string));
        state = 0;  
      }
    }
};

WikipediaGetter wg; //wikipedia object
Button button(BUTTON_PIN); //button object!


void setup() {
  Serial.begin(115200); //for debugging if needed.
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
    Serial.printf("%d:%d:%d:%d (%s) (%s)\n", WiFi.localIP()[3], WiFi.localIP()[2],
                  WiFi.localIP()[1], WiFi.localIP()[0],
                  WiFi.macAddress().c_str() , WiFi.SSID().c_str());    delay(500);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
  if (imu.setupIMU(1)) {
    Serial.println("IMU Connected!");
  } else {
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart(); // restart the ESP (proper way)
  }
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK); //set color of font to green foreground, black background
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  primary_timer = millis();
}

void loop() {
  float x, y;
  get_angle(&x, &y); //get angle values
  int bv = button.update(); //get button value
  wg.update(-y, bv, response); //input: angle and button, output String to display on this timestep
  if (strcmp(response, old_response) != 0) {//only draw if changed!
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(0, 0, 1);
    tft.println(response);
  }
  memset(old_response, 0, sizeof(old_response));
  strcat(old_response, response);
  while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
  primary_timer = millis();
}
