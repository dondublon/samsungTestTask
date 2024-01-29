# The Queue


I use DB (SQLIte in my case) and leverage on its indexes. 
Of course, I can do the index myself, but it would be just a reproduction of DB indexes.
Each time I add a task, it is inserted in the perfect position. 
The first step - the DB engine consider `ram` border, for each `ram` value if considers `cpu_cores` interval, 
for each `ram` value and `cpu_cores` it founds `gpu_count` interval.
Of course, it consumes some time, but in general it works quite quick. 

There are some tasks ordered by priority, we can take the 1st one.  
 
While we request for a task, anyway we cut-off tasks that are otu of resources, 
then we can take the maximum priority. 

Also, potentially we can consider asynchronous adding/retrieving here, and database handles it better. 
I guess, this functionality of out of the test task scope. 
