
#include <TFT_eSPI.h>

void printStartScreen(){
  tft.fillScreen(TFT_WHITE);  
  drawB();
  drawL1();
  drawU();
  drawF1();
  drawF2();
  drawA();
  drawL2();
  drawSnout();
  drawO();
  drawDetails();
  drawOutline();
  drawBody();
  tft.setCursor(22,140);
  tft.println("Press to start");
}


//numPlayers: an integer with the number of players
//scores, an array with the scores of each player where sizeof(scores) = numPlayers
//        and scores[0] is the score of player 0.
//users, a 2d array where user[0] is the name of player 0.
void printScoreScreen(int numPlayers,int* scores,char users[][20]){
  uint16_t colors[5] = {TFT_GREEN,TFT_BLUE,TFT_RED,TFT_YELLOW,TFT_BLACK};
  int highest = 100;
  for (int i =0; i< numPlayers;i++){
    if (scores[i] > highest){
      highest = scores[i];
    }
  }
  
  tft.setTextColor(TFT_BLACK);
  for (int i = 0; i < numPlayers;i++){
    tft.setCursor(0,i*30 + 1,1);
    tft.print(users[i]);
    tft.print(": ");
    tft.println(scores[i]);
    tft.println("\n\n");
    int ypos = i*30+10;
    
    int len = (int)(((float)scores[i]/(float)highest)*115);
    Serial.println(scores[i]);
    Serial.println(len);
    tft.drawRect(0,ypos,len,20,colors[i%6]);
    tft.fillRect(0,ypos,len,20,colors[i%6]);
  }


  

}



void drawPixelScaled(int x,int y,uint16_t color){
  int realX = x * 4;
  int realY = y * 4;
  
  for(int i = realX;i < realX+4;i++){
    for(int j = realY;j < realY+4;j++){
      tft.drawPixel(i,j,color);
    }
  }
}

void drawB(){
  drawPixelScaled(1,2,TFT_BLACK);
  drawPixelScaled(2,2,TFT_BLACK);
  drawPixelScaled(3,2,TFT_BLACK);
  drawPixelScaled(4,2,TFT_BLACK);
  drawPixelScaled(5,3,TFT_BLACK);
  drawPixelScaled(4,4,TFT_BLACK);
  drawPixelScaled(5,5,TFT_BLACK);
  drawPixelScaled(4,6,TFT_BLACK);
  drawPixelScaled(3,6,TFT_BLACK);
  drawPixelScaled(2,6,TFT_BLACK);
  drawPixelScaled(1,6,TFT_BLACK);
  drawPixelScaled(1,5,TFT_BLACK);
  drawPixelScaled(1,4,TFT_BLACK);
  drawPixelScaled(1,3,TFT_BLACK);
}


void drawL1(){
  drawPixelScaled(7,2,TFT_BLACK);
  drawPixelScaled(7,3,TFT_BLACK);
  drawPixelScaled(7,4,TFT_BLACK);
  drawPixelScaled(7,5,TFT_BLACK);
  drawPixelScaled(7,6,TFT_BLACK);
}

void drawU(){
  drawPixelScaled(9,4,TFT_BLACK);
  drawPixelScaled(9,5,TFT_BLACK);
  drawPixelScaled(10,6,TFT_BLACK);
  drawPixelScaled(11,6,TFT_BLACK);
  drawPixelScaled(11,5,TFT_BLACK);
  drawPixelScaled(11,4,TFT_BLACK);
}

void drawF1(){
  drawPixelScaled(15,2,TFT_BLACK);
  drawPixelScaled(14,2,TFT_BLACK);
  drawPixelScaled(13,3,TFT_BLACK);
  drawPixelScaled(13,4,TFT_BLACK);
  drawPixelScaled(14,4,TFT_BLACK);
  drawPixelScaled(13,5,TFT_BLACK);
  drawPixelScaled(13,6,TFT_BLACK);
}

