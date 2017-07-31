#include<cstdio>
#include<algorithm>

using namespace std;

const int MAXN = 2005;

int n;
int var[MAXN];
int dp[MAXN][MAXN];

int getDp(int l, int r){
    if(dp[l][r]){
        return dp[l][r];
    }
    if(l == r){
        return dp[l][r] = (n - r + l) * var[l];
    }
    int gain = n - r + l;
    return dp[l][r] = max(getDp(l + 1, r) + gain * var[l], getDp(l, r - 1) + gain * var[r]);
}

int main(){
    scanf("%d", &n);
    for(int i = 1; i <= n; ++i){
        scanf("%d", &var[i]);
    }
    printf("%d", getDp(1, n));
    return 0;
}