# for x86_64-w64-mingw64 need the full name of the compiler.
CC = x86_64-w64-mingw32-gcc.exe
#CC = gcc

EXTRA_FLAGS = 

CFLAGS = \
-DDLL_EXPORT -DPIC \
-I$N/include -I$N/src/scopmath -I$N/src/nrnoc -I$N/src/oc \
$(EXTRA_FLAGS)

TARGET=nrnmech.dll

bin = bin

# to handle variations of filename extensions
.SUFFIXES: .o .mod .moD .mOd .mOD .Mod .MoD .MOd .MOD
.PRECIOUS: %.c

%.o : %.mod

%.c : %.mod
	nocmodl $*

%.o : %.c
	$(CC) $(CFLAGS) -c $*.c

# additional rules to handle variations of filename extensions
%.c : %.moD
	nocmodl $*

%.c : %.mOd
	nocmodl $*

%.c : %.mOD
	nocmodl $*

%.c : %.Mod
	nocmodl $*

%.c : %.MoD
	nocmodl $*

%.c : %.MOd
	nocmodl $*

%.c : %.MOD
	nocmodl $*

%.o : %.moD

%.o : %.mOd

%.o : %.mOD

%.o : %.Mod

%.o : %.MoD

%.o : %.MOd

%.o : %.MOD

mod_func.o: mod_func.c
	$(CC) $(CFLAGS) -c $*.c

nrnmech.dll: mod_func.o $(MODOBJFILES)
	$(CC) $(EXTRA_FLAGS) -shared mod_func.o $(MODOBJFILES) \
  -L$N/$(bin) -lnrniv -lpthread -o $(TARGET)
	#rebase -b 0x64000000 -v nrnmech.dll

mod_func.o $(MODOBJFILES): $(N)/$(bin)/nrniv.exe


