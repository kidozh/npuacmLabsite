#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<string>
using namespace std;
int d[2001][2001];
int main()
{
    int a[2222];
    int N;
    cin>>N;
    for(int i=1;i<=N;i++)
    {
        scanf("%d",&a[i]);
    }
    for(int i=0;i<=N;i++)
    {
        for(int j=0;i+j<=N;j++)
        {
            if(i==0&&j!=0)d[i][j]=d[i][j-1]+a[N-j+1]*j;
            if(i!=0&&j==0)d[i][j]=d[i-1][j]+a[i]*i;
            if(i!=0&&j!=0)d[i][j]=max(d[i][j-1]+a[N-j+1]*(i+j),d[i-1][j]+a[i]*(i+j));
            //printf("d[%d][%d]=%d\n",i,j,d[i][j]);
        }
    }
    int maxn=0;
    for(int i=0;i<=N;i++)
    {
        if(d[i][N-i]>maxn)maxn=d[i][N-i];
    }
    cout<<maxn<<endl;
}
