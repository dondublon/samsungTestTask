# The Queue


I use DB (SQLIte in my case) and leverage on its indexes.
Of course, I can do the index myself, but it would be just a reproduction of DB indexes functionality.

Let's designate:
* amount of possible priority values as |P|,
* amount of possible ram values as |Ra|,
* the same for CPU count - |C|
* the same for GPU amount - |G|.
* |Ra|*|C|*|G|=|R| (resources)

The main "fork" in approach is - if we have rather small |P| value (for example, 100 or even 
1000 possible priority options) with large |R|, or, otherwise, large |P| with small |R| 
(for example |Ra|, |C|, |G| < 100).

Depending on this, there are two approached to create DB indexes:
1. Priority, then Ram, CPU, CPU.
2. Ram, CPU, GPU - then Ram. 

(Consider the 2nd option.
Each time I add a task, it is inserted in the perfect position. 
The first step - the DB engine consider `ram` border, for each `ram` value if considers `cpu_cores` interval, 
for each `ram` value and `cpu_cores` it founds `gpu_count` interval.
Of course, it consumes some time, but in general it works quite quick.

There are some tasks ordered by priority, we can take the 1st one. )
 
While we request for a task, anyway we cut-off tasks that are otu of resources, 
then we can take the maximum priority. 

As additional approach, I implemented the queue myself using arrays (numpy arrays for convenience and Python lists).
This approach is super-fast, especially when |R| is not very big, but less scalable.
Please, consider DB way as the main one. 

Also, potentially we can consider asynchronous adding/retrieving here, and database handles it better. 
I guess, this functionality of out of the test task scope. 
