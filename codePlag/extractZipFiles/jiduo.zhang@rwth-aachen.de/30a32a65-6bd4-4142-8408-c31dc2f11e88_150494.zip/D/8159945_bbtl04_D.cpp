#include <iostream>
using namespace std;

int main()
{
    int n;
    int num[30];
    int cnt=0;
    cin>>n;
    if (n==0) cout<<"0";
    while (n){
        if (n>0&&n%2==1)
        {
            num[cnt++]=1;
            n=(n-1)/(-2);
        }
        else if(n<0&&(-n)%2==1){
            num[cnt++]=1;
            n=(n-1)/(-2);
        }
        else {
            num[cnt++]=0;
            n=n/(-2);
        }

    }
    if (cnt){
        for (int j=cnt-1;j>=0;j--)
            cout<<num[j];
    }
    cout<<endl;
    return 0;
}
