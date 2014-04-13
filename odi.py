#!/usr/bin/env python3
########################################################################
#
# Project:      OpenCL Device Info
#
# File:         odi.py
# Created on:   13.04.2014
# Changed on:   13.04.2014
# Author:       Lukas Murer <lmurer@hsr.ch>
#
########################################################################

print ()
print ('(Py)OpenCL Device Info tool,v0.1')
print ('      (c) 2014 Lukas Murer')
print ()



########################################################################
# Imports
########################################################################

import argparse


try:
  import pyopencl as cl

except ImportError:
  print ('FATAL: Could not load PyOpenCL.')
  print ('  To use this OpenCL Device Info tool, you need pyopencl to be installed.')
  print ('  You can get it from "https://pypi.python.org/pypi/pyopencl".')
  print ()
  print ('EXITING')
  exit(-1)




def usage():
  odi_args = argparse.ArgumentParser(prog='(Py)OpenCL Device Info tool')
  odi_args.add_argument('-v','--verbose',dest='v',action='store_true',help='Show details')
  odi_args.add_argument('-vv','--more-verbose',dest='vv',action='store_true',help='Show more details')
  odi_args.add_argument('-vvv','--show-all',dest='vvv',action='store_true',help='Show anything %(prog)s can get')
  
  return odi_args.parse_args()


cmdline = usage()

# Make more contain successors
if cmdline.vvv:
  cmdline.vv = True
  cmdline.v = True

elif cmdline.vv:
  cmdline.v = True
  




def clPrintTF(value_clBool):
  return "True" if (value_clBool == 1) else "False"



def print_prop(description, prop, offset, length):
  print (' '*offset + '+ -- ' + description + ' '*((length - len(description)) if (length > len(description)) else 0) + prop)



