#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<unistd.h>

int g = 0;

void *mythread(void *vargp){
  int *myid = (int*) vargp;
  static int s = 0;
  ++s; ++g;
  printf("Thread ID: %d, Static: %d, Global: %d\n", *myid, s, g);
  return NULL;
}

int main(void){
  pthread_t thread_id;
  for(int i = 0; i < 3; i++){
    pthread_create(&thread_id, NULL, mythread, (void*)&thread_id);
  }
  pthread_exit(NULL);
  return 0;
}
