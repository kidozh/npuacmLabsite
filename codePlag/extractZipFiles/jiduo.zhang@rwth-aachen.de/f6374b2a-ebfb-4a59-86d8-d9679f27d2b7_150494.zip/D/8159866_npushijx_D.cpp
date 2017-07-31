#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<string>
using namespace std;

int main()
{
    long long x;
    cin>>x;
    if(x==0)cout<<0<<endl;
    if(x>0)
    {
        string s;
        int t=1;
        x--;
        while(x)
        {
            if(x%4==1)s="10"+s;
            if(x%4==2)s="11"+s;
            if(x%4==3)s="00"+s;
            if(x%4==0)s="01"+s;
            x-=1;
            t*=4;
            x/=4;
        }
        cout<<"1"+s<<endl;
    }

    if(x<0)
    {
        x*=-1;
        string s;
        int t=2;
        x--;
        while(x>1)
        {
            x-=2;
            if(x%4==0)s="01"+s;
            if(x%4==1)s="00"+s;
            if(x%4==2)s="11"+s;
            if(x%4==3)s="10"+s;
            t*=4;
            x/=4;
        }
        if(x==0)s="11"+s;
        if(x==1)s="10"+s;
        cout<<s<<endl;
    }
}
