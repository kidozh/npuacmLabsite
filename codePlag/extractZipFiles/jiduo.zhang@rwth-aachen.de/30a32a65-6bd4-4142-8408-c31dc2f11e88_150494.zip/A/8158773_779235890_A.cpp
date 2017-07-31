#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cmath>
#include<algorithm>
using namespace std; 
int main()
{
	int a,b;
	scanf("%d%d",&a,&b);
	int ans=0;
	while(a!=0)
	{
		int aa=a%10;
		a=a/10;
		int bb=b;
		while(bb!=0)
		{
			int k=bb%10;
			ans+=aa*k;
			bb=bb/10;
		}
	}
	printf("%d",ans);
}
