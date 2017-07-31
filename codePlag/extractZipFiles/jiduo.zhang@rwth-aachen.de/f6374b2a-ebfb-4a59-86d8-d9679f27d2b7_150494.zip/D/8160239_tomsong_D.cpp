#include <iostream>
#include<algorithm>
using namespace std;
int main()
{
    int num,i;
    bool pt[100];
    cin>>num;
    if(num==0) {cout<<0;return 0;}
    for(i=0;num;i++)
    {
        pt[i]=abs(num%(-2));
        num-=abs(num%(-2));
        num/=(-2);
    }
    for(i--;i>=0;i--) cout<<pt[i];
    return 0;
}
