#! /bin/sh

git config --global http.proxy http://104.198.3.182:80

rm YouCompleteMe/ -r 

git clone --depth=1 --recursive 'https://github.com/Valloric/YouCompleteMe.git' '/home/zfchen/.vim/bundle/YouCompleteMe'

