all: C3Server

LIBS  = -lpthread -lc -ldl 

DEFS  = -DSYSV -D_POSIX_SOURCE -D_XOPEN_SOURCE -DByteSwapped -D__UNIXOS2__ -DNeedFuncProto -ansi -fPIC -O 
DBG   =  -g -Wall -pg

# HOME=/home/baardf
# LIBS  = -lncarg -lncarg_gks -lncarg_c -lgfortran -lXpm -lX11 -lXext -lnetcdf -lpthread -lc  -lhdf5 -lhdf5_hl
##DEFS  = -DSYSV -D_POSIX_SOURCE -D_XOPEN_SOURCE -DByteSwapped -D__UNIXOS2__ -DNeedFuncProto -ansi -fPIC 

ifeq ($(OSTYPE),darwin10.0)
	HOME  = /Users/bardf
	INCL  = -I$(HOME)/local/include -I/usr/include
	LIBCAT= -L$(HOME)/local/lib -L/usr/X11R6/lib -L/usr/local/lib -L/opt/local/lib -L/usr/lib 
else
	HOME  = /home
	INCL  = -I$(HOME)/local/include -I/usr/include
	LIBCAT= -L$(HOME)/local/lib -L/usr/X11R6/lib -L/usr/local/lib -L/opt/local/lib -L/usr/lib 
endif


CC=gcc
# CC=icc
CFLAGS=-I.  $(INCL)

DEPS=mongoose.h 
OBJ=main.o mongoose.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $<  $(CFLAGS)  $(DBG)

C3Server: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(DBG) $(DEFS) $(LIBCAT) $(LIBS)

clean:
	rm C3Server
	rm *.o
