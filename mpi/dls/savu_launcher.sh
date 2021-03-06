#!/bin/bash
module load global/cluster

echo "SAVU_LAUNCHER:: Running Job"

datafile=$1
processfile=$2
outpath=$3
shift 3
options=$@

outname=savu
nNodes=2
nCoresPerNode=20

DIR="$(cd "$(dirname "$0")" && pwd)"
filepath=$DIR'/savu_mpijob.sh'
savupath=${DIR%/mpi}

M=$((nNodes*nCoresPerNode))

log_path=/dls/tmp/savu
while [[ $# -gt 1 ]]
do
if [ $1 == "-l" ]
  then
  log_path=$2
fi
shift
done

qsub -N $outname -sync y -j y -o $log_path -e $log_path -pe openmpi $M -l exclusive -l infiniband -l gpu=1 -q medium.q@@com10 $filepath $savupath $datafile $processfile $outpath $nCoresPerNode $options > /dls/tmp/savu/$USER.out

echo "SAVU_LAUNCHER:: Job Complete, preparing output..."

filename=`echo $outname.o`
jobnumber=`awk '{print $3}' /dls/tmp/savu/$USER.out | head -n 1`
filename=/dls/tmp/savu/$filename$jobnumber

while [ ! -f $filename ]
do
  sleep 2
done

echo "SAVU_LAUNCHER:: Output ready, spooling now"

cat $filename

echo "SAVU_LAUNCHER:: Process complete"

