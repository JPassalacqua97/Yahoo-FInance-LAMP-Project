#!/bin/sh

for((i = 0; i < 60; i++)); do
    d=`date +%Y_%m_%d_%H_%M_%S`
    fn="yahoo_$d.html"

    wget -O $fn "https://finance.yahoo.com/most-active/"
    python hw8.py $fn
    sleep 1m
done