#include<iostream>
#include<algorithm>
#include<cstring>
#include<string>
#include<cstdio>
#define N 3020
#define ll long long
using namespace std;
int n,x,y;
int v[N],ans;
int f[N][N];bool vis[N][N];
int dp(int l,int r,int now)
{
	if(l==r)return v[l]*now;
	if(vis[l][r])return f[l][r];
	vis[l][r]=1;int tmp=0;
	tmp=max(dp(l+1,r,now+1)+now*v[l],dp(l,r-1,now+1)+now*v[r]);
	return f[l][r]=tmp;
}
int main()
{
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
		scanf("%d",&v[i]);
	printf("%d\n",dp(1,n,1));
}