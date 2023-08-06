#!/bin/bash -e

export PATH=$PATH:`pwd`/out

export NETWORK=ganache

export PYTHONPATH=`pwd`

export PUBLIC=`cat /tmp/0.pub`
export PRIVATE=`cat /tmp/0.prv`

export WEB3_PROVIDER_URI=http://localhost:${PORT}

export WALLET=0

echo Using Network $NETWORK...

$*
