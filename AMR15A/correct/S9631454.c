
    #include<stdio.h>
    int main()
    {
    int odd=0,even=0,a=0,i,j,n;
    scanf("%d",&n);
    for(i=0;i<n;i++)
    {
    scanf("%d",&a);
    if(a%2==0)
    even++;
    else
    odd++;
    }
    if (even>odd)
    printf("READY FOR BATTLE");
    else
    printf("NOT READY");
    return 0;
    }

