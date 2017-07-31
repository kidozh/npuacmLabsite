#include<stdio.h>
#define MAX 11
char a[MAX],b[MAX];
int main(){
	int m,n,i,j,l;
	scanf("%s%s",a,b);
	long long k;
//	getchar();
	i=0;
	j=0;
	k=0;
	while(a[i]!='\0'){
		m=a[i]-'0';
		//printf("%d\n",m);
		while(b[j]!='\0'){
            n=b[j]-'0';
          //  printf("%d\n",n);
			k+=m*n;
			j++;
		}
		i++;
		j=0;
	}
	printf("%I64d\n",k);
	return 0;
} 