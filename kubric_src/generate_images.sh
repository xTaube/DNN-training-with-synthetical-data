#!/bin/bash

for iter in {0..10}
do
  python3 worker.py -i "$iter" -o testing
done