## What is it

This is loader of [AssemblyScript](https://www.assemblyscript.org/) wasm-modules for Python. It use [Wasmer for Python](https://github.com/wasmerio/wasmer-python) as backend. This loader is a direct port of the default [AssemblyScript loader](https://github.com/AssemblyScript/assemblyscript/tree/main/lib/loader) from JavaScript to Python. Also we use [wasmbind](https://github.com/miracle2k/wasmbind) as reference.

## How to install

Simply

```pip install pyaswasm```

## Supported features

* Convert strings and numeric arrays from Python to wasm memory and back
* Allows to create objects from Python inside wasm memory
* Create Python wrappers of objects from wasm memory. This allows to call object's methods directly from Python

## How to use

### The simplest example

```python
# import module
from pyaswasm import ASModule

# instantiate wasm module
module = ASModule("some_module.wasm")

# we can output all functions from the module
print(module.description())
# this will print all global variables, functions and classes, which can be used with this module

# let, for example, out module contains function sqrt_sum_square(float32, float32) -> float32
# this function return sqrt(a^2 + b^2)
# we can use it in the following way
v = module.sqrt_sum_square(3.0, 4.0)
print(v)  # this will output 5.0
```

### How to define custom imports

When the module is instantiated, it may requires some callbacks. For example, wasm module can use external functions. To define it implementation we should use importer dictionary. For example, to implement function ```console.log(str)``` in the Python host, ww should write
```python
def console_log(ptr: int):
    print(console_log.module.get_string(ptr))

# ...

module = ASModule("math.some_module", imports={("index", "console.log"): console_log})
```

Notice that for all functions in the imports dictionary the module add it reference. So, we can use the module inside the function (call ```console_log.module.get_string``` in the example).

The module use default functions for ```abort```, ```trace``` and ```seed```, but it's possible to override it.

If you would like to define signature of the imported functions, then to the tuple ```("module name", "function name")``` in the imports dictionary you should instead function juxtapose the tuple ```(function, ([input types], [output types]))```. For example, for the ```console_log``` function it should be 

```
imports={("index", "console.log"): (console_log, ([Type.I32], []))}
```

### How to use arrays

Wasm module return pointers to all non-numeric values in the memory. So, if we use arrays, then it should be created inside the memory and then we should use pointer to the corresponding data block for functions and any other calculations.

```python
from pyaswasm import ASModule

# import wasm module with array functionality
module = ASModule("array.wasm") 

# we would like to generate random float array
float_array_ptr = module.generate_random_float_array(10, -2.0, 2.0)  # this will return pointer to the array
float_array = module.get_array(float_array_ptr)  # convert to Python array

# in the same way we can generate integer array
int_array_ptr = module.generate_random_integer_array(10)
int_array = module.get_array(int_array_ptr)
print(int_array)

# we can change integer array from Python and simultaneously change it values in the memory
# for this purpose we should use method get_array_view
view, start, finish = module.get_array_view(int_array_ptr)  # view is not actual array, but a whole memory, interpreted as integer values
# change the second value
view[start + 1] = 50
# then again get array from the pointer and look at the second element
int_array = module.get_array(int_array_ptr)
print(int_array[1])  # this will output 50
```

Also we can create array from Python side. But it's important to remember, that all data, creating from Python side, should be pinned in the memory to preserve it destruction from garbage collector.

```python
from pyaswasm import ASModule
import random

module = ASModule("array.wasm") 

# create an array, we should use the method new_array
# also the module should contains global value as a type id for the array, Float32Array_ID in out example
a_ptr = module.new_array(module.Float32Array_ID, [random.uniform(-1.0, 1.0) for i in range(10)])

# next pin the pointer
module.pin(a_ptr)

# then we can make any calculations with this array
# when we does not need this array anymore, unpin it
module.unpin(a_ptr)
# and this will allows to clear the memory by garbage collector
```

### How to use float array view

By default wasmer does not support float view of the memory, but we can use bytes of the array elements.

```python
from pyaswasm import ASModule
import random
import struct

module = ASModule("array.wasm") 

a_ptr = module.new_array(module.Float32Array_ID, [random.uniform(-1.0, 1.0) for i in range(10)])
module.pin(a_ptr)  # we should pin this pointer to preserve it from garbage collector
a = module.get_array(a_ptr)  # variable a contains copy of the array from the memory
a[1] = 16.0
b = module.get_array(a_ptr)
print(a[1] == b[1])  # print False

view, start, finish = module.get_array_view(a_ptr)  # view contains bytes of the array
# we know that array contains f32 values, so, one value corresponds to 4 bytes
# we would like to change the second value array[1] to 17.0
view[start + 4 * 1 : start + 4 * 2] = struct.pack("f", 17.0)
print(module.get_array(a_ptr))  # return the second element = 17.0
module.unpin(a_ptr)
```

### How to use strings

There are two methods for strings: ```get_string(ptr) -> str``` convert pointer of the string to Python string, ```new_string(str) -> int``` write string to the memory and return pointer to it.

```python
from pyaswasm import ASModule

module = ASModule("string.wasm") 

# get string from the wasm memory
hello_ptr = module.get_hello_string()  # this will return integer pointer to the string
hello_str = module.get_string(hello_ptr)
print(hello_str)  # output Hello world!

# how to create the string
msg_ptr = module.new_string("message string")  # this will create string in the memory and return pointer to it
module.pin(msg_ptr)  # pin it, because we need this string in the memory
newmsg_ptr = module.expand_string(msg_ptr)  # this will return pointer to the new string, generated by module function
newmsg_str = module.get_string(newmsg_ptr)
print(newmsg_str)
module.unpin(msg_ptr)
```

### How to use classes

Classes can be used in two scenarios. The first one is using object from the wasm memory.

```python
from pyaswasm import ASModule

module = ASModule("vector3d.wasm")
# we assume that this module contains class Vector3d and some functions with objects of this class

vectors_ptr = module.get_random_vectors(5)  # return pointer to the array
vectors_array = module.get_array(vectors_ptr)  # this will return array with integer values - pointers to objects
vectors = [module.Vector3d.wrap(v) for v in vectors_array]  # now each element of the array is Python object, which linked with object in the wasm memory
# wrap method automatically pin pointer to the object and unpin it at the end of the object's life cycle
# we can call methods of the objects
# for example, calculate length of each vector
print([v.length() for v in vectors])  # length() is a method in the class inside the module
```

The second scenario is creating object in the wams memory from Python side. Continue the previous example
```python
new_vector = module.Vector3d(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))  # we does not need to pin pointer to this object, because it pinned and unpinned automatically
vectors.append(new_vector)
# next we would like to find minimum distance between points (which corresponds to vectors) in the array
# now vectors variable contains Python array, so, we should convert it to the array inside wasm memory
vectors_ptr = module.new_array(module.VectorsArray_ID, vectors)
module.pin(vectors_ptr)
min_distance = module.get_minimum_distance(vectors_ptr)  # this will return float value
print("minimum distance is", min_distance)
module.unpin(vectors_ptr)
```

## Performance

We use benchmark from [Path Finder](https://github.com/Tugcga/Path-Finder), which contains wasm module for path finding tasks. We use navigation mesh with 2 294 polygons, select different pairs of points and find shortest path between these points in the navigation mesh. The following table contains execution time of different tasks for Node.js (by using default AssemblyScript loader) and Wasmer (by using our loader).

| Task | Node.js | Wasmer |
|---|---|---|
initialization | 0.06 sec | 0.17 sec
1024 pairs | 0.16 sec | 0.47 sec
4096 pairs | 0.52 sec | 1.71 sec
16 384 pairs | 2.16 sec | 6.94 sec
38 416 pairs | 5.19 sec | 16.05 sec
65 536 pairs | 8.63 sec | 27.27 sec

The result: Wasmer is nearly 3.1-3.2 times slowly than Node.js.