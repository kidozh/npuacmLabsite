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
int f[2100][2100];
int n;
int v[2100];
int sum[2100];
int main()
{
	scanf("%d",&n);
	for (int i=1;i<=n;i++)
		scanf("%d",&v[i]),sum[i]=sum[i-1]+v[i];
	for (int i=1;i<=n;i++)
		f[i][i]=v[i];
	for (int i=2;i<=n;i++)
		for (int j=1;j<=n-i+1;j++)
			f[j][j+i-1]=max(f[j+1][j+i-1]+sum[j+i-1]-sum[j]+v[j],f[j][j+i-2]+sum[j+i-2]-sum[j-1]+v[j+i-1]);
	printf("%d\n",f[1][n]);
	return 0;
}