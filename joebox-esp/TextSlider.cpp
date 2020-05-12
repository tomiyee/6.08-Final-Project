#include "Arduino.h"
#include "TextSlider.h"

TextSlider::TextSlider () {
  state = 0;
  char_index = 0;
  scrolling_timer = millis();
}

void TextSlider::update (float angle, int a_button, int b_button, char* output) {
  // Short Press, append the char
  if (a_button == 1) {
    sprintf(output, "%s%c", query_string, alphabet[char_index]);
    sprintf(query_string, "%s",output);
    char_index = 0;
    return;
  }
  // Short press b, delete the most recent char
  if (b_button == 1)
    query_string[strlen(query_string)-1] = '\0';

  // Increment or decrement the char index appropriately
  if (abs(angle) > angle_threshold && millis() - scrolling_timer >= scrolling_threshold) {
    if (angle > 0)
      char_index += 1;
    if (angle < 0)
      char_index -= 1;
    // Loop Around
    char_index = ( char_index + strlen(alphabet) ) % strlen(alphabet);
    scrolling_timer = millis();
  }
  sprintf(output, "%s%c", query_string, alphabet[char_index]);
}

void TextSlider::getValue (char* output) {
  sprintf(output, "%s", query_string);
}

void TextSlider::reset () {
  query_string[0] = '\0';
}
