#!/bin/bash

#This script converts a temperature from degrees Fahrenheit to degress Celcius.

echo -n "Enter a temperature in degrees Fahrenheit ->"
read a

b=$(($a-32))
c=$(($b*5))

d=$(($c/9))

echo "$a degrees Fahrenheit is equal to $d degress Celcius"
