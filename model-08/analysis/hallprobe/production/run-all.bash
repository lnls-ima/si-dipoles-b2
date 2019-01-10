#!/usr/bin/env bash

func=$1
cmd=$2
current=$3
side=$4

folder=x0-8p165mm

function f1 {
  cmd=$1
  current=$2
  side=$3
  cd $folder/B2-001/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-002/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-003/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-004/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-005/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-006/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-007/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-008/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-009/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-010/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
}

function f2 {
  cmd=$1
  current=$2
  side=$3
  cd $folder/B2-011/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-013/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-014/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-015/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-016/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-017/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-018/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-019/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-021/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-022/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
}

function f3 {
  cmd=$1
  current=$2
  side=$3
  cd $folder/B2-023/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-024/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-025/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-026/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-027/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-028/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-029/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-030/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-031/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-032/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
}

function f4 {
  cmd=$1
  current=$2
  side=$3
  cd $folder/B2-033/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-034/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-036/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-037/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-038/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-040/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-042/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-043/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-044/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-045/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
  cd $folder/B2-046/$current/$side; fac-fma-analysis.py $cmd; cd ../../../../
}

$func $cmd $current $side

# ./run-all.bash f1 run 381p7A z-positive
# ./run-all.bash f2 run 381p7A z-positive
# ./run-all.bash f3 run 381p7A z-positive
# ./run-all.bash f4 run 381p7A z-positive
# ./run-all.bash f1 run 381p7A z-negative
# ./run-all.bash f2 run 381p7A z-negative
# ./run-all.bash f3 run 381p7A z-negative
# ./run-all.bash f4 run 381p7A z-negative
# 
# ./run-all.bash f1 run 401p8A z-positive
# ./run-all.bash f2 run 401p8A z-positive
# ./run-all.bash f3 run 401p8A z-positive
# ./run-all.bash f4 run 401p8A z-positive
# ./run-all.bash f1 run 401p8A z-negative
# ./run-all.bash f2 run 401p8A z-negative
# ./run-all.bash f3 run 401p8A z-negative
# ./run-all.bash f4 run 401p8A z-negative
# 
# ./run-all.bash f1 run 421p9A z-positive
# ./run-all.bash f2 run 421p9A z-positive
# ./run-all.bash f3 run 421p9A z-positive
# ./run-all.bash f4 run 421p9A z-positive
# ./run-all.bash f1 run 421p9A z-negative
# ./run-all.bash f2 run 421p9A z-negative
# ./run-all.bash f3 run 421p9A z-negative
# ./run-all.bash f4 run 421p9A z-negative
