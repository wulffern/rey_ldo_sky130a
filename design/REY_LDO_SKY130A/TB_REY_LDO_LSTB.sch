v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 390 -840 1190 -440 {flags=graph

y2=70
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1


divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0
node=re(lg_mag)
color=5
dataset=-1
unitx=1
logx=1
logy=0
sim_type=ac

y1=-72
autoload=1
x1=2
x2=9}
B 2 390 -420 1190 -20 {flags=graph


ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1

x2=9
divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=1
logy=0
sim_type=ac
x1=2
y1=-650
y2=180
color=4
node=re(lg_phase)
autoload=0
rawfile=$netlist_dir/TB_REY_LDO_LSTB.raw}
N -280 -130 -280 -110 {
lab=VDD_1V8}
N -280 -50 -280 -10 {
lab=0}
N -280 -10 -160 -10 {
lab=0}
N -110 -140 -80 -140 {
lab=VDD_1V8}
N -110 -100 -80 -100 {
lab=0}
N 220 -140 250 -140 {
lab=VDD_1V2}
N 220 -120 250 -120 {
lab=LPI}
N 300 -30 300 -10 {lab=0}
N -160 -10 300 -10 {lab=0}
N 300 -140 300 -90 {lab=VDD_1V2}
N 250 -140 300 -140 {lab=VDD_1V2}
C {devices/vsource.sym} -280 -80 0 0 {name=V1 value=\{vdda\} savecurrent=false}
C {devices/gnd.sym} -220 -10 0 0 {name=l1 lab=0}
C {devices/code_shown.sym} -299.3514969502943 -970 0 0 {name=s1 only_toplevel=false value="

.lib "../../../tech/ngspice/corners.spi" Ktt
.lib "../../../tech/ngspice/temperature.spi" Tt
.lib "../../../tech/ngspice/supply.spi" Vt
.include ../../../../cpdk/ngspice/tian_subckt.lib
X999 LPI VDD_1V2 loopgainprobe

.control
optran 0 0 0 10n 20u 0
save alli
save allv
save @m.*[gm]
op
remzerovec
write TB_REY_LDO_LSTB_OP.raw
unsave all

save allv
save i(v1) i(v2)
* Set voltage AC to 1
ac dec 50 100 1G
* Set Current to 1
alter i.X999.Ii acmag=1
alter v.X999.Vi acmag=0
ac dec 50 100 1G
let lg_mag = db(tian_loop())
let lg_phase = 180*cph(tian_loop())/pi
remzerovec
write TB_REY_LDO_LSTB.raw

meas ac gm_db find lg_mag when lg_phase=0
meas ac pm_deg find lg_phase when lg_mag=0
meas ac f3db when lg_phase=135
meas ac ug when lg_mag=0
meas ac lf_gain find lg_mag at=1k
remzerovec
write TB_REY_LDO_LSTB_meas.raw
exit
.endc
.end

"}
C {devices/launcher.sym} 460 -890 0 0 {name=h5
descr="load AC" 
tclcommand="xschem raw_read $netlist_dir/TB_REY_LDO_LSTB.raw ac"
}
C {devices/lab_wire.sym} -280 -130 0 0 {name=p6 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} -110 -140 0 0 {name=p7 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} -110 -100 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/capa.sym} 310 -220 0 0 {name=C1
m=1
value=1f
footprint=1206
device="ceramic capacitor"}
C {devices/lab_wire.sym} 310 -250 0 0 {name=p11 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 310 -190 0 1 {name=p12 sig_type=std_logic lab=LPI}
C {REY_LDO_SKY130A/REY_LDO.sym} 70 -120 0 0 {name=x1}
C {devices/lab_wire.sym} 250 -140 0 1 {name=p1 sig_type=std_logic lab=VDD_1V2}
C {devices/lab_wire.sym} 250 -120 0 1 {name=p2 sig_type=std_logic lab=LPI}
C {devices/res.sym} 300 -60 0 0 {name=R1
value=1e6
footprint=1206
device=resistor
m=1}
