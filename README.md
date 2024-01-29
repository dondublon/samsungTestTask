# The Queue


The 1st option - I use DB (SQLIte in my case) and leverage on its indexes. 
Of course, I can do the index myself, but it would be just a reproduction of DB indexes.
Each time I add a task, it is inserted in the perfect position. Of course, it consumes some time.
The index is: resources (3 items) + priority. 
While we request for a task, anyway we cut-off tasks that are otu of resources, 
then we can take the maximum priority. 

Also, potentially we can consider asynchronous adding/retrieving here, and database handles it better. 
I guess, this functionality of out of the test task scope. 
