#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<algorithm>
#define MX 2010
using namespace std;
int n,v[MX];
int dp[MX][MX];
int F(int l,int r){
	if(dp[l][r])return dp[l][r];
	if(l==r)return dp[l][r]=v[l]*n;
	return dp[l][r]=max(v[l]*(n-(r-l))+F(l+1,r),v[r]*(n-(r-l))+F(l,r-1));
}
int main()
{
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%d",&v[i]);
	printf("%d",F(1,n));
	return 0;
}
