#include<bits/stdc++.h>
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
template <class T> inline void wt(T x){if (x<0)putchar('-'),x=-x;if (x<10)putchar(x + '0');else wt(x / 10), putchar(x % 10 + '0');}
template <class T> inline void rd(T&x){bool f=0; char ch;for(ch=getchar();ch<=32;ch=getchar());if (ch=='-')f=1,ch=getchar();for(x=0;ch>32;ch=getchar()) x =(x<<3)+(x<<1)+ch-'0';if(f) x=-x;}
/* .................................................................................................................................. */
const int N=100005;
int tt;
int n,m,k;
/* .................................................................................................................................. */
struct Edge {
    int u,v,n;
    Edge (int u=0,int v=0,int n=0):u(u),v(v),n(n){}
}E[N+N];
int cntE,H[N];
void add (int x,int u,int v){
    E[cntE]=Edge(u,v,H[x]);
    H[x]=cntE++;
}
struct Node {
    int u,v,cntu,cntv,ranku,rankv;
    Node (int u=0,int v=0,int cntu=0,int cntv=0,int ranku=0,int rankv=0):u(u),v(v),cntu(cntu),cntv(cntv),ranku(ranku),rankv(rankv){}
}S[N+N] ;
int top;
ll ans;
namespace ufs{
	int p[N],cnt[N],rk[N];
	void init(){
		R(i,1,n){
			p[i]=i;
			cnt[i]=1;
			rk[i]=0;
		}
	}
	int find(int x){
	    int u=x;
	    while(p[u]!=u)u=p[u];
	    int ans=u;
	    while(p[x]!=x){
	        int tmp=p[x] ;
	        p[x]=tmp ;
	        x=tmp ;
	    }
	    return ans ;
	}
	void Union (int l,int r){
	    R(t,l,r){
	        for(int i=H[t];~i;i=E[i].n){
	            int u=find(E[i].u) ;
	            int v=find(E[i].v) ;
	            if (u==v)continue;
	            S[top++]=Node(u,v,cnt[u],cnt[v],rk[u],rk[v]);
	            ans+=1LL*cnt[u]*cnt[v];
	            if(rk[u]<=rk[v]) {
	                rk[v]=max(rk[v],rk[u]+1);
	                p[u]=v ;
	                cnt[v]+=cnt[u];
	            } else {
	                p[v]=u ;
	                cnt[u]+=cnt[v];
	            }
	        }
	    }
	}
}
using namespace ufs;
void back(int x){
    while (top>x){
        --top;
        int u=S[top].u,v=S[top].v;
        ans-=1LL*S[top].cntu*S[top].cntv;
        p[u]=u;
        p[v]=v;
        cnt[u]=S[top].cntu;
        cnt[v]=S[top].cntv;
        ufs::rk[u]=S[top].ranku;
        ufs::rk[v]=S[top].rankv;
    }
}

void cdq(int l,int r){
    if (l==r) {
        printf("%lld\n",ans) ;
        return ;
    }
    int m=(l+r)>>1;
    int rtop=top ;
    Union(m+1,r) ;
    cdq(l,m);
    back(rtop);
    Union(l,m);
    cdq(m+1,r);
    back(rtop);
}

void solve (){
    int u,v,c;
    init();
    ans=0;top=0;cntE=0;
    mset(H,-1);
    R(i,1,m){
        scanf("%d%d%d",&u,&v,&c);
        if(c>k){
            u=find(u);
            v=find(v);
            if(u==v)continue ;
            if(ufs::rk[u]<=ufs::rk[v]){
                ufs::rk[v]=max(ufs::rk[v],ufs::rk[u]+1);
                p[u]=v;
                cnt[v]+=cnt[u];
            } else {
                p[v]=u ;
                cnt[u]+=cnt[v];
            }
        } else add(c,u,v) ;
    }
    cdq (1,k) ;
}

int main () {
    while (~scanf("%d%d%d",&n,&m,&k)) solve () ;
    return 0 ;
}
/*







*/




