#include<math.h>
#include<iostream>
#include<cstdlib>

#define BLOCKSIZE 256


// __global__
// void dot(float* X, float* Y, float* c){
//   // int index = blockIdx.x * blockDim.x + threadIdx.x;
//   // __shared__ float cache[BLOCKSIZE];
//   //
//   // cache[threadIdx.x] = X[index] * Y[index];
//   //
//   // __syncthreads();
//   //
//   // if(threadIdx.x == 0){
//   //   int sum = 0;
//   //   for(int i = 0; i < BLOCKSIZE; i++){
//   //     sum += cache[i];
//   //   }
//   //   atomicAdd(c, sum);
//   // }
// }
//
__global__
void dot(float* X, float* Y, float* c, int n){
  __shared__ float cache[BLOCKSIZE];
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  while(i < n){
    cache[threadIdx.x] = X[i] * Y[i];
    i+= gridDim.x * blockDim.x;
  }
  __syncthreads();

  i = BLOCKSIZE / 2;

  while(i > 2){
    if(threadIdx.x < i)
    cache[threadIdx.x] += cache[threadIdx.x +i];
    __syncthreads();
    i /= 2;
  }
  if (threadIdx.x ==0) atomicAdd(c, cache[0]);

}
__device__
float sigmoid(float x){
  return 1.0f / (1 + exp(-x));
}
__global__
void sigPass(int n, float *X, float *S){
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;

  for(int i = idx; i<n; i += stride){
    S[i] = sigmoid(X[i]);
  }
}
__global sigBackProp(int n, float *X, float *errors, float *out_slopes){
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;

  for(int i = index; i < n; i+= stride){
    out_slopes[i] = errors[i] * sigmoid(X[i]) * (1 - sigmoid(X[i]));
  }
}

int main(void){
  int xdim = 1<<16;
  int ydim = 1;
  int n = xdim * ydim;
  float *X, *Y, *S, *c;

  cudaMallocManaged(&X, n*sizeof(float));
  cudaMallocManaged(&S, sizeof(float));
  cudaMallocManaged(&Y, n*sizeof(float));
  cudaMallocManaged(&c, sizeof(float));

  for (int i = 0; i < n; i++){
    X[i] = (rand() %100)/10000.f;
    Y[i] = (rand() %100)/10000.f;
  }



  int numBlocks = (n + BLOCKSIZE - 1) / BLOCKSIZE;
  dot<<<numBlocks, BLOCKSIZE>>>(X,Y,c,n);
  cudaDeviceSynchronize();
  printf(" dot output: %f", *c);
  cudaFree(X);
  cudaFree(Y);
  sigPass<<<numBlocks, BLOCKSIZE>>>(1,c,S);
  cudaDeviceSynchronize();


  printf("final output: %f\n", *S);
  cudaFree(c);
  cudaFree(S);



}