void drawF2(){
  drawPixelScaled(19,2,TFT_BLACK);
  drawPixelScaled(18,2,TFT_BLACK);
  drawPixelScaled(17,3,TFT_BLACK);
  drawPixelScaled(17,4,TFT_BLACK);
  drawPixelScaled(18,4,TFT_BLACK);
  drawPixelScaled(17,5,TFT_BLACK);
  drawPixelScaled(17,6,TFT_BLACK);
}

void drawA(){
  drawPixelScaled(22,2,TFT_BLACK);
  drawPixelScaled(23,2,TFT_BLACK);
  drawPixelScaled(24,3,TFT_BLACK);
  drawPixelScaled(24,4,TFT_BLACK);
  drawPixelScaled(23,4,TFT_BLACK);
  drawPixelScaled(22,4,TFT_BLACK);
  drawPixelScaled(21,5,TFT_BLACK);
  drawPixelScaled(22,6,TFT_BLACK);
  drawPixelScaled(23,6,TFT_BLACK);
  drawPixelScaled(24,5,TFT_BLACK);
  drawPixelScaled(24,6,TFT_BLACK);
}


void drawL2(){
  drawPixelScaled(26,2,TFT_BLACK);
  drawPixelScaled(26,3,TFT_BLACK);
  drawPixelScaled(26,4,TFT_BLACK);
  drawPixelScaled(26,5,TFT_BLACK);
  drawPixelScaled(26,6,TFT_BLACK);
}

void drawO(){
  drawPixelScaled(28,3,TFT_BLACK);
  drawPixelScaled(28,4,TFT_BLACK);
  drawPixelScaled(28,5,TFT_BLACK);
  drawPixelScaled(28,6,TFT_BLACK);
  drawPixelScaled(29,3,TFT_BLACK);
  drawPixelScaled(29,6,TFT_BLACK);
  drawPixelScaled(30,3,TFT_BLACK);
  drawPixelScaled(30,4,TFT_BLACK);
  drawPixelScaled(30,5,TFT_BLACK);
  drawPixelScaled(30,6,TFT_BLACK);
}

