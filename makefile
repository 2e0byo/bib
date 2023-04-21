.PHONY: format install

format:
	find . -name "*.bib" | parallel -i{} python format.py {} \;

install:
	cp .hook .git/hooks/pre-commit
