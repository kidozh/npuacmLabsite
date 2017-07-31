#include<cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
#define X first
#define Y second
#define mp make_pair
#define pb push_back
#define mset(a,b) memset(a,b,sizeof a)
#define R(i,s,t) for(register int i=s;i<=t;++i)
#define Rd(i,s,t) for(register int i=s;i>=t;--i)
#define RR(i,a) for(register int i=0;i<int(a.size());++i)
#define __ puts("")
#define _ putchar(' ')
#define all(T) T.begin(),T.end()
#define rall(T) T.rbegin(),T.rend()
#define sz(a) int(a.size())
#define mma max_element
#define mmi min_element
#define acu accumulate
typedef long long ll;
template <class T> inline void wt(T x){if (x<0)putchar('-'),x=-x;if (x<10)putchar(x + '0');else wt(x / 10), putchar(x % 10 + '0');}
template <class T> inline void rd(T&x){bool f=0; char ch;for(ch=getchar();ch<=32;ch=getchar());if (ch=='-')f=1,ch=getchar();for(x=0;ch>32;ch=getchar()) x =(x<<3)+(x<<1)+ch-'0';if(f) x=-x;}
/* .................................................................................................................................. */
const int N=2005;
int tt;
int n,m,k;
/* .................................................................................................................................. */
ll dp[N][N];
ll a[N];
int main(){
    int n;
    while(~scanf("%d",&n)){
        R(i,1,n)rd(a[i]);
        mset(dp,0);
        R(len,0,n){
            for(int i=1;i+len<=n;i++){                
                int j=i+len;
                if(len==0)dp[i][j]=a[i]*n;
                else{
                    dp[i][j]=max(dp[i][j],dp[i][j-1]+(i+n-j)*a[j]);
                    dp[i][j]=max(dp[i][j],dp[i+1][j]+(i+n-j)*a[i]);
                }
            }
        }
        wt(dp[1][n]);__;
    }
}
