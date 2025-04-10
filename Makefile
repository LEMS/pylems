all:	lems-code lems-doc

JLEMSPATH = ../jLEMS
JLEMSBIN = lems
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
	pylems examples/example1.xml

example2:
	pylems examples/example2.xml

example3:
	pylems examples/example3.xml

example4:
	pylems examples/example4.xml

example5:
	pylems examples/example5.xml

example6:
	pylems examples/example6.xml

example7:
	pylems examples/example7.xml

example8:
	pylems examples/example8.xml

example9:
	pylems examples/example9.xml

ex0:
	pylems examples/LEMS_NML2_Ex0.xml

nmlex0:
	pylems ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex0_IaF.xml

nmlex1:
	pylems ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex1_HH.xml

nmlex2:
	pylems ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex2_Izh.xml

nmlex3:
	pylems ../NeuroML2/NeuroML2CoreTypes/LEMS_NML2_Ex3_Net.xml

run:	example1

bench:
	@echo "Java"
	env LEMS_HOME=${JLEMSPATH} ${TIME} ${JLEMSPATH}/${JLEMSBIN} ${BENCHFILE} -nogui 2>&1 > /dev/null

	@echo "CPython 2 (no optimizations)"
	@${TIME} python pylems -nogui ${BENCHFILE} > /dev/null

	@echo "CPython 2 (with optimizations)"
	@${TIME} python -O pylems -nogui ${BENCHFILE} > /dev/null

	@echo "PyPy"
	@${TIME} pypy pylems -nogui ${BENCHFILE} > /dev/null
