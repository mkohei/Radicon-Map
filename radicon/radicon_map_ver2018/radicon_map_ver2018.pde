// Constants
final float RADICON_R = 100;
final float TARGET_R = 100;

final int TARGET_NUM = 50;
final int TARGET_INTERVAL = 30;
final int TARGET_LIFE = 400;
final int TARGET_HIGH_RATE = 6;

final int GAME_TIME = TARGET_NUM * TARGET_INTERVAL + TARGET_LIFE/4;

// Variables
RadiconMove rm;
TargetController tc;
float[] point;

int count;
int game_point;

void setup() {
  //fullScreen();
  size(1000, 600);
  
  count = 0;
  game_point = 0;
  
  rm = new RadiconMove();
  tc = new TargetController(TARGET_NUM, TARGET_INTERVAL, TARGET_LIFE, TARGET_HIGH_RATE);
}



void draw() {
  background(255);
  
  tc.product();
  tc.show();
  
  point = rm.move();
  
  noStroke();
  fill(255, 0, 0, 100);
  ellipse(point[0], point[1], RADICON_R, RADICON_R);
  
  show_gametime_arc();
  
  game_point += tc.collision(point[0], point[1]);
  println(game_point);
  
  count++;
  if (count == GAME_TIME) println("end");
}



void show_gametime_arc() {
  noStroke();
  fill(0, 255, 0, 200);
  arc(width-70, 0+70, TARGET_R, TARGET_R, -2*PI*(GAME_TIME-count)/GAME_TIME - HALF_PI, -HALF_PI);
}


// finish by ESC
void keyPressed() {
  if (key == 27) exit();
}