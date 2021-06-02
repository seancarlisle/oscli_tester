Script to test OpenStack clients from Newton to Train (with more to come.)
The idea here is to verify where older clients can no longer talk to the
APIs. This testing is by no means exhaustive, but it does touch the main 
clients and confirms API communication. While I firmly believe that you 
should always use latest stable clients, sometimes users have a 
hard time understanding that...

## Usage
Run from the directory. The os-version doesn't matter, it's more for 
documentation purposes in the testing output.

root@localhost:~/oscli_tester#./oscli_tester.py
usage: osa-tester.py [-h]
                     {newton,ocata,pike,queens,rocky,stein,train,ussuri}
                     os-version


