Memory Management in Python
===========================

[Mostly from here](https://realpython.com/python-memory-management/)

Python interpreter actually converts python code into byte code that get run on a virtual machine.

Default python interpreter is CPython.
- *CPython* is different from *Cython*
  - CPython is pure C, and is the most common python distribution.
  - Cython is an extension of python that allows you to compile python code.
    - You typically compile slow code, then import it as regular python code.
    - Cython requires types to be declared, optimises memory etc.
    - Cython also allows importing and calling a function from C libraries in python.


**--- Cython sidetrack ---**

Say we have a slow function

```python
# func.py
def looper(n):
    k = 0
    for i in range(n):
        for j in range(n):
            k += j
    return k
```

To convert to cython:

```cython
# func.pyx
import cython
cimport cython
 
cpdef long looper(int n):
    cdef long i, j, k = 0
    for i in range(n):
        for j in range(n):
            k += j
    return k
```

**--- end sidetrack ---**

Since python bytecode is interpreted by CPython in C, here are some C infos:
- C does not natively support objects
    - C has a `struct` called `PyObject` which is the grand daddy that all objects use.
        - a `struct` is a custom data type in C that groups together different data types.  Analagous to a class with atrributes and no methods.
    - `PyObject` contains only two things:
        - `ob_refcnt`: reference count.  Used for garbage collection.
        - `ob_type`: pointer to another type.
    - Objects also a memory allocator and deallocator.
    
GIL:
- locks the entire enterpreter such that only one thread at a time can access a single resource.

Garbage collection:
- `PyObject` has attribute `ob_refcnt`.
    - count gets increased for different reasons, eg:
        - when object is assigned to another variable (`a=1; b=a` makes count=2)
        - Pass object as an argument
        - include object in list
    - When this count drops to 0, the object's deallocation function frees it from memory.
    
CPython's Memory Management:
- The operating system abstracts the physical memory and creates a virtual memory layer that python accesses.
    - The virtual memory manager carves out chunk of memory for python process.
        - CPython then partitions this chunk:
            - Some of that memory is used for python's internals.
            - The rest is dedicated to object storage.
        - Heap:
            - memory set aside for dynamic allocation.  This means there is no enforced pattern to allocation and deallocation.
                - i.e allocate and deallocate at any time.  Makes memory management more complex.
            - generally only one heap per application.
        - Stack:
            - Stack memory is allocated to each thread.
            - Last In First Out allocation
                - i.e The oldest block is always first to be freed.
                - Thus freeing a block is simple: just adjust one pointer.
- CPython has an object allocator that allocates memory within the object memory area.
    - It gets called every time a new object needs space allocated or deleted.
        - Adding and removing is tuned to be fast for objects that don't require much memory, and tries to be used as little as possible.
    - Main components of of memory:
        - *Arena*:
            - Largest chunk of memory
            - Aligned on a page boundary in memory.  
                - This is the edge of a fixed-length contiguous chunk of memory that the os uses.
                    - English: big block of memory
                - Python assumes this is 256 kilobytes.
            - This carved out first from os.
            - Really nice, because we can free entire arena in one go without having to worry about individual deallocations.
            - It's kinda like the heap: 
        - *Pool*:
            - Subset of Arena
                - 4 kB in size
            - Composed of blocks from a single size class (i.e. all blocks in pool would be (default) 8 bytes)
            - Can be `empty`, `used`, `full`.  Used still has available blocks to be stored.
        - *Block*:
            - Subset of Block
            - Data is placed into blocks with size class, and the block size is allocated by rounding up 2^n.
            - Pools contain pointers to free blocks of memory.
    - Memory allocation strategy:
        - A "freed" block is not actually freed to the OS, it's just available for reallocation.
            - python keeps them allocated, probably helps with speed.
        - The fullest Arena's are selected to place data into first.  I think this prevents empty memory from being written into needlessly.
            - The fullest Arena's may contain Pools that have blocks available to put data into.
        - Tries to "leave memory alone unless needed."

**Thoughts**

- This comes through as to some weirdness in python when using `is` to compare two objects.
    - A lot of objects are allocated early on (for example `1` is allocated hundreds of times by time code runs) and can just be reused.
    - The value of `1`, that is the object that is type `int` and uses up 8 bytes etc has a block that is used.
        - This block sits in a pool with other blocks of size 8 bytes.
        - The containing Arena will probably be first in line to be read/written to, and so least amount of actual writing will have to be done
        every time a 1 comes up, because that memory allocation already exists.

- This gave me a nice overview into pointers and how objects deal with memory via CPython.















