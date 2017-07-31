#include<iostream>
#include<cmath>
#include<cstdio>
#include<iomanip>
#include<cstring>
#include<stdlib.h>
#include<string>
#include<algorithm>
#include<queue>
using namespace std;
int ans[100005];
int main()
{
	int a,b,n;
	while(~scanf("%d",&n))
	{
		if(n==0)printf("0\n");
		else
		{
			int i=0;
			while(n!=0)
			{
				if((-n)%2==0)
				{
					ans[i++]=0;
					n/=-2;
				}
				else
				{
					ans[i++]=1;
					if(n<0)n=(-n)/2+1;
					else n=-(n/2);
				}
			}
			for (i--;i>=0;i--)
			printf("%d",ans[i]);
			printf("\n");
		}
	}

	return 0;
}
