
    #include <stdio.h>
    int main(void) {
    	// your code goes here
    	int n,i,a[100],count1=0,count2=0;
    	scanf("%d",&n);
    	for(i=0;i<n;i++)
    	{
    		scanf("%d",&a[i]);
    		if(a[i]%2==0)
    		count1++;
    		else
    		count2++;
    	}
    	if(count1>count2)
    	printf("READY FOR BATTLE");
    	else
    	printf("NOT READY");
    	return 0;
    }
    

