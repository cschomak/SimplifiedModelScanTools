#!/bin/bash

  #exec > /dev/null 2>/dev/null
  
  #WORKDIR=AUniquePlaceholderName
  #CONFIGDIR=ConfigDirPlaceholderName
  RELEASEDIR=~/CMSSW_release/CMSSW_6_1_1
  
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
  pwd > stdout.txt
  export SCRAM_ARCH="slc5_amd64_gcc472"  
  export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"  
  echo "VO_CMS_SW_DIR = $VO_CMS_SW_DIR, SCRAM_ARCH = $SCRAM_ARCH" >> stdout.txt
  source $VO_CMS_SW_DIR/cmsset_default.sh  >> stdout.txt
  ini cmssw  >> stdout.txt
  cmsenv
  which combine > stdout.txt
#  setenv SCRAM_ARCH slc5_amd64_gcc472
#  module load cmssw/slc5_amd64_gcc472
#  setcms
  #ini root530 
