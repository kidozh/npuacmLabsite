#include<iostream>
#include<string>
#include<vector>
#include<utility>
#include<algorithm>
#include<cstdio>
#include<cstdlib>
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
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<pii> vii;
typedef double DB;
template <class T> T abs(T a){return a>=0?a:-a;}
template <class T> T gcd(T a,T b){return b?gcd(b,a%b):a;}
template <class T> T mod(T a,T b){T ret=a%b;if(ret<0)ret+=b;return ret;}
ll mulmod(ll a,ll b,ll c){if(b==0LL)return 0LL;ll ret=mulmod(a,b>>1,c);ret=(ret+ret)%c;if(b&1LL)ret=(ret+a)%c;return ret;}
ll powmod(ll a,ll b,ll c){if(b==0LL)return 1LL;ll ret=powmod(a,b>>1,c);ret=ret*ret%c;if(b&1LL)ret=ret*a%c;return ret;}
/* .................................................................................................................................. */
const int N=100005;
int tt;
ll u,v,w,n,m;
/* .................................................................................................................................. */
vi a;
int main(){
	cin>>u;
	if(u==0)return puts("0"),0;
	while(u){
		a.pb(abs(u%2));
		u-=a.back();
		u/=-2;
	
	}
	reverse(all(a));
	RR(i,a)cout<<a[i];



	return 0;
}