
#Part 1
import numpy as np
from numpy import trapz


# The y values.  A numpy array is used here
y = np.array([4, 6, 6, 4, 4, 5])

# Compute the area using the composite trapezoidal rule.
area = trapz(y, dx=2)
print("area =", area)


#Part B
from mpi4py import MPI
comm =  MPI.COMM_WORLD
rank =  comm.Get_rank()
number_of_processors = comm.Get_size()

if rank !=0:
  message= "Hello from Josh" + str(rank)
  comm.send(message,dest=0)
else:
    for procid in range(1,number_of_processors):
      message=comm.recv(source=procid)
      print("Process 0 receives message from process",procid,":",message)



#Part C
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()


x0=0
x1=10
n=5
total=-1.00
destination=0

h=(x1-x0)/n

local_n=n/size


local_x0=x0+size*local_n*h
local_x1=local_x0+local_n*h
integral = area

if rank ==0:
    total=integral
    for source in range(1,size):
        integral=comm.recv(source=source)
        print("The process ranked: ",rank,"",source,",",integral,"\n")
        print("With n= ", n, " trapezoid number \n")
        print("Integral from: ", x0, " to ", x1, "=", total, "\n")

        total=total+integral
else:
    print("Process ranked: ",rank,"has sent it's result to destination",destination,",",integral,"\n")
    comm.send(integral,destination)

if (rank == 0):
     print("With n= ",n," trapezoid number \n")
     print("Integral from: ",x0," to " , x1 , "=" , total , "\n")
     print(size)

MPI.Finalize
