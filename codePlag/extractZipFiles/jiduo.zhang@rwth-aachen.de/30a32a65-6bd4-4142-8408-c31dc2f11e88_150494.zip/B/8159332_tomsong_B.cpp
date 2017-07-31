#include <iostream>

using namespace std;
int maxm(int a,int b)
{
    if(a>b) return a;
    return b;
}
int main()
{
    int n,i,j,v[2000],l,r,sum,k[2000];
    cin>>n;
    for(i=0;i<n;i++) cin>>v[i];
    l=0,r=n,sum=0;
    k[0]=0;
    for(i=1;i<n;i++)
    {
        k[i]=k[i-1]+v[i-1]*i;
        for(j=i-1;j>0;j--)
        {
            k[j]=maxm(k[j]+v[j+n-i]*i,k[j-1]+v[j-1]*i);
        }
        k[0]=k[0]+v[n-i]*i;
    }
    sum=k[0]+v[0]*n;
    for(i=1;i<n;i++)
    {
        if(sum<(k[i]+v[i]*n))
            sum=k[i]+v[i]*n;
    }
    cout<<sum;
    return 0;
}
