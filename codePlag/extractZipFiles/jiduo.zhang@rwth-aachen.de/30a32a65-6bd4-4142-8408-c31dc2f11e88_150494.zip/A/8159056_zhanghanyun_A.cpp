#include<stdio.h>
int main()
{
    int a,b;
    int a1[20],b1[20];
    while(scanf("%d%d",&a,&b)!=EOF){
        int k,l;
        k=l=0;
        while(a){
          a1[k++]=a%10;
            a/=10;
        }
        while(b){
            b1[l++]=b%10;
            b/=10;
        }
        int i,j;
        int sum=0;
        for(i=0;i<k;i++){
            for(j=0;j<l;j++){
                sum+=(a1[i]*b1[j]);
            }
        }
        printf("%d\n",sum);
    }
    return 0;
}
