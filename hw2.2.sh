#!/bin/bash

#This script gives a count of thenu mber of files and subdirectories in the current directory.

a=$(ls | wc -l)

echo "There are $a files and/or subdirectories in the current directory"

