#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<algorithm>

using namespace std;
int x[10],y[10],ans;
int main()
{
	int a,b;
	scanf("%d%d",&a,&b);
	for(int i=0;i<=9;i++)
	x[i]=a%10,a/=10,y[i]=b%10,b/=10;
	for(int i=0;i<=9;i++)
	for(int j=0;j<=9;j++)
	ans+=x[i]*y[j];
	printf("%d",ans);
	return 0;
}
