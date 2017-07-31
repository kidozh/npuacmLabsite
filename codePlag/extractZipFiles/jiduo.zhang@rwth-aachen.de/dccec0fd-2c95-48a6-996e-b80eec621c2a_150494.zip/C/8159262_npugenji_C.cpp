#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>

using namespace std;
int map[1010][1010],map2[1010][1010];
int vis[1010];
int main()
{
    int n,m,x,i,j,k,a,b,t,ans=0,pos,minlen;
    scanf("%d%d%d",&n,&m,&x);
    for (i=1;i<=n;i++)
    {
        for (j=1;j<=n;j++)
            map2[i][j]=map[i][j]=999999999;
        map[i][i]=map2[i][i]=0;
    }

    for (i=0;i<m;i++)
    {
        scanf("%d%d%d",&a,&b,&t);
        map[a][b]=t;
        map2[b][a]=t;
    }
    vis[x]=1;
    for (i=1;i<n;i++)
    {
        minlen=99999999;
        for (j=1;j<=n;j++)
            if (!vis[j] &&map[x][j]<minlen)
            {
                minlen=map[x][j];
                pos=j;
            }
        vis[pos]=1;
        for (j=1;j<=n;j++)
            if (!vis[j] && map[x][j]>map[x][pos]+map[pos][j])
                map[x][j]=map[x][pos]+map[pos][j];
    }
    memset(vis,0,sizeof vis);
    vis[x]=1;
    for (i=1;i<n;i++)
    {
        minlen=99999999;
        for (j=1;j<=n;j++)
            if (!vis[j] &&map2[x][j]<minlen)
            {
                minlen=map2[x][j];
                pos=j;
            }
        vis[pos]=1;
        for (j=1;j<=n;j++)
            if (!vis[j] && map2[x][j]>map2[x][pos]+map2[pos][j])
                map2[x][j]=map2[x][pos]+map2[pos][j];
    }


    for (i=1;i<=n;i++)
        ans=max(ans,map[x][i]+map2[x][i]);
    cout<<ans;
    return 0;
}