void drawOutline(){
  drawPixelScaled(2,20,0x1861);
  drawPixelScaled(2,21,0x1861);
  drawPixelScaled(2,22,0x1861);
  drawPixelScaled(2,23,0x1861);
  drawPixelScaled(2,24,0x1861);
  drawPixelScaled(3,23,0x1861);
  drawPixelScaled(3,24,0x1861);
  drawPixelScaled(3,25,0x1861);
  drawPixelScaled(4,25,0x1861);
  drawPixelScaled(5,25,0x1861);
  drawPixelScaled(6,25,0x1861);
  drawPixelScaled(7,25,0x1861);
  drawPixelScaled(7,24,0x1861);
  drawPixelScaled(7,23,0x1861);
  drawPixelScaled(8,25,0x1861);
  drawPixelScaled(8,24,0x1861);
  drawPixelScaled(8,23,0x1861);
  drawPixelScaled(8,26,0x1861);
  drawPixelScaled(8,27,0x1861);
  drawPixelScaled(8,28,0x1861);
  drawPixelScaled(9,27,0x1861);
  drawPixelScaled(9,28,0x1861);
  drawPixelScaled(9,29,0x1861);
  drawPixelScaled(9,30,0x1861);
  drawPixelScaled(9,31,0x1861);
  drawPixelScaled(9,32,0x1861);
  drawPixelScaled(10,28,0x1861);
  drawPixelScaled(10,32,0x1861);
  drawPixelScaled(11,32,0x1861);
  drawPixelScaled(11,31,0x1861);
  drawPixelScaled(11,30,0x1861);
  drawPixelScaled(13,30,0x1861);
  drawPixelScaled(14,30,0x1861);
  drawPixelScaled(14,29,0x1861);
  drawPixelScaled(14,28,0x1861);
  drawPixelScaled(14,31,0x1861);
  drawPixelScaled(14,32,0x1861);
  drawPixelScaled(15,30,0x1861);
  drawPixelScaled(15,31,0x1861);
  drawPixelScaled(15,32,0x1861);
  drawPixelScaled(16,30,0x1861);
  drawPixelScaled(17,30,0x1861);
  drawPixelScaled(18,30,0x1861);
  drawPixelScaled(19,30,0x1861);
  drawPixelScaled(20,30,0x1861);
  drawPixelScaled(21,29,0x1861);
  drawPixelScaled(21,30,0x1861);
  drawPixelScaled(22,30,0x1861);
  drawPixelScaled(22,31,0x1861);
  drawPixelScaled(22,32,0x1861);
  drawPixelScaled(23,30,0x1861);
  drawPixelScaled(23,31,0x1861);
  drawPixelScaled(23,32,0x1861);
  drawPixelScaled(25,30,0x1861);
  drawPixelScaled(25,31,0x1861);
  drawPixelScaled(25,32,0x1861);
  drawPixelScaled(26,30,0x1861);
  drawPixelScaled(26,31,0x1861);
  drawPixelScaled(26,32,0x1861);
  drawPixelScaled(23,29,0x1861);
  drawPixelScaled(24,29,0x1861);
  drawPixelScaled(25,29,0x1861);
  drawPixelScaled(26,29,0x1861);
  drawPixelScaled(25,28,0x1861);
  drawPixelScaled(26,28,0x1861);
  drawPixelScaled(25,27,0x1861);
  drawPixelScaled(26,27,0x1861);
  drawPixelScaled(26,26,0x1861);
  drawPixelScaled(27,26,0x1861);
  drawPixelScaled(27,27,0x1861);
  drawPixelScaled(27,25,0x1861);
  drawPixelScaled(27,24,0x1861);
  drawPixelScaled(28,24,0x1861);
  drawPixelScaled(28,23,0x1861);
  drawPixelScaled(28,22,0x1861);
  drawPixelScaled(28,21,0x1861);
  drawPixelScaled(27,18,0x1861);
  drawPixelScaled(28,18,0x1861);
  drawPixelScaled(27,19,0x1861);
  drawPixelScaled(27,20,0x1861);
  drawPixelScaled(28,19,0x1861);
  drawPixelScaled(28,20,0x1861);
  drawPixelScaled(26,16,0x1861);
  drawPixelScaled(27,16,0x1861);
  drawPixelScaled(26,17,0x1861);
  drawPixelScaled(27,17,0x1861);
  drawPixelScaled(26,18,0x1861);
  drawPixelScaled(26,14,0x1861);
  drawPixelScaled(26,15,0x1861);
  drawPixelScaled(25,15,0x1861);
  drawPixelScaled(25,13,0x1861);
  drawPixelScaled(14,12,0x1861);
  drawPixelScaled(15,12,0x1861);
  drawPixelScaled(16,12,0x1861);
  drawPixelScaled(17,12,0x1861);
  drawPixelScaled(18,12,0x1861);
  drawPixelScaled(19,12,0x1861);
  drawPixelScaled(20,12,0x1861);
  drawPixelScaled(21,12,0x1861);
  drawPixelScaled(22,12,0x1861);
  drawPixelScaled(23,12,0x1861);
  drawPixelScaled(24,12,0x1861);
  drawPixelScaled(12,13,0x1861);
  drawPixelScaled(13,13,0x1861);
  drawPixelScaled(12,14,0x1861);
  drawPixelScaled(13,14,0x1861);
  drawPixelScaled(14,14,0x1861);
  drawPixelScaled(10,14,0x1861);
  drawPixelScaled(11,14,0x1861);
  drawPixelScaled(10,15,0x1861);
  drawPixelScaled(11,15,0x1861);
  drawPixelScaled(12,15,0x1861);
  drawPixelScaled(8,15,0x1861);
  drawPixelScaled(9,15,0x1861);
  drawPixelScaled(8,16,0x1861);
  drawPixelScaled(9,16,0x1861);
  drawPixelScaled(7,15,0x1861);
  drawPixelScaled(6,15,0x1861);
  drawPixelScaled(5,16,0x1861);
  drawPixelScaled(4,17,0x1861);
  drawPixelScaled(3,17,0x1861);
  drawPixelScaled(3,18,0x1861);
  drawPixelScaled(3,19,0x1861);
  drawPixelScaled(13,17,0x1861);
  drawPixelScaled(10,18,0x1861);
  drawPixelScaled(11,18,0x1861);
  drawPixelScaled(12,18,0x1861);
  drawPixelScaled(1,14,0x1861);
  drawPixelScaled(2,14,0x1861);
  drawPixelScaled(3,14,0x1861);
  drawPixelScaled(4,15,0x1861);
  drawPixelScaled(1,15,0x1861);
  drawPixelScaled(2,16,0x1861);

  drawPixelScaled(4,19,0x0000);
  drawPixelScaled(8,19,0x0000);
}

