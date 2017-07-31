#include <iostream>
#include <string>
#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;

int main()
{
    int i,j,ans=0;
    string a,b;
    cin>>a>>b;
    for (i=0;i<a.length();i++)
        for (j=0;j<b.length();j++)
            ans+=(a[i]-'0')*(b[j]-'0');
    cout<<ans;
    return 0;
}
