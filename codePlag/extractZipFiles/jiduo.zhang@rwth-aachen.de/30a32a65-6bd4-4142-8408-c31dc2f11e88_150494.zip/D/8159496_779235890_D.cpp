#include<cstdio>
#include<cmath>
int  ans[10000];
int main()
{
	int n,t;
	t=0;
	scanf("%d",&n);
	if(n==0)
	{
		printf("0");
		return 0;
	}
	while(n!=1)
	{
	//	printf("::%d\n",n);
		int nn=n;
		if(nn<0)
		nn=-nn;
		if(nn%2!=0)
		{
			t++;
			ans[t]=1;
			n=(n-1)/(-2);
		}
		else
		{
			t++;
			ans[t]=0;
			n=n/-2;
		}
	}
	printf("1");
	for(int i=t;i>=1;i--)
	{
		printf("%d",ans[i]);
	}
}