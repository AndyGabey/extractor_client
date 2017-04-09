#!/bin/bash
find log -name "load_extapi-*.out"|xargs tail -n1 -q|grep -v FAILED|awk '{total += $9} END {print total}'
