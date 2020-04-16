char* msg = "Lol hi guys";
const int SCREEN_HEIGHT = 160;
const int SCREEN_WIDTH = 128;

#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();
void setup () {
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_WHITE);
}


void loop () {

}
