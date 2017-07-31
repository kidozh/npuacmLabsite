#include<stdio.h>
int main(){
	int a,b,c[10],d,i=0,j=0,sum=0;
	scanf("%d%d",&a,&b);
	while(a>0){
		c[i++] = a % 10;
		a /= 10;
	}
	while(b>0){
		d = b % 10;
		b /= 10;
		for(j=0;j<i;j++)sum += c[j]*d;
	}
	printf("%d\n",sum);
	return 0;
}