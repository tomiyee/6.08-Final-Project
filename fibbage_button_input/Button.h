#ifndef Button_h
#define Button_h
#include "Arduino.h"

//button class object that returns a flag 
//returns 1 for completed short press and 2 for completed long press

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

#endif
