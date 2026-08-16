

all:
	${MAKE} typical etc TB=lstb LCORNER="Li,Lh"
	${MAKE} typical etc TB=psrr LCORNER="Li,Lh"
	${MAKE} typical etc TB=tran
	${MAKE} summary

TB=lstb
VIEW=Sch
#VIEW=Lay
CELL=REY_LDO
LIB =REY_LDO_SKY130A
OPT=
THREADS=8
PROGRESS=--progress

#- lstb and psrr sweep the load as a corner (Li idle, Lh 200 uA);
#- tran drives its own load step and takes no L corner
LCORNER=Gt

include ../../tech/make/sim.make

test:
	${MAKE} typical OPT="Debug"

typical: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt "${LCORNER}"

slow: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Th,Tl" Vl "${LCORNER}"

fast: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Th,Tl" Vh "${LCORNER}"

tfs: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_tfs ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt,Th,Tl" "Vt,Vl,Vh" "${LCORNER}"

etc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs" "Th,Tl" "Vl,Vh" "${LCORNER}"

mc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_mc --count 30 ${TB} ${OPT} ${VIEW} Gt "Kttmm" "Tt" "Vt" "${LCORNER}"

temp: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt "${LCORNER}"

summary:
	cicsim summary --output "README.md"
	-pandoc -o README.html README.md -s

slide:
	pandoc -s -t slidy README.md -o README.html

clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm *.run
	-rm *.pdf
	-rm *.csv
