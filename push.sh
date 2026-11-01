#!/bin/bash
cd ~/my_website
git add .
git commit -m "${1:-cap nhat code}"
git push
