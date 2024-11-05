#!/bin/bash
if [ "$#" -eq 1 ]; then
  FILETYPE=$1
else
  echo "Specify file type, txt or pdf"
  exit 1
fi

if [ $FILETYPE == "txt" ]; then
  python3 graspi_igraph/tests.py txt
elif [ $FILETYPE == "pdf" ]; then
  python3 graspi_igraph/tests.py pdf
else
  echo "Unsupported file type. Must be txt or pdf"
  exit 1
fi