def listDevices(platform, pl_num, offset=4):
  devices = platform.get_devices()
  i = 0
  
  field_length = 24
  
  if (len(devices) == 1):
    print_prop ('Found %d compute device:' % len(devices),'', offset-2, field_length)
  elif (len(devices) > 1):
    print_prop ('Found %d compute devices:' % len(devices),'', offset-2, field_length)
  else:
    print_prop ('Found no compute devices!','', offset-2, field_length)
  
  for dev in devices:
    print_prop ('Device #%d.%d:' % (pl_num, i), dev.name.strip(), offset,  field_length+2 )
    
    offset += 2
    
    if cmdline.v:
      # General information
      print_prop ('Available:',    clPrintTF(dev.available), offset, field_length)
      print_prop ('Vendor (VID):', '%s (%d)' % (dev.vendor, dev.vendor_id), offset, field_length)
      print_prop ('Version:', dev.version, offset, field_length)
      print_prop ('Driver version:', dev.driver_version, offset, field_length)
      print_prop ('Profile:', 'full' if (dev.profile == 'FULL_PROFILE') else 'embedded', offset, field_length)
      print_prop ('Type:', str(dev.type), offset, field_length)
      
    
    if cmdline.vv: 
      print_prop ('Has compiler:', clPrintTF(dev.compiler_available), offset, field_length)
      print_prop ('Error correction:',clPrintTF(dev.error_correction_support), offset, field_length)
      print_prop ('Execution cap.:', str(dev.execution_capabilities), offset, field_length)
      print_prop ('Extensions:',dev.extensions, offset, field_length)
      print_prop ('Endianess:', '%s' % 'Little' if (dev.endian_little == 1) else 'Big', offset, field_length)
      
      # Device properties
    if cmdline.v:
      print_prop ('Clock frequency (max):', '%d MHz' % dev.max_clock_frequency, offset, field_length)
      print_prop ('Compute units:', '%d' % dev.max_compute_units, offset, field_length)
      print_prop ('Global memory:','%d MB' % (dev.global_mem_size/1024), offset, field_length)
      print_prop ('Local memory:', '%d MB, %s' % (dev.local_mem_size,dev.local_mem_type), offset, field_length)
    
    if cmdline.vv:
      # Mem information
      print_prop ('Address bits:', str(dev.address_bits), offset, field_length)
      print_prop ('Global Cache:', '%d MB, %s' % (dev.global_mem_cache_size/1024, dev.global_mem_cache_type), offset, field_length)
      print_prop ('-- Line size:','%d B' % dev.global_mem_cacheline_size, offset, field_length)
      print_prop ('Max const. buffer:', '%d B' % dev.max_constant_buffer_size, offset, field_length)
      print_prop ('Max mem alloc:', '%d B' % dev.max_mem_alloc_size, offset, field_length)
      print_prop ('Mem alignment:', '%d' % dev.mem_base_addr_align, offset, field_length)
      print_prop ('Mem align size:', '%d' % dev.min_data_type_align_size, offset, field_length)
      
      # Kernel options
    if cmdline.vvv:
      print_prop ('Max param. size:', '%d B' % dev.max_parameter_size, offset, field_length)
      print_prop ('Max wg size:', '%d' % dev.max_work_group_size, offset, field_length)
      print_prop ('Max work item dim.:', '%d' % dev.max_work_item_dimensions, offset, field_length)
      print_prop ('Max work item size:', str(dev.max_work_item_sizes), offset, field_length)
      
      # Floating point capabilities
      print_prop ('FP (double prec.):', str(dev.double_fp_config), offset, field_length)
      print_prop ('FP (single prec.):', str(dev.single_fp_config), offset, field_length)
      #print_prop ('       + -- FP (half prec.):   %d' % dev.half_fp_config, offset, field_length)
      
      # Other capabilities
      print_prop ('Image support:', clPrintTF(dev.image_support), offset, field_length)
      print_prop ('-- 2D max (w/h):', '%d/%d' % (dev.image2d_max_width,dev.image2d_max_height), offset, field_length)
      print_prop ('-- 3D max (w/h/d):', '%d/%d/%d' % (dev.image3d_max_width,dev.image3d_max_height,dev.image3d_max_depth), offset, field_length)
      print_prop ('Max image args (R):', '%d' % dev.max_read_image_args, offset, field_length)
      print_prop ('Max image args (W):', '%d' % dev.max_write_image_args, offset, field_length)
      print_prop ('Prof. timer res.:', str(dev.profiling_timer_resolution), offset, field_length)
      print_prop ('Queue properties:', str(dev.queue_properties), offset, field_length)
      
      # Datatypes
      print_prop ('Max samplers:', '%d' % dev.max_samplers, offset, field_length)
      print_prop ('Preferred vector size:','', offset, field_length)
      print_prop ('-- CHAR:', str(dev.preferred_vector_width_char), offset, field_length)
      print_prop ('-- SHORT:', str(dev.preferred_vector_width_short), offset, field_length)
      print_prop ('-- INT:', str(dev.preferred_vector_width_int), offset, field_length)
      print_prop ('-- LONG:', str(dev.preferred_vector_width_long), offset, field_length)
      print_prop ('-- FLOAT:', str(dev.preferred_vector_width_float), offset, field_length)
      print_prop ('-- DOUBLE:', str(dev.preferred_vector_width_double), offset, field_length)
    

    i += 1

def listPlatforms(offset=2):
  platforms = cl.get_platforms()
  i = 0
  offset = 4
  field_length = 18
  
  if (len(platforms) == 1):
    print ('Found %d OpenCL platform:' % len(platforms))
  elif (len(platforms) > 1):
    print ('Found %d OpenCL platforms:' % len(platforms))
  else:
    print ('Found no OpenCL platforms!')
  
  
  for pl in platforms:
    print (' + Platform #%d: "%s":'  % (i, pl.name.strip()))
    print_prop ('Vendor:', pl.vendor, offset, field_length)
    version_str = '%s (on %s)' % (pl.version[7:10], pl.version[11:].lower())
    print_prop ('Version:', version_str, offset, field_length)
    
    if cmdline.v:
      print_prop ('Profile:', 'full' if pl.profile == 'FULL_PROFILE' else 'embedded', offset, field_length)
      
    if cmdline.vv:
      exts = pl.extensions.split(' ')
      print_prop ('Extensions:', exts[0], offset, field_length)
      for extension in exts[1:]:
        print (' '*(offset + field_length + 5) + extension)
      
    listDevices(pl, i, offset + 2)
      
           
    
    
    i+= 1
  



if (__name__ == '__main__'):
  listPlatforms()
  print ()
  
