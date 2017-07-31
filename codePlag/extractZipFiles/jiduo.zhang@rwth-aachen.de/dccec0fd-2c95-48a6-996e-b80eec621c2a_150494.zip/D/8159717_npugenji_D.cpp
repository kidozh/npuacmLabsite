#include <iostream>
#include <cstring>
#include <algorithm>
#include <cstdio>
#include <string>
using namespace std;

int main()
{
    int a,k=1;
    string s="";
    scanf("%d",&a);
    if (a==0) cout<<"0";
    while (a)
    {
        if (a&1)
        {
            if (k<0) a+=1;
            s.insert(0,"1");
        }
        else
            s.insert(0,"0");
        a>>=1;
        k=-k;
    }
    cout<<s;
    return 0;
}
