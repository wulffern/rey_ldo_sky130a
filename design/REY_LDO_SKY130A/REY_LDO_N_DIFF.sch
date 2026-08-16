v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=LPI}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=REF_1V2}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=VBP}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=VGSO}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=VS}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_11C5F0.sym} 400 0 0 0 {name=Xxdiff1}
N 440.0 -50.0 440.0 -30.0 {lab=VGSO}
C {devices/lab_pin.sym} 440.0 -50.0 3 0 {name=l0 sig_type=std_logic lab=VGSO }
N 380.0 0.0 400.0 0.0 {lab=REF_1V2}
C {devices/lab_pin.sym} 380.0 0.0 0 0 {name=l1 sig_type=std_logic lab=REF_1V2 }
N 440.0 50.0 440.0 30.0 {lab=VS}
C {devices/lab_pin.sym} 440.0 50.0 1 0 {name=l2 sig_type=std_logic lab=VS }
N 460.0 0.0 440.0 0.0 {lab=VSS}
C {devices/lab_pin.sym} 460.0 0.0 2 0 {name=l3 sig_type=std_logic lab=VSS }
C {REY_ATR_SKY130A/REYATR_NCH_11C5F0.sym} 400 170.0 0 0 {name=Xxdiff2}
N 440.0 120.0 440.0 140.0 {lab=VBP}
C {devices/lab_pin.sym} 440.0 120.0 3 0 {name=l4 sig_type=std_logic lab=VBP }
N 380.0 170.0 400.0 170.0 {lab=LPI}
C {devices/lab_pin.sym} 380.0 170.0 0 0 {name=l5 sig_type=std_logic lab=LPI }
N 440.0 220.0 440.0 200.0 {lab=VS}
C {devices/lab_pin.sym} 440.0 220.0 1 0 {name=l6 sig_type=std_logic lab=VS }
N 460.0 170.0 440.0 170.0 {lab=VSS}
C {devices/lab_pin.sym} 460.0 170.0 2 0 {name=l7 sig_type=std_logic lab=VSS }
