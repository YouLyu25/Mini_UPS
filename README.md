The code for UPS web-app is in directory project/web-app.\
The code for UPS server is in directory project/ups_Docker
The world simulator is in directory project/world_Docker

To run the UPS web-app and UPS server as well as the "world", simply use
"sudo docker-compose up".

Note that due to the race condition of multiple docker containers (some
containers may try to connect to another at the starting up, but if the container
it depends on does not start at the time, the connecting container may report
error and exit, during our test we found that the world container will suffer for
such issue when trying to connect the postgres DB server), the user may need to
run "sudo docker-compose up" for several times to have a stable server state.

That says, if any container "EXITS" due to errors, please run the command again.


To tackle with the issue where Amazon side does not function properly, the UPS
server and web-app can be tested independently in the following way:

------------------------------------------------------------------------------------
1. First, the user needs to run:
"sudo docker-compose up"
to start the UPS, web-app and world containers.
Note that for testing purpose the UPS server will create a new world for every run
of the containers.

The user can now run "amazon_server" under directory /ups_Docker using:
"python3 ./amazon_server"

and provide the warehouse number (for testing, set to 10 will be fine) as well as
the ups_host name/address and world_host name/address (these two are the same and
will be the machine name currently running containers, could be vcm-XX.vm.duke.edu)
and also the warehouse id (could enter 1 for now).
The "amazon_server.py" is the testing software which breifly simulates Amazon's
behavior for sending messages to UPS. The user may consider run this testing
program in a different machine.
The testing software will now connect to UPS server and use the worldid provided by
UPS to connect to the world and initialize the warehouse in that world.
The user should record the worldid printed in testing software's end for later use.


------------------------------------------------------------------------------------
2. The user may now need to set up the warehouse and stocking information in the
world's database to simulate the operation of Amazon.

2.1 The user needs to use similar way to look for the "world" container's name:
"sudo docker container ls"
and the results will be "project_world_X" where X can be an arbitrary number.

2.2 The user needs to enter:
"sudo docker exec -it project_world_X /bin/bash"
to attach a terminal and interact with the world container where project_world_X is
the name of world container just looked up.
The result is an attached terminal with information like:
"postgres@343df7783df1:/sim$ "

2.3 The user can now check the scripts under /sim directory using "ls", and then
run the .sh file named "init_whread.sh" using:
"./init_whready.sh [worldid_the_testing_program_received]"
This operation will init the warehouse stocks for our testing, to be specific,
warehouse 1 will now have package with packageid 1, warehouse 2 will now have
package with packageid 2, and so forth. There will be 11 warehouse in total fromi
warehouse 1 to warehouse 10, each contains a package with corresponding packageid.

2.4 The user now needs to enter:
"./rst_truckhas.sh [worldid_the_testing_program_received]"
to clear the truck state.

2.5 The user will now terminate the containers and amazon_server.py.


------------------------------------------------------------------------------------
3. Run the containers using:
"sudo docker-compose up"
again and then run:
"python3 ./amazon_server.py"
and enter the warehouse number (use 10 for testing) and warehouse id (use 1 for
testing) as well as the ups_host and world_host name/address.


------------------------------------------------------------------------------------
The user is now able to see the testing result via accessing webpage:
"vcm-XXX.vm.duke.edu:8000/ups_frontend/"
and register a user with username "yl489" (this is the username that testing program
will associated to), a valid email address and an address with pos_x is 10 and
pos_y is 10.
The user can then log in an see the status of his/her package.

Note that for each run of "amazon_server.py", the user may specify a warehouse id
which has not been used during previous tests. This is because when a package is
successfully delivered, its record in "whready" datatable of world will be cleared.
For our testing, the packageid and warehouse id are set to be the same. That means
warehouse 1 will store only package 1. Therefore, if warehouse id 1 is used for the
first run of "amazon_server.py", and the package is successfully delivered, the
warehouse will not have package 1 anymore, hence if the UPS dispatch a truck to
that warehouse, an error will be returned from the world indicating package 1 is
not in warehouse 1.

What the tester could do is to run "amazon_server.py" with warehouse id 1 for the
first time, run "amazon_server.py" with warehouse id 2 for the second time, run
"amazon_server.py" with warehouse id 3 for the third time and so forth.
When the warehouse id reaches 9, the tester will have to reset the "whready" and
"truckhas" table using the procedures introduced in step 3 above.



We realize that it may be a bit of cumbersome to do the testing in this way,
however, this is what we have to do to test our program under the case that the
Amazon group may still need some further work to make the whole system works
well. We are sorry for any inconvenience brought but this is the way that we
demonstrate our work and the functionality of our UPS system as we have tested it
for a large amount of runs.










