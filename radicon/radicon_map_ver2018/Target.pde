class Target {
  static final int P1 = 1;
  static final int P5 = 5;
  
  final float x, y;
  final int point;
  final int lifespan;
  int life;
  
  Target(float _x, float _y, int _life, int _point) {
    this.x = _x;
    this.y = _y;
    this.lifespan = _life;
    this.life = _life;
    this.point = _point;
  }
  
  boolean dead() {
    return life <= 0;
  }
  
  void grow() {
    if (dead()) return;
    life--;
  }
  
  void show() {
    if (dead()) return;
    
    if (this.point == P1) stroke(255, 255, 0, 200);
    else if (this.point == P5) stroke(255, 0, 255, 200);
    else {
    }
    strokeWeight(10);
    noFill();
    ellipse(x, y, TARGET_R, TARGET_R);
    
    if (this.point == P1) fill(255, 255, 0, 200);
    else if (this.point == P5) fill(255, 0, 255, 200);
    else {
    }
    noStroke();
    arc(x, y, TARGET_R, TARGET_R, -2*PI*life/lifespan - HALF_PI, -HALF_PI);
  }
  
  int collision(float rx, float ry) {
    if (dead()) return 0;
    if ( pow(this.x-rx, 2) + pow(this.y-ry, 2) < pow(RADICON_R/2+TARGET_R/2, 2)) {
      this.life =  0;
      return this.point;
    }
    return 0;
  }
}
  
  