#include<math.h>
#include<iostream>

__global__
void dot(float* X, float* Y, float* c){
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x;
  __shared__ float cache[blockDim.x];

  cache[threadIdx.x] = X[index] * Y[index];

  __syncthreads();

  if(threadIdx.x == 0){
    int sum = 0;
    for(int i = 0; i < blockDim.x; i++){
      sum += temp[i];
    }
    atomicAdd(c, sum);
  }
}
