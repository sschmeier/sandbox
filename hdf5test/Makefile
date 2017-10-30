# list all rules/targets
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: help
help:
	@echo "  run         Run analysis"
	@echo "  cleanbak    Remove emacs temp-files"
	@echo "  cleandata   Move current data to dated dir and delete data in current"
	@echo "  conda       Extract conda package information and create conda env freeze."

.PHONY : cleandata
cleandata: storedata rmdata

.PHONY : rmdata
rmdata :
	rm -f data/current/*

.PHONY : storedata
storedata :
	now=$$(date +"%Y-%m-%d_%H%M%S"); mkdir data/$$now; cp -r data/current/* data/$$now;

# Clean emacs backup files
.PHONY : cleanbak
cleanbak:
	find . -name '*~' |  xargs -I pattern rm pattern

.PHONY : conda
conda:
	conda list -e > conda-packages.txt
	conda env export > conda-env-freeze.yml

.PHONY : run
run:
	bash workflow.sh

