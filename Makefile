all:	lems-code lems-doc

lems-code:

lems-doc:
	epydoc -v -o doc/epydoc pylems

clean:
	find . -name "*.pyc" | xargs rm -f
	rm -rf doc/epydoc/*

test:
	# ./runlems.py examples/example1.xml
	./runlems.py examples/sawtooth.xml
