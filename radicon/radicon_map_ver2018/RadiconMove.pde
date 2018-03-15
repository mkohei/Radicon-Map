class RadiconMove {
  
  float x, y;
  float vx, vy;
  float ax, ay;
  
  RadiconMove() {
    x = width/2;
    y = height/2;
    vx = 4;
    vy = 4;
    ax = 0;
    ay = 0;
  }
  
  float[] move() {
    vx += ax;
    vy += ay;
    x += vx;
    y += vy;
    if (x >= width || x <= 0) vx *= -1;
    if (y >= height || y <= 0) vy *= -1;
    
    float[] point = {x, y};
    return point;
  }
}