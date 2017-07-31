#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cmath>
#include<iostream>
#include<algorithm>
#include<set>
#include<map>
#include<queue>
#include<stack>
#include<vector>
#include<bitset>

using namespace std;
int a,b;
int x[110],y[110],na,nb;
int ans;
int main()
{
	scanf("%d %d",&a,&b);
	while (a) x[na++]=a%10,a/=10;
	while (b) y[nb++]=b%10,b/=10;
	for (int i=0;i<na;i++)
		for (int j=0;j<nb;j++)
			ans+=x[i]*y[j];
	printf("%d\n",ans);
	return 0;
}