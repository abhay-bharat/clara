
    #include<stdio.h>
    int main()
    {
    	int n;
    	scanf("%d",&n);
    	int a[n],i,even=0,odd=0;
    	for(i=0;i<n;i++)
    	{
    		scanf("%d",&a[i]);
    		if(a[i]/2==0)
    		  even++;
    		else
    		  odd++;
    		
    	}
    	
    	if(even>odd)
    	  printf("THey ARE ReadY");
    	else
    	  printf("THEY are NOT ReadY");
    	  return 0;	
    } 

