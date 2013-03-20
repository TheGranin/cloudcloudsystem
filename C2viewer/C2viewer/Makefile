# Makefile for the C2viewer
# (c) BŒrd Fjukstad,  bard.fjukstad@uit.no
# From SDLsample, (c) 2006 Daniel Stødle, daniels@cs.uit.no

CC	 	= gcc

ifeq ($(OSTYPE),darwin10.0)
	CFLAGS		= -Wall -g -O2 -I/opt/local/include/SDL -D_GNU_SOURCE=1 -D_THREAD_SAFE
	LDOPTS		= -lpthread -L/opt/local/lib -lSDLmain -lSDL -Wl,-framework,Cocoa -lSDL_image -lSDL_ttf
	SWITCH=osx
else
	CFLAGS		= -Wall -g -O2 `sdl-config --cflags`
	LDOPTS		= -lpthread `sdl-config --libs` -lSDL_image -lSDL_ttf
	SWITCH=else
endif

#CFLAGS		= -Wall -g -O2 `sdl-config --cflags`
#LDOPTS		= -lpthread `sdl-config --libs` -lSDL_image -lSDL_ttf
##CFLAGS		= -Wall -g -O2 `sdl-config --cflags`
##LDOPTS		= -lpthread -framework SDL

C2VIEWER_OBJS	= main.o

all: C2viewer


C2viewer: $(C2VIEWER_OBJS)
	$(CC) $(LDOPTS) -o $@ $^

clean:
	rm -f *.o *~ C2viewer
	rm -f .depend

depend: .depend
.depend:
	$(CC) $(CFLAGS) -MM *.c > $@

%.o:%.c
	$(CC) $(CFLAGS) -c -o $@ $<

-include .depend

