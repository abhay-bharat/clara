
    #include<stdio.h>
    int main()
     {
      int n, s,e=0,o=0;
      scanf("%d",&n);
      while(n--)
       {
        scanf("%d",&s);
        if(s%2==0)
         e++;
        else 
         o++;
       }
       if(e>0)
        printf("READY FOR BATTLE\n");   
       else
        printf("NOT READY\n"); 
      return 0;
     } 

