all:	lems-code lems-doc

JLEMSPATH = ../jLEMS
JLEMSBIN = lemsio
TIME = /usr/bin/time -f '%E s'
BENCHFILE = ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex2_Izh.xml

lems-code:

lems-doc:
	mkdir -p doc/epydoc
	epydoc -v -o doc/epydoc lems

clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "*.pyo" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	rm -rf doc/epydoc/*

example1:
	./runlems.py examples/example1.xml

example2:
	./runlems.py examples/example2.xml

example3:
	./runlems.py examples/example3.xml

example4:
	./runlems.py examples/example4.xml

example5:
	./runlems.py examples/example5.xml

example6:
	./runlems.py examples/example6.xml

example7:
	./runlems.py examples/example7.xml

example8:
	./runlems.py examples/example8.xml

example9:
	./runlems.py examples/example9.xml

ex0:
	./runlems.py examples/LEMS_NML2_Ex0.xml

nmlex0:
	./runlems.py ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex0_IaF.xml

nmlex1:
	./runlems.py ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex1_HH.xml

nmlex2:
	./runlems.py ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex2_Izh.xml

nmlex3:
	./runlems.py ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex3_Net.xml

run:	example9

bench:
	@echo "Java"
	env LEMS_HOME=${JLEMSPATH} ${TIME} ${JLEMSPATH}/${JLEMSBIN} ${BENCHFILE} -nogui 2>&1 > /dev/null

	@echo "CPython 2 (no optimizations)"
	@${TIME} python runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "CPython 2 (with optimizations)"
	@${TIME} python -O runlems.py -nogui ${BENCHFILE} > /dev/null

	@echo "PyPy"
	@${TIME} pypy runlems.py -nogui ${BENCHFILE} > /dev/null

