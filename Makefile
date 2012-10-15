all:	lems-code lems-doc

JLEMSPATH = ../LEMS
TIME = /usr/bin/time -f '%E s'
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

example1:
	./runlems.py examples/example1.xml

example2:
	./runlems.py examples/example2.xml

run:	example2

bench:
	@echo "Java"
	@${TIME} ${JLEMSPATH}/lems ${JLEMSPATH}/${BENCHFILE} -nogui > /dev/null

	@echo "CPython 2 (no optimizations)"
	@${TIME} python runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "CPython 2 (with optimizations)"
	@${TIME} python -O runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "PyPy"
	@${TIME} pypy runlems.py -nogui ${BENCHFILE} > /dev/null

