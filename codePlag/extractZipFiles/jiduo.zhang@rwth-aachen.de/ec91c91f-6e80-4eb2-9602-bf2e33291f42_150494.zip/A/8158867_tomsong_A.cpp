#include <cstdio>
#include<cstring>
int main()
{
    int a[10],b[10],i,j,cnt=0;
    char s[10];
    memset(a,0,sizeof(a));
    memset(b,0,sizeof(b));
    scanf("%s",s);
    for(i=0;s[i]!='\0';i++) a[i]=s[i]-'0';
    scanf("%s",s);
    for(i=0;s[i]!='\0';i++) b[i]=s[i]-'0';
    for(i=0;i<10;i++)
    {
        for(j=0;j<10;j++)
            cnt+=a[i]*b[j];
    }
    printf("%d",cnt);
    return 0;
}
