"""Execute selected real .hd functions with mocked LEDs; no ASR SDK/hardware.

Requires clang's wasm32 target, a C++11 sysroot and Node.js. Generated files
are written only to --output-dir (or a dedicated temporary directory).
"""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile


def function(source, name):
    m = re.search(r'(?:void|int|bool)\s+' + name + r'\([^;]*?\)\s*\{', source)
    start = m.start(); end = m.end(); depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def run(args, out):
    root = Path(__file__).parents[1] / 'src/asrpro_firmware/tianwen_block_projects'
    snake = (root/'贪吃蛇.hd').read_text(encoding='utf-8')
    final = (root/'最终版本.hd').read_text(encoding='utf-8')
    # Use the source's delay declarations, not a parallel timing implementation.
    delays = '\n'.join('{' + x + '}' for x in re.findall(r'uint16_t frameDelay\[\].*?;', final))
    assert delays.count('frameDelay') == 3
    pre = r'''
#include <stdint.h>
extern "C" void *memset(void *p,int v, unsigned long n) {
  unsigned char *q=(unsigned char*)p; for(unsigned long i=0;i<n;i++)q[i]=(unsigned char)v;return p;
}
int snakeX[256],snakeY[256],snakeLength,dx,dy,foodX,foodY,score;
bool gameStarted,gameOver;
char pendingDirection = 0;
int rand(){return 12345;}
void showScore(){}
void flashRed(){}
struct LEDs {
  int seen[256] = {}; bool bad=false;
  void pixel_clear(){} void pixel_show(){} void setBrightness(int){}
  void pixel_set_all_color(int,int,int){}
  void pixel_set_color(int i,int r,int g,int b) {
    if(i<0 || i>=256){bad=true;return;} ++seen[i];
  }
} ASR_WS2812_2;
'''
    core = '\n'.join(function(snake,n) for n in ('getPixelIndex','isOnSnake','generateFood','drawSnake','moveSnake'))
    rgb = function(final,'displaycolorfulPattern')
    tests = r'''
extern "C" int run_tests() {
  // All pixel indices are in range and distinct.
  bool seen[256]={};
  for(int y=0;y<16;y++)for(int x=0;x<16;x++){
    int i=getPixelIndex(x,y); if(i<0||i>=256||seen[i])return 1;seen[i]=true;
  }
  unsigned char image[16][16]={}; displaycolorfulPattern(image,image,image);
  if(ASR_WS2812_2.bad)return 2;
  for(int i=0;i<256;i++)if(ASR_WS2812_2.seen[i]!=1)return 3;
  // Exactly one free cell; full board must terminate without random retries.
  snakeLength=255;
  for(int i=0;i<255;i++){snakeX[i]=i%16;snakeY[i]=i/16;}
  if(!generateFood() || foodX!=15 || foodY!=15)return 4;
  snakeX[255]=15;snakeY[255]=15;snakeLength=256;
  if(generateFood())return 5;
  // Growing to capacity preserves the old tail and ends play.
  snakeLength=255;snakeX[0]=14;snakeY[0]=15;
  for(int i=0;i<254;i++){snakeX[i+1]=i%16;snakeY[i+1]=i/16;}
  dx=1;dy=0;foodX=15;foodY=15;score=0;gameStarted=true;gameOver=false;
  moveSnake();if(snakeLength!=256||gameStarted||!gameOver||score!=1)return 6;
  // Multiple inputs in one tick cannot reverse the last committed direction.
  snakeLength=3;snakeX[0]=4;snakeY[0]=4;snakeX[1]=3;snakeY[1]=4;snakeX[2]=2;snakeY[2]=4;
  dx=1;dy=0;foodX=10;foodY=10;__atomic_store_n(&pendingDirection, 'W', __ATOMIC_SEQ_CST);__atomic_store_n(&pendingDirection, 'A', __ATOMIC_SEQ_CST);
  moveSnake();if(dx!=1||dy!=0||snakeX[0]!=5)return 7;
  return 0;
}
'''
    out.mkdir(parents=True, exist_ok=True)
    cpp=out/'logic.cpp';wasm=out/'logic.wasm'
    cpp.write_text(pre+core+rgb+'\nvoid check_delays(){'+delays+'}\n'+tests,encoding='utf-8')
    env=os.environ.copy();env['TMP']=env['TEMP']=str(out.resolve())
    subprocess.run([args.clang,'--target=wasm32','-std=c++11','-fno-builtin','-nostdlib','-nostdinc++',
                    '--sysroot='+args.sysroot,
                    '-Wl,--no-entry','-Wl,--export=run_tests',str(cpp),'-o',str(wasm)],check=True,env=env)
    js='WebAssembly.instantiate(require("fs").readFileSync(process.argv[1])).then(x=>{let n=x.instance.exports.run_tests();console.log({cases:7,failedCase:n});process.exitCode=n;})'
    subprocess.run([args.node,'-e',js,str(wasm)],check=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--clang',required=True);p.add_argument('--sysroot',required=True);p.add_argument('--node',default='node');p.add_argument('--output-dir')
    a=p.parse_args()
    if a.output_dir:run(a,Path(a.output_dir))
    else:
        with tempfile.TemporaryDirectory(prefix='lighting-basic-tests-') as t:run(a,Path(t))
