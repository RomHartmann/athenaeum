#!/usr/bin/env bash
git clone https://github.com/aiff22/DPED

brew install coreutils
brew install swig
brew cask install homebrew/cask-versions/java8
brew install bazel

brew tap caskroom/drivers
brew cask install nvidia-cuda

pip install -r requirements.txt
