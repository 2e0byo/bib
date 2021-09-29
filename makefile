format:
	find . -name "*.bib" | parallel -i{} python format.py {} \;
