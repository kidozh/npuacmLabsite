#include <iostream>

using namespace std;
int a[15],b[15];
int main()
{
    int A,B;
    int lena=0,lenb=0;
    cin>>A>>B;
    while (A){
        a[lena++]=A%10;
        A/=10;
    }
    while (B){
        b[lenb++]=B%10;
        B/=10;
    }
    int sum=0;
    for (int i=0;i<lena;i++){
        for (int j=0;j<lenb;j++){
            sum+=(a[i]*b[j]);
        }
    }
    cout<<sum<<endl;
    return 0;
}
