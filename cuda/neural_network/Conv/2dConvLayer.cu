#include<iostream>
#include<cooperative_groups.h>
#define KERNEL_DIM = 5;
using namespace cooperative_groups;

__global__
void convolve(int *img, int *out, int N){
  int col = threadIdx.x + blockIdx.x * blockDim.x;
  int row = threadIdx.y + blockIdx.y * blockDim.y;
  int kernel_size = (sizeof(kernel)/sizeof(int))^(1/2);
  int frame = KERNEL_DIM /2
  int temp;
    for (int m = -frame; m < frame; m++){
      for (int n = -frame; n < frame; n++){
        if ((row+m > 0) && (col+n > 0))
        temp += kernel[m + frame][n + frame] * img[row+m][col+n];
      }
    }
  }

int main(void){
  // import image. for now random matri


  int *img;
  int *out;
  int N = 1080 * 1080;
  cudaMallocManaged(&img, N * sizeof(int));
  cudaMallocManaged(&out, N * sizeof(int));

  extern __constant__ int kernel[5 * 5];

  for (int i = 0; i< 5*5; i++){
    *kernel++ = rand()%100;
  }

  for (int i = 0; i< 1080*1080; i++){
    *img++ = rand()%100;
  }

  int blockSize = 256;
  int numBlocks = (blockSize - 1 + n) / blockSize;
  convolve<<<blockSize, numBlocks>>>(img, out);
  return 0;
}
