#!/bin/bash

REMOTE_PORT=9999
REMOTE_HOST="REMOTE_HOST"

# $COMMAND is the command used to create the reverse ssh tunnel
COMMAND="/usr/bin/ssh -q -N -R $REMOTE_PORT:localhost:22 $REMOTE_HOST -o ExitOnForwardFailure=yes -o ServerAliveInterval=10"

CHECK_TUNNEL=`ps auxw | grep "$COMMAND" | grep -v grep`

if [ -z "$CHECK_TUNNEL" ]; then
  $COMMAND
fi
