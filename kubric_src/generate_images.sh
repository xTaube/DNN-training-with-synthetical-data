#!/bin/bash

for iter in {0..50}
do
  python3 worker.py -i "$iter" -o testing
done