#!/usr/bin/python3

import sys
import time
import binascii
import pyopencl as cl
import math as m

MAX_PW_LEN = 8

# Read hash from arguments
if len(sys.argv) != 2:
    print('Usage: ./crack_md5.py <md5hash>')
    sys.exit(-1)
input_hash = bytearray(binascii.unhexlify(sys.argv[1]))

# Create context and queue
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Prepare result objects
result = bytearray(MAX_PW_LEN)
result_string = bytearray(MAX_PW_LEN)

# Prepare buffers
mf = cl.mem_flags
hash_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_hash)
result_buf = cl.Buffer(ctx, mf.WRITE_ONLY | mf.COPY_HOST_PTR, hostbuf=result)

with open('md5.cl', 'r') as f:
    fstr = ''.join(f.readlines())
    prg = cl.Program(ctx, fstr).build()

# Define work sizes
global_worksize = (int(m.pow(26,2)), int(m.pow(26,1)), int(m.pow(26,1)))
local_worksize = None

# Start measuring time
t0 = time.time()

# Run kernel!
prg.crack(queue, global_worksize, local_worksize, hash_buf, result_buf)

# Copy result back to device
cl.enqueue_read_buffer(queue, result_buf, result_string).wait()

# Get elapsed time
t1 = time.time()

# Strip null bytes, convert to unicode
plaintext = result_string.strip(b'\x00').decode('ascii')
if plaintext:
    print('Result is "%s"!' % plaintext)
else:
    print('Did not find a result.')

# Print stats
print('\nStats\n-----\n')
print('- Elapsed time: %fs' % (t1 - t0))
print('- Keyspace: %d' % (26 ** MAX_PW_LEN))
print('- Searched: %d' % ((26 ** 6)))

maxtime = ((26 ** 2) * (t1 - t0))

days = maxtime / (24*60*60)
maxtime = maxtime % (24*60*60)
hours = maxtime / (60 * 60)
maxtime = maxtime % (60*60)
mins = maxtime / 60
secs = maxtime % 60

print('- Time to search keyspace ((26^2)^3): %d days, %d hours, %d mins, %d seconds' % (days, hours, mins, secs))
