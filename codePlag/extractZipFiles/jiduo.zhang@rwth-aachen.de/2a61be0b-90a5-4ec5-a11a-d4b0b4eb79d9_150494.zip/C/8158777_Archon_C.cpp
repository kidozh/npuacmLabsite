#include <cctype>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <iomanip>
#include <string>
#include <algorithm>
#include <bitset>
#include <functional>
#include <numeric>
#include <deque>
#include <list>
#include <map>
#include <queue>
#include <vector>
#include <set>
#include <stack>
#include <iterator>
#include <memory>
#include <utility>
#include <string>
#include <cassert>

using namespace std;

#define X first
#define Y second
#define mp make_pair
#define pb push_back
#define mset(a,b) memset(a,b,sizeof a)
#define mcpy(a,b) memcpy(a,b,sizeof a)
#define R(i,s,t) for(register int i=s;i<=t;++i)
#define Rd(i,s,t) for(register int i=s;i>=t;--i)
#define __ puts("")
#define _ putchar(' ')
#define all(T) T.begin(),T.end()

typedef long long ll;
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<pii> vii;
template <class T> T abs(T a){return a>=0?a:-a;}
template <class T> T gcd(T a,T b){return b?gcd(b,a%b):a;}
template <class T> T mod(T a,T b){T ret=a%b;if(ret<0)ret+=b;return ret;}
ll mulmod(ll a,ll b,ll c){if(b==0LL)return 0LL;ll ret=mulmod(a,b>>1,c);ret=(ret+ret)%c;if(b&1LL)ret=(ret+a)%c;return ret;}
ll powmod(ll a,ll b,ll c){if(b==0LL)return 1LL;ll ret=powmod(a,b>>1,c);ret=ret*ret%c;if(b&1LL)ret=ret*a%c;return ret;}
template <class T> inline void write(T x){if (x<0)putchar('-'),x=-x;if (x<10)putchar(x + '0');else write(x / 10), putchar(x % 10 + '0');}
template <class T> inline void read(T&x){bool f=0; char ch;for(ch=getchar();ch<=32;ch=getchar());if (ch=='-')f=1,ch=getchar();for(x=0;ch>32;ch=getchar()) x =(x<<3)+(x<<1)+ch-'0';if(f) x=-x;}
//===========================================================================================
int x;
struct sp{
	vii G[50005];
	int N,M;
	int dis[50005],c[50005];
	bool done[50005];
	inline void add(int a,int b,int c){G[a].pb(mp(b,c));}
	bool spfa(int s) {
		deque<int> Q;
		memset(dis,0x3f,sizeof(dis));
		memset(done,false,sizeof(done));
		Q.push_front(s);
		done[s] = true;
		dis[s] = 0;
		bool isacyclic = true;
		while(! Q.empty()) {
			int u = Q.front();
			Q.pop_front();
			done[u] = false;
			for(int i=0;i<G[u].size();++i) {
				int v = G[u][i].X;
				if(dis[u] + G[u][i].Y < dis[v]) {
					dis[v] = dis[u] + G[u][i].Y;
					if(! done[v]) {
						done[v] = true;
						c[v] ++;
						if(Q.empty()) {
							Q.push_front(v);
						} else {
							int asd = Q.front();
							if(dis[v] < dis[asd]) {
								Q.push_front(v);
							} else {
								Q.push_back(v);
							}
						}
						if(c[v] > N) {
							return ~isacyclic;
						}
					}
				}
			}
		}
		return isacyclic;
	}
	void init(){
			cin>>N>>M;
	}
}G1,G2;
int main(){
	G1.init();
	G2.N=G1.N;
	G2.M=G1.M;
	cin>>x;
	R(i,1,G1.M){
		int u,v,w;
		cin>>u>>v>>w;
		G1.add(u,v,w);
		G2.add(v,u,w);
	}
	G1.spfa(x);
	G2.spfa(x);
	int ans=-1;
	R(i,1,G1.N){
                if(G1.dis[i]!=0x3f3f3f3f&&G2.dis[i]!=0x3f3f3f3f)
                    ans=max(ans,G1.dis[i]+G2.dis[i]);
            }
    cout<< ans;
	
	
	return 0;
} 