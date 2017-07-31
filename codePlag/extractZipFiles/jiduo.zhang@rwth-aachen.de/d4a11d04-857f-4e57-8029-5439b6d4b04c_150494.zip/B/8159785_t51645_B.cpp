#include<iostream>
#include <stdio.h>
#include <algorithm>
#include <math.h>
#include<stdlib.h>
#include <string.h>
#include<queue>
#include<set>
#include<map>
#include<stack>
#include<time.h>
using namespace std;
#define MAX_N 2005
#define inf 0x7fffffff
#define LL long long
#define ull unsigned long long
#define mod 10007
LL INF=9e18;

int v[MAX_N];
int dp[MAX_N][MAX_N];
int cal(int l, int r, int k)
{
    if(dp[l][r])
        return dp[l][r];
    if(l == r) {
        dp[l][r] = v[l]*k;
        return v[l]*k;
    }
    int lv,rv;
    lv = cal(l+1, r, k+1) + v[l]*k;
    rv = cal(l, r-1, k+1) + v[r]*k;
    dp[l][r] = max(lv, rv);
    return dp[l][r];
}
int main()
{
    int N;
    cin >> N;
    for(int i=1;i<=N;i++)
        scanf("%d",&v[i]);
    memset(dp, 0, sizeof(dp));
    printf("%d\n",cal(1, N, 1));
}
