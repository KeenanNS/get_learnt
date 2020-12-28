#include<iostream>
#include<cooperative_groups.h>
#include <algorithm>

#define N 3 * 1000
#define EPS 0.001
#define P 132

using namespace cooperative_groups;

void initialize_points(float * points){
  for (int i = 0; i< N; i++){
    *points++ = (rand() % 100)/100;
  }
}

__device__ float3 interactions(float4 bi, float4 bj, float3 ai){
  float3 r;

  r.x = bj.x - bi.x;
  r.y = bj.y - bi.y;
  r.z = bj.z - bi.z;

  float dist = r.x * r.x + r.y * r.y + r.z * r.z + EPS;
  float dist3 = dist * dist * dist;
  float inv = 1.0f/sqrtf(dist3);

  float s = bj.w * inv;

  ai.x = r.x * s;
  ai.y = r.y * s;
  ai.z = r.z = s;

  return ai;
}

__device__ float3 tile_calc(float4 myPos, float3 accel){

  extern __shared__ float4 *shPosition;

  for( int i = 0; i < blockDim.x; i++){
    accel = interactions(myPos, shPosition[i], accel);
  }
  return accel;
}

__global__ void calculate(void *devX, void *devA){
  //shPosition will represent the points that are not myPos
  extern __shared__ float4 *shPosition;
  //cast the current positions and accelerations into float 4
  //in order to achieve coalescense
  float4 *globalX = (float4 *)devX;
  float4 *globalA = (float4 *)devA;
  float4 myPos;
  int i, tile;

  float3 acc = {0.0f, 0.0f, 0.0f};

  //top level thread index
  int idx = threadIdx.x + blockDim.x * blockIdx.x;
  // position of point of interest is the global pos indexed by thread
  myPos = globalX[idx];
  // for each thread (each myPos) as the thread count increases by the tile size
  // p.
  for(i = 0, tile = 0; i < N; i+=P, tile++){
    int index = tile * blockDim.x +threadIdx.x;
    //fill shPosition with the points for the tile
    shPosition[threadIdx.x] = globalX[index];
    __syncthreads();
    //calculate the accelerations on a tile
    acc = tile_calc(myPos, acc);
    __syncthreads();
  }
  //once acc is full, split it into a float4
  // for coalescense and then put it in globalA
  float4 acc4 = {acc.x, acc.y, acc.z, 0.0f};
  globalA[idx] = acc4;
}

int main(void){
  //initialize the 3 * 100000 points
  float points [1000*3];
  initialize_points(points);
  void *devX, *devA;
  cudaMallocManaged(&devX, N*sizeof(float));
  cudaMallocManaged(&devA, N/3 *sizeof(float));
  int blocksize = 256;
  int numBlocks = (N + blocksize - 1) / blocksize;
  calculate<<<numBlocks, blocksize>>>(devX, devA);
}
