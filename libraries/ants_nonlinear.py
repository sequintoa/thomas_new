#!/usr/bin/env python


import os
import sys
from parallel import command


def bias_correct(input_image, output_image, **exec_options):
    cmd = 'N4BiasFieldCorrection -d 3 -i %s -o %s -b [200] -s 3 -c [50x50x30x20,1e-6]' % (input_image, output_image)
    command(cmd, **exec_options)
    return output_image, cmd

def ants_nonlinear_registration(template, input_image, output, switches='', linear=False, cost='CC', **exec_options):
    """Do nonlinear registration with ANTS as in buildtemplateparallel.sh"""
    if linear:
        iterations = '0'
    else:
        iterations = '30x90x20'
    cmd = 'ANTS 3 -m %s[%s,%s,1,5] -t SyN[0.25] -r Gauss[3,0] -o %s -i %s --use-Histogram-Matching --number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000 %s' % (cost, template, input_image, output, iterations, switches)
    output_warp = output+'Warp.nii.gz'
    output_affine = output+'Affine.txt'
    command(cmd, **exec_options)
    return output_warp, output_affine, cmd

def ants_new_nonlinear_registration(template, input_image, output, switches='', **exec_options):
    """Do nonlinear registration with antsRegistration"""
    cmd = 'antsRegistration -d 3 --float 0 --output %s -t Affine[0.1] --metric MI[%s,%s,1,32,Regular,0.25] -r [rigid0GenericAffine.mat,1] --convergence [1000x500x250x100,1e-6,10] -f 8x4x2x1 -s 3x2x1x0vox -t SyN[0.1,3.0] --metric CC[%s,%s,1,4] --convergence [70x70x20,1e-6,10] -f 4x2x1 -s 2x1x0vox' % (output, template, input_image, template, input_image)
    output_warp = output+'Warp.nii.gz'
    output_affine = output+'Affine.txt'
    command(cmd, **exec_options)
    return output_warp, output_affine, cmd

def ants_v0_nonlinear_registration(template, input_image, output, switches='', **exec_options):
    """Do nonlinear registration with antsRegistration but no -r option """
    cmd = 'antsRegistration -d 3 --float 0 --output %s -t Affine[0.1] --metric MI[%s,%s,1,32,Regular,0.25] --convergence [1000x500x250x100,1e-6,10] -f 8x4x2x1 -s 3x2x1x0vox -t SyN[0.1,3.0] --metric CC[%s,%s,1,4] --convergence [70x70x20,1e-6,10] -f 4x2x1 -s 2x1x0vox' % (output, template, input_image, template, input_image)
    output_warp = output+'Warp.nii.gz'
    output_affine = output+'Affine.txt'
    command(cmd, **exec_options)
    return output_warp, output_affine, cmd



def ants_linear_registration(template, input_image, cost='CC', **exec_options):
    cmd = 'ANTS 3 -m %s[%s,%s,1,5] -o linear -i 0 --use-Histogram-Matching --number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000 --rigid-affine true' % (cost, template, input_image)
    output_warp = 'linearWarp.nii.gz'
    output_affine = 'linearAffine.txt'
    command(cmd, **exec_options)
    return output_warp, output_affine, cmd

def ants_oldrigid_registration(template, input_image, cost='CC', **exec_options):
    cmd = 'ANTS 3 -m %s[%s,%s,1,5] -o linear -i 0 --use-Histogram-Matching --number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000 --rigid-affine false' % (cost, template, input_image)
    output_warp = 'linearWarp.nii.gz'
    output_affine = 'linearAffine.txt'
    command(cmd, **exec_options)
    return output_warp, output_affine, cmd


def ants_rigid_registration(fixed, moving, cost='MI', **exec_options):
    cmd = 'antsRegistration -d 3 --float 0 --output rigid -t Rigid[0.1] -r [%s,%s,1]  --metric %s[%s,%s,1,32,Regular,0.25] --convergence [1000x500x250x100, 1e-6,10] -v -f 8x4x2x1 -s 3x2x1x0vox' % (fixed, moving, cost, fixed, moving)
    output_warp = 'rigid.nii.gz'
    output_rigid = 'rigidGeneric0Affine.txt'
    command(cmd, **exec_options)
    return output_warp, output_rigid, cmd


def ants_apply_warp(template, input_image, input_warp, input_affine, output_image, switches='', ants_apply=False, **exec_options):
    if ants_apply:
        cmd = os.path.join(this_path, 'tools', 'WarpImageMultiTransform.py')+' %s %s %s %s %s %s' % (switches, input_image, output_image, template, input_warp, input_affine)
    else:
        cmd = 'WarpImageMultiTransform 3 %s %s %s %s -R %s %s' % (input_image, output_image, input_warp, input_affine, template, switches)
    command(cmd, **exec_options)
    return output_image, cmd


this_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    try:
        template, input_image, output_warp = sys.argv[1:]
    except ValueError:
        print '%s <template reference> <input image> <output warp>' % sys.argv[0]
        sys.exit(1)

    ants_nonlinear_registration(template, input_image, output_warp)
