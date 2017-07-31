#include<cstdio>   
#include<algorithm>  
#include<cmath>
#include<iostream>
using namespace std;  
int ans[1000];  
int main()  
{  
    int a;  
    cin>>a;
    if(a==0)  
    {  
        printf("0\n");  
        return 0;
    }  
    int cont=0;  
    while(a)  
    {  
        ans[cont++]=abs(a%(-2));  
        a-=abs(a%(-2));  
        a/=(-2);  
    }  
    for(int i=cont-1;i>=0;i--) printf("%d",ans[i]);  
    cout<<endl;
      
}  