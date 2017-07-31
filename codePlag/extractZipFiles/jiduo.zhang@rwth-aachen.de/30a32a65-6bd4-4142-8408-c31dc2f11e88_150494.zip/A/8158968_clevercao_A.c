#include <stdio.h>
#include <string.h>
#include <math.h>
int main ()
{
	int a,b,i,j,c[12],d[12],e[102],sum;
	for (i=1;i<=9;i++)
		for (j=1;j<=9;j++)
			e[i*10+j]=i*j;
	while(scanf("%d%d",&a,&b)!=EOF){
		sum=0;
		for (i=1,j=1;i<=10;j*=10,i++) c[i]=a/j%10;
		for (i=1,j=1;i<=10;j*=10,i++) d[i]=b/j%10;
		for (i=1;i<=10;i++)
			for (j=1;j<=10;j++){
			if(c[i]!=0&&d[j]!=0) sum+=e[c[i]*10+d[j]];
		}
		printf("%d\n",sum);
	}



	return 0;
}
