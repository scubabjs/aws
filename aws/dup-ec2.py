#!/usr/bin/env python3
#  Copyright (c) 2020 - Brian J. Smith
#  Version 0.1
#
# Given:  
#       1 - Two EC2 instances abc and abc-x
	2 - clb that has abc in pool of nodes
# 
# Desired Output:
#	1 - Replicated abc instance, but in a shared tenancy pool.
	2 - Remount of ebs volumes with no copying.
#	
#       Remove abc from clb pool
#	shutdown abc
#	stop all non-os applications
#	snapshot abc /root ebs
#	Remove all non-/root ebs volumes from abc	
#	shutdown abc
#	Boot abc-x
#	Replicate /root ebs volume to abc-x /root2 ebs volume
#
#
#
