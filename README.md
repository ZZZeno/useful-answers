# useful-answers

some useful answers on other website

### difference between thread join and detach
thread join will block current thread, but detach will not. when thread detach invoked, this thread's status cannot be known by any thread, and its resources will be recycled by OS as soon as it finishes.

https://stackoverflow.com/questions/37015775/what-is-different-between-join-and-detach-for-multi-threading-in-c/37021767#37021767
