#!/bin/bash

#This script moves an inputted file to the trash directory.

if [ ! -d /home/brett/trash ]
	then
		mkdir -p /home/brett/trash
fi

echo "Please enter a file you would like to move to the trash."
	read filename

if [ -f $filename ]
	then
		mv $filename /home/brett/trash
		echo "The file $filename was moved to the trash folder in your home directory."
		
	else
		echo "File $filename does not exist."
fi
