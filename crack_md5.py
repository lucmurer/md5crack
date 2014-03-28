import pyopencl as cl
import numpy as np

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

input_hash = np.array(('d41d8cd98f00b204e9800998ecf8427e',))

mf = cl.mem_flags
hash_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_hash)
result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, size=32)
result_string = np.zeros_like(result_buf)

with open('md5.cl', 'r') as f:
    fstr = ''.join(f.readlines())
    prg = cl.Program(ctx, fstr).build()

prg.crack(queue, (1,), None, hash_buf, result_buf)
cl.enqueue_copy(queue, result_string, result_buf).wait()
print(result_string)
