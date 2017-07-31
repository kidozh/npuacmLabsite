#include<vector>
#include<cstdio>

using namespace std;

void getVar(vector<int> &var, int a){
    while(a){
        var.push_back(a % 10);
        a /= 10;
    }
}

int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    vector<int>var1;
    vector<int>var2;
    getVar(var1, a);
    getVar(var2, b);
    int tempAns = 0;
    for(int i = 0; i < (int)var1.size(); ++i){
        for(int j = 0; j < (int) var2.size(); ++j){
            tempAns += var1[i] * var2[j];
        }
    }
    printf("%d\n", tempAns);
    return 0;
}