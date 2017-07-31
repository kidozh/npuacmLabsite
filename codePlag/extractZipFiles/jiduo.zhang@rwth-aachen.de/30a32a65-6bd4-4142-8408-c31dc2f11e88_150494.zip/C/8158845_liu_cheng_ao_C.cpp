#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<vector>
#include<algorithm>

using namespace std;

int n,m,x;
struct EE{int t,w;};vector<EE>E[1100],EN[1100];
int f[1100],fn[1100],e[1100];

int main()
{
    scanf("%d%d%d",&n,&m,&x);
    for(int i=1;i<=m;i++)
    {
            int a,b,c;
            scanf("%d%d%d",&a,&b,&c);
            struct EE et;
            et.w=c;
            et.t=a;
            EN[b].push_back(et);
            et.t=b;
            E[a].push_back(et);
    }
    memset(f,0x3f3f3f3f,sizeof(f));
    memset(e,0,sizeof(e));
    f[x]=0;
    for(int k=1;k<n;k++)
    {
            int mni,mnf=0x3f3f3f3f;
            for(int i=1;i<=n;i++)
            if(mnf>f[i]&&!e[i])
            {
                        mni=i;
                        mnf=f[i];
            }
            e[mni]=1;
            for(int i=0;i<E[mni].size();i++)
            {
                    f[E[mni][i].t]=f[E[mni][i].t]<f[mni]+E[mni][i].w?f[E[mni][i].t]:f[mni]+E[mni][i].w;
            }
    }
    memset(fn,0x3f3f3f3f,sizeof(fn));
    memset(e,0,sizeof(e));
    fn[x]=0;
    for(int k=1;k<n;k++)
    {
            int mni,mnf=0x3f3f3f3f;
            for(int i=1;i<=n;i++)
            if(mnf>fn[i]&&!e[i])
            {
                        mni=i;
                        mnf=fn[i];
            }
            e[mni]=1;
            for(int i=0;i<EN[mni].size();i++)
            {
                    fn[EN[mni][i].t]=fn[EN[mni][i].t]<fn[mni]+EN[mni][i].w?fn[EN[mni][i].t]:fn[mni]+EN[mni][i].w;
            }
    }    
    int mx=0;
    for(int i=1;i<=n;i++)
    mx=mx>f[i]+fn[i]?mx:f[i]+fn[i];
    printf("%d",mx);
    return 0;
}

