#!/bin/bash

  #exec > /dev/null 2>/dev/null
  
  WORKDIR=AUniquePlaceholderName
  #CONFIGDIR=ConfigDirPlaceholderName
  RELEASEDIR=ReleaseDirPlaceholderName
  
#  ZERO="" #$SGE_TASK_ID
#  if [ $SGE_TASK_ID -lt 1000 ]; then
#    ZERO="0"
#  fi
#  if [ $SGE_TASK_ID -lt 100 ]; then
#    ZERO="00"
#  fi
#  if [ $SGE_TASK_ID -lt 10 ]; then
#    ZERO="000"
#  fi
  JOB=`printf "%04d" "$SGE_TASK_ID"`

  # change to scratch directory (local, not lustre in this example)
  #cd $TMPDIR
  # copy raw data to scratch directory (here from the afs)
  # DO NOT USE afscp UNTIL FURTHER NOTICE afscp /afs/naf.desy.de/group/vo/rawdata/bigfile bigfile
  # cp /afs/naf.desy.de/group/vo/rawdata/bigfile bigfile
  #sleep $SGE_TASK_ID
  
  #cp -r $RELEASEDIR .
  #RELEASEBASE=`basename $RELEASEDIR`
  cd $RELEASEDIR/src
  #ini cmssw
  #cmsenv
  #pwd > stdout.txt
  #module use -a /afs/desy.de/group/cms/modulefiles/
  #module load cmssw/slc5_amd64_gcc472
  #cmsenv
  #which combine > stdout.txt
#  setenv SCRAM_ARCH slc5_amd64_gcc472
#  module load cmssw/slc5_amd64_gcc472
#  setcms
  #ini root530 

  cd $WORKDIR
  
  mkdir job$JOB/results
  mkdir job$JOB/log
  cd job$JOB

  pwd > stdout.txt
  
  export SCRAM_ARCH="slc5_amd64_gcc472"  
  export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"  
  echo "VO_CMS_SW_DIR = $VO_CMS_SW_DIR, SCRAM_ARCH = $SCRAM_ARCH" >> stdout.txt
  source $VO_CMS_SW_DIR/cmsset_default.sh  >> stdout.txt
  ini cmssw  >> stdout.txt
  ##cmsenv  >> stdout.txt
  eval `scramv1 runtime -sh`  >> stdout.txt 
  
  which combine >> stdout.txt
  echo "SGE_TASK_ID = $SGE_TASK_ID"  >> stdout.txt
  date   >> stdout.txt
  for i in `cat config/config_*`
  do    
    echo $i  >> stdout.txt
    cat ../../$i  >> stdout.txt
    file="${i##*/}"
    echo "copying ../../$i to config/$file"  >> stdout.txt
    cp ../../$i config/$file  
    echo "calling ../../limit config/$file"  >> stdout.txt
    ../../limit_V2 config/$file
  done
  du -h --max-depth=1 >> stdout.txt
  date   >> stdout.txt
  ls -l   >> stdout.txt

  #cp results/* job$SGE_TASK_ID/results/.
  mv stdout.txt log/.
  #cp stderr.txt log/.
  #cp -r job$SGE_TASK_ID $RESULTPATH/.

### qsub -t 1-3609 -l h_cpu=00:15:00 -l h_vmem=4000M job.sh
