
    #include <stdio.h>
    #include <stdlib.h>
    
    int main()
    {
       int S,i,W,ready=0,notready=0;
       scanf("%d\n",&S);
       for(i=0;i<S;i++)
       {
           scanf("%d",&W);
           if(W%2==0)
            ready++;
            else
                notready++;
       }
       if(ready>notready)
       {
           printf("READY FOR BATTLE\n");
       }
       else
        printf("NOT READY\n");
       return 0;
    }
    

