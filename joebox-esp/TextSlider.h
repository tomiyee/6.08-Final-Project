#ifndef TextSlider_h
#define TextSlider_h
#include "Arduino.h"

class TextSlider {
    char alphabet[50] = " ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char query_string[50] = {0};
    int char_index;
    int state;
    unsigned long scrolling_timer;
    const int scrolling_threshold = 150;
    const float angle_threshold = 0.3;
  public:
    TextSlider ();
    void update (float angle, int a_button, int b_button, char* output);
    void getValue (char* output);
};
#endif
