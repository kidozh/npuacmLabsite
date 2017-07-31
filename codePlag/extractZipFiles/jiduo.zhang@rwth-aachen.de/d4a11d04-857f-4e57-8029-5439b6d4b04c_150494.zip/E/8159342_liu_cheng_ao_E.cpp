#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<algorithm>
#include<vector>

using namespace std;
int n,m,k;
struct Edge{
	int f,t;
}e[200100];
vector<int>s[401000];
long long ans;
int fa[200100],sz[201000],rk[201000];
inline int ffa(int no)
{
	return (fa[no]==no)?no:ffa(fa[no]);
}
inline void add(int no,int l,int r,int ll,int rr,int x)
{
	if(ll<=l&&rr>=r)s[no].push_back(x);
	else{
		int mid=(l+r)>>1;
		if(ll<=mid)add(no<<1,l,mid,ll,rr,x);
		if(rr>mid)add(no<<1|1,mid+1,r,ll,rr,x);
	}
}
inline void clr(int no,int l,int r)
{
	if(!s[no].empty())s[no].clear();
	if(l<r){
		int mid=(l+r)>>1;
		clr(no<<1,l,mid);
		clr(no<<1|1,mid+1,r);
	}
}
struct Modify{
	int f,t,szo,rko;
}stk[401000];
int stc;
inline void wk(int no,int l,int r){
	int t1=stc;
	for(int i=0;i<s[no].size();i++){
		int it=s[no][i];
		int ff=ffa(e[it].f),ft=ffa(e[it].t);
		if(ff==ft)continue;
		if(rk[ff]<rk[ft]){
			stk[++stc]=(Modify){ff,ft,sz[ft],rk[ft]};
			fa[ff]=ft;ans+=(long long)sz[ff]*sz[ft];
			sz[ft]+=sz[ff];
		}else if(rk[ff]==rk[ft]){
			stk[++stc]=(Modify){ff,ft,sz[ft],rk[ft]};
			fa[ff]=ft;ans+=(long long)sz[ff]*sz[ft];
			sz[ft]+=sz[ff];rk[ft]++;
		}else{
			stk[++stc]=(Modify){ft,ff,sz[ff],rk[ff]};
			fa[ft]=ff;ans+=(long long)sz[ff]*sz[ft];
			sz[ff]+=sz[ft];
		}
	}
	if(l==r)printf("%lld\n",ans);
	else{
		int mid=(l+r)>>1;
		wk(no<<1,l,mid);
		wk(no<<1|1,mid+1,r);
	}
	for(;stc>t1;stc--){
		sz[stk[stc].t]=stk[stc].szo;
		rk[stk[stc].t]=stk[stc].rko;
		ans-=(long long)sz[stk[stc].f]*sz[stk[stc].t];
		fa[stk[stc].f]=stk[stc].f;
	}
}
int main()
{
	while(scanf("%d%d%d",&n,&m,&k)!=EOF)
	{
		clr(1,1,k);
		ans=0;
		for(int i=1;i<=n;i++)sz[i]=1;
		memset(rk,0,sizeof(rk));
		for(int i=1;i<=n;i++)fa[i]=i;
		for(int i=1;i<=m;i++){
			int a,b,c;
			scanf("%d%d%d",&a,&b,&c);
			e[i].f=a,e[i].t=b;
			if(c>1)add(1,1,k,1,min(c-1,k),i);
			if(c<k)add(1,1,k,c+1,k,i);
		}
		wk(1,1,k);
	}
	return 0;
}
