all:	lems-code lems-doc

TIME = /usr/bin/time -f '%e s'
MODELFILE = examples/curvetooth.xml

lems-code:

lems-doc:
	epydoc -v -o doc/epydoc pylems

clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "*.pyo" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	rm -rf doc/epydoc/*

test:
	# ./runlems.py examples/example1.xml
	./runlems.py ${MODELFILE}

example1:
	./runlems.py examples/example1.xml

bench:
	@echo "Java"
	@${TIME} ../LEMS/lems-nogui ${MODELFILE} > /dev/null

	@echo "CPython (no optimizations)"
	@${TIME} python runlems.py ${MODELFILE} > /dev/null

	@echo "CPython (with optimizations)"
	@${TIME} python -O runlems.py ${MODELFILE} > /dev/null

	@echo "PyPy"
	@${TIME} pypy runlems.py ${MODELFILE} > /dev/null

