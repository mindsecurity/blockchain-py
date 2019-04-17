#!/bin/bash
 set -e
 nosetests -sv --with-xunit --xunit-file=nosetests.xml --cover-xml  --cover-xml-file=FILE
