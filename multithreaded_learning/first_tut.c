#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<unistd.h>

void *mythread(void *vargp){
  sleep(1);
  printf("hello world\n");
  return NULL;
}

int main(void){
  pthread_t thread_id;
  printf("pre-thread\n");
  pthread_create(&thread_id, NULL, mythread, NULL);
  pthread_join(thread_id, NULL);
  printf("past-thread\n");
  return 0;
}
