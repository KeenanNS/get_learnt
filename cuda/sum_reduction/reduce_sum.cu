#include<iostream>
#include<math.h>
#include<cooperative_groups.h>

using namespace cooperative_groups;
int numBlocks = 40;
int blockSize = 256;

__device__ int reduce_sum(thread_group g, int *temp, int val){
  for (int i = g.size()/2; i>0; i /=2){
    // make a val variable for each thread and take the value from the shared array
    temp[g.thread_rank()] = val;
    //sync them to prevent the race condition
    g.sync();
    if(g.thread_rank() < i) {val += temp[g.thread_rank() +i];}
    g.sync();
  }
  return val;
}
__device__ int block_sum(float *input, int n){
  int sum = 0;
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  for(int i = index; i < n/4; i += stride){
    int4 in = ((int4*) input)[i];
    sum += in.x + in.y + in.z + in.w;
  }
  return sum;
}

__global__ void sum_kernel(float *sum, float *input, int n){
  int my_sum = block_sum(input, n);
  //shared memory, need to synchronize threads before reading or writing
  //
  extern __shared__ int temp[];
  auto g = this_thread_block();
  int block_sum = reduce_sum(g, temp, my_sum);
  if (g.thread_rank() ==0){ atomicAdd(sum, block_sum);}
}

int main(void){

  int n = 1 << 10;
  int blockSize = 256;
  int numBlocks = (n + blockSize - 1) / blockSize;
  float *input, *sum;
  cudaMallocManaged(&input, n * sizeof(float));
  cudaMallocManaged(&sum, sizeof(float));

  for (int i = 0; i < n; i ++){
    input[i] = (rand() %100) / 100.0;
  }

  sum_kernel <<<numBlocks, blockSize>>>(sum, input, n);
  printf("the final sum: %f", *sum);
}
