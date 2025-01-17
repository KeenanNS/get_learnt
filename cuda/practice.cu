#include <iostream>
#include <math.h>
// Kernel function to add the elements of two arrays
__global__
void add(int n, float *x, float *y)
{
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  int count = 0;
  for (int i = index; i < n; i += stride){
    printf("count : %d\n",count ++);
    y[i] = x[i] + y[i];
  }

}

int main(void)
{
  int N = 1<<12;
  float *x, *y;

  // Allocate Unified Memory – accessible from CPU or GPU
  cudaMallocManaged(&x, N*sizeof(float));
  cudaMallocManaged(&y, N*sizeof(float));

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the GPU
  int blocksize = 256;
  int numBlocks = (N + blocksize - 1) / blocksize;
  for(int i = 0; i<100; i++)
  add<<<numBlocks, blocksize>>>(N, x, y);

  // Wait for GPU to finish before accessing on host
  cudaDeviceSynchronize();

  // Check for errors (all values should be 3.0f)

  cudaFree(x);
  cudaFree(y);

  return 0;
}
