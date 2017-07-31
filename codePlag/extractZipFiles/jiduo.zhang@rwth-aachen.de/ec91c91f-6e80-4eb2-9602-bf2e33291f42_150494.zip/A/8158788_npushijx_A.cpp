#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

int main()
{
    char a[20],b[20];
    int x[20],y[20];
    int sum=0;
    cin>>a>>b;
    int la=strlen(a);
    int lb=strlen(b);
    for(int i=0;i<la;i++)
    {
        x[i]=a[i]-'0';
    }
    for(int i=0;i<lb;i++)
    {
        y[i]=b[i]-'0';
    }
    for(int i=0;i<la;i++)
    {
        for(int j=0;j<lb;j++)
        {
            sum+=x[i]*y[j];
        }
    }
    cout<<sum<<endl;
}
