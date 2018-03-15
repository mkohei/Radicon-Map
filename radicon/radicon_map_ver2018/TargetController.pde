class TargetController {
  Target[] targets;
  
  final int GENERATION_INTERVAL;
  final int LIFE;
  
  int age, order;
  final int RATE_HIGH_POINT;
  
  
  TargetController(int n, int gi, int life, int p5_rate) {
    targets = new Target[n];
    GENERATION_INTERVAL = gi;
    LIFE = life;
    order = 0;
    age = 0;
    
    RATE_HIGH_POINT = p5_rate;
  }
  
  
  void product() {
    for (int i=0; i<order; i++) {
      targets[i].grow();
    }
    
    if (age % GENERATION_INTERVAL == 0) {
      if (order < targets.length) {
        if ((order+1) % RATE_HIGH_POINT == 0) {
          targets[order] = new Target(random(0, width), random(0, height), LIFE, Target.P5);
        } else {
          targets[order] = new Target(random(0, width), random(0, height), LIFE, Target.P1);
        }
      }
      if (order < targets.length) order++;
    }
    age++;
  }
  
  
  int collision(float x, float y) {
    int cnt=0;
    for (int i=0; i<order; i++) {
      cnt += targets[i].collision(x,y);
    }
    return cnt;
  }
  
  
  void show() {
    for (int i=0; i < order; i++) {
      targets[i].show();      
    }
  }
}