void drawBody(){
  for(int i = 10;i < 25;i++){
    for(int j = 19;j<28;j++){
      drawPixelScaled(i,j,0x6A68);
    }
  }
  for(int i =15;i < 25;i++){
    for(int j = 13;j<19;j++){
      drawPixelScaled(i,j,0x6A68);
    }
  }

  for(int i =25;i < 27;i++){
    for(int j = 19;j<26;j++){
      drawPixelScaled(i,j,0x6A68);
    }
  }

  for(int i =15;i < 21;i++){
    for(int j = 28;j<30;j++){
      drawPixelScaled(i,j,0x6A68);
    }
  }

  for(int i =7;i < 10;i++){
    for(int j = 21;j<23;j++){
      drawPixelScaled(i,j,0x6A68);
    }
  }
  drawPixelScaled(4,22,0x6A68);
  drawPixelScaled(6,22,0x6A68);  
  drawPixelScaled(9,20,0x6A68);  

  for(int j = 23;j<27;j++){
      drawPixelScaled(9,j,0x6A68);
  }

  for(int i = 21;i<25;i++){
      drawPixelScaled(i,28,0x6A68);
  }

  for(int i = 11;i<14;i++){
      drawPixelScaled(i,28,0x6A68);
  }

  for(int i = 21;i<24;i++){
      drawPixelScaled(27,i,0x6A68);
  }

  for(int i = 16;i<19;i++){
      drawPixelScaled(25,i,0x6A68);
  }

  for(int i = 16;i<19;i++){
      drawPixelScaled(14,i,0x6A68);
  }

  drawPixelScaled(14,13,0x6A68);
  drawPixelScaled(25,14,0x6A68);
  drawPixelScaled(13,18,0x6A68);
  drawPixelScaled(13,29,0x6A68);
  drawPixelScaled(22,29,0x6A68);
  drawPixelScaled(25,26,0x6A68);
}



void drawDetails(){
  for(int i =6;i < 8;i++){
    for(int j = 16;j<21;j++){
      drawPixelScaled(i,j,0x5A06);
    }
  }
  for(int j = 18;j<21;j++){
      drawPixelScaled(8,j,0x5A06);
  }
  for(int j = 29;j<32;j++){
      drawPixelScaled(10,j,0x5A06);
  }

  for(int i = 4;i<7;i++){
      drawPixelScaled(i,24,0x5A06);
      drawPixelScaled(i,23,0x5A06);
  }

  
  for(int j = 17;j<21;j++){
      drawPixelScaled(5,j,0x5A06);
  }

  drawPixelScaled(4,18,0x5A06);
  drawPixelScaled(3,20,0x5A06);
  drawPixelScaled(4,20,0x5A06);
  drawPixelScaled(11,29,0x5A06);
  drawPixelScaled(12,29,0x5A06);
  drawPixelScaled(12,30,0x5A06);
}

void drawSnout(){
  for(int i =3;i < 7;i++){
    for(int j = 21;j<23;j++){
      drawPixelScaled(i,j,0x7AA9);
    }
  }
}
