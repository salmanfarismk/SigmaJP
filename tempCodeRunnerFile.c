#include <stdio.h>
struct node{
    int data;
    struct node *next;
};
int main() {
    struct node *first,*second,*third;
    first.data = 10;
    second.data = 20;
    third.data = 30;
    first.next = &second;
    second.next = &third;
    third.next = NULL;
    first.next->data;
    first.next->next->data;
    printf("%d",first.data);

}
