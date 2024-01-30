# The Queue


## 1st Approach, using DB. The main one. 
I use DB (SQLIte in my case) and leverage on its indexes.
Of course, I can do the index myself, but it would be just a reproduction of DB indexes functionality.

Let's designate:
* amount of possible priority values as |P|,
* amount of possible ram values as |Ra|,
* the same for CPU count - |C|
* the same for GPU amount - |G|.
* |Ra| * |C| * |G|=|R| (resources)

The main "fork" in the approach is - if we have large |P| with small |R| 
(for example |Ra|, |C|, |G| < 100), OR, otherwise, we have rather small |P| value (for example, 100 or even 
1000 possible priority options) with large |R|. 

Depending on this, there are two approaches to create DB indexes:
1. Ram, CPU, GPU - then Ram.
2. Priority, then Ram, CPU, CPU.
 
Consider the 1nd option more closely.
Each time I add a task, it is inserted in the perfect position. 
The first step - the DB engine consider `ram` border, for each `ram` value if considers `cpu_cores` interval, 
for each `ram` value and `cpu_cores` it founds `gpu_count` interval.
While we request for a task, anyway we cut-off tasks that are out of resources, 
then we can take the maximum priority. 
Of course, it consumes some time, but in general it works quite quick.
There are some tasks ordered by priority, we can take the 1st one. 

The second approach does analogous. We got the tasks sorted by priority, 
then we quickly go to `ram` values that fits us, then `cpu_cores`, then `gpu_count`.    
 
## 2nd approach, using arrays, the additional one.

As an additional approach, I implemented the queue myself using arrays (numpy arrays for convenience and Python lists).
This approach entirely in memory, it is super-fast, especially when |R| is not very big, but less scalable.
Please, consider DB way as the main one. 

Also, potentially we can consider asynchronous adding/retrieving here, and database handles it better. 
I guess, this functionality of out of the test task scope. 
