import pyopencl as cl
import numpy as np

MAX_PW_LEN = 4

# Create context and queue
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Prepare objects for input hash and result
input_hash = bytearray('9a8ad92c50cae39aa2c5604fd0ab6d8c'.encode('ascii'))
result = bytearray(MAX_PW_LEN)

# Prepare buffers
mf = cl.mem_flags
hash_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_hash)
result_buf = cl.Buffer(ctx, mf.WRITE_ONLY | mf.COPY_HOST_PTR, hostbuf=result)

with open('md5.cl', 'r') as f:
    fstr = ''.join(f.readlines())
    prg = cl.Program(ctx, fstr).build()

# Define work sizes
global_worksize = (26,)
local_worksize = None

# Run kernel!
prg.crack(queue, global_worksize, local_worksize, hash_buf, result_buf)

# Copy result back to device
result_string = bytearray(MAX_PW_LEN)
cl.enqueue_read_buffer(queue,result_buf, result_string).wait()
print(result_string)
