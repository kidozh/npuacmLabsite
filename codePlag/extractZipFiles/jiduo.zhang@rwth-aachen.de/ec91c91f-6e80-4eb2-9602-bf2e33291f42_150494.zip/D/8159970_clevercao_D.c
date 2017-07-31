#include <stdio.h>
int main(){
	long long n;
	int a[102],i;
	while(scanf("%lld",&n)!=EOF){
		i=0;
		while(n){
			a[i]=n%-2;
			if(a[i]<0) a[i]*=-1,n=n/-2+1;
			else n/=-2;
			i++;
		}
		if(i==0) printf("0");
		else for (i--;i>=0;i--) printf("%d",a[i]);
		printf("\n");
	}



	return 0;
	}
