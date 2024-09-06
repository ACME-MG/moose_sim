#!/bin/bash

nohup python3 sample_cvp_lh.py 0 > out_0.log 2>&1 &
nohup python3 sample_cvp_lh.py 1 > out_1.log 2>&1 &
nohup python3 sample_cvp_lh.py 2 > out_2.log 2>&1 &
nohup python3 sample_cvp_lh.py 3 > out_3.log 2>&1 &
