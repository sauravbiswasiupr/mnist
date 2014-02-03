#!/bin/bash 
./mnist_lstm.py -c mnist_train.pkl mnist_train.nc 
./mnist_lstm.py -c mnist_valid.pkl mnist_valid.nc 
./mnist_lstm.py -c mnist_test.pkl mnist_test.nc 