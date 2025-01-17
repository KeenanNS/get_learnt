#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

pthread_t tid[2];
int counter;
pthread_mutex_t lock;

void* trythis(void *arg){

  pthread_mutex_lock(&lock);
  unsigned long i = 0;
  counter++;
  printf("job %d starter\n", counter);
  for(i = 0; i < (0xffffffff); i++);
  printf("job %d finished\n", counter);
  pthread_mutex_unlock(&lock);
  return NULL;
}

int main(void){
  int i = 0;
  int error;

  pthread_mutex_init(&lock, NULL);
  while(i < 2){
    error = pthread_create(&(tid[i]), NULL, &trythis, NULL);
    if(error != 0){
      printf("thread cant be created : [%s]", strerror(error));
    }
      i++;
  }
  pthread_join(tid[0], NULL);
  pthread_join(tid[1], NULL);
  pthread_mutex_destroy(&lock);

  return 0;
}
