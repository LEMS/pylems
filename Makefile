all:	lems-code lems-doc

JLEMSPATH = ../LEMS
TIME = /usr/bin/time -f '%E s'
MODELFILE = examples/example1.xml
BENCHFILE = examples/sawtooth_bench.xml

lems-code:

lems-doc:
	mkdir -p doc/epydoc
	epydoc -v -o doc/epydoc pylems

clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "*.pyo" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	rm -rf doc/epydoc/*

run:
	./runlems.py ${MODELFILE}

example1:
	./runlems.py examples/example1.xml

bench:
	@echo "Java"
	@${TIME} ${JLEMSPATH}/lems ${JLEMSPATH}/${BENCHFILE} -nogui > /dev/null

	@echo "CPython 2 (no optimizations)"
	@${TIME} python runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "CPython 2 (with optimizations)"
	@${TIME} python -O runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "PyPy"
	@${TIME} pypy runlems.py -nogui ${BENCHFILE} > /dev/null

