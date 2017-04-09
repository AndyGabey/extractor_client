#!/usr/bin/env bash
cmd=load_extapi

for i in $(eval echo {1..$1}); do {
  echo "Process \"$i\" started";
  sleep 0.1
  $cmd $2 $3 > log/$cmd-$i.out & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";
