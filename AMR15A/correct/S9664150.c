
    #include <stdio.h>
    
    int main()
    {
    	int n;
    	scanf("%d",&n);
    	int a[n],i,even=0,odd=0;
    	for(i = 0; i < n; i++)
    	{
    		scanf("%d",&a[i]);
    		if((a[i] % 2) == 0)
    		{
    			even++;
    		}
    	}
    	odd = n - even;
    	if(even > odd)
    	{
    		printf("READY FOR BATTLE");
    	}
    	else
    	{
    		printf("NOT READY");
    	}
    	return 0;
    }
    	

