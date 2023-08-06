#!/bin/bash

## install-upgrade-data-science-stack

# are we called from a GUI?
USE_PKEXEC=0

# did the caller specify the new version to upgrade the data stack to?
NEW_VER=""
if [ $# -ge 1 ]
then  
  echo "received NEW_VER param: $NEW_VER"
  NEW_VER="$1"
fi

if [ $# -ge 2 ]
then  
  echo "received USE_PKEXEC param: $2"
  USE_PKEXEC="$2"
fi

## do we have some version of the data science stack already installed?
if [ -d "$HOME/data-science-stack" ]
then
   ## the idea is that we simply back it up
   ver=`grep '^STACK_VERSION=' $HOME/data-science-stack/data-science-stack | cut -d '=' -f2 | xargs`
   echo "existing installation of data-science-stack $ver detected.. backing it up"
   if [ -d "$HOME/data-science-stack-backup-${ver}" ]
   then
     subver=1
     while [ -d "$HOME/data-science-stack-backup-${ver}.${subver}" ]
     do
       subver=$((subver+1))
     done
     mv "$HOME/data-science-stack" "$HOME/data-science-stack-backup-${ver}.${subver}"
     echo "backed up dss to $HOME/data-science-stack-backup-${ver}.${subver}"
   else  
     mv "$HOME/data-science-stack" "$HOME/data-science-stack-backup-${ver}"
   fi
fi

pushd $HOME

if [ -z "$NEW_VER" ] 
then
  echo "installing the latest version of the data science stack"
  git clone https://github.com/NVIDIA/data-science-stack.git
else
  echo "installing tag $NEW_VER of the data science stack"
  git clone -b v"${NEW_VER}"  https://github.com/NVIDIA/data-science-stack.git
fi  

pushd ${HOME}/data-science-stack

if [ "$USE_PKEXEC" -eq 0 ]
then
 echo "regular install"
 bash ./data-science-stack setup-system
 if [ $? -ne 0 ]
 then
  echo "data science stack install failed"
  exit 1
 fi
else # driver only
 echo "pkexec driver only install"
 pkexec bash ${HOME}/data-science-stack/data-science-stack install-driver
 if [ $? -ne 0 ]
 then
  echo "data science stack driver install failed"
  exit 1
 fi
fi
popd
popd
# echo "UPGRADE done, please log out and log back in"
exit 0