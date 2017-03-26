#!/usr/bin/env bash
cmd=load_extapi

for i in $(eval echo {1..$1}); do {
  echo "Process \"$i\" started";
  $cmd $2 $3 $4 & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";
