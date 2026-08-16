v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 560 -370 760 -370 {lab=VSS}
N 560 -340 650 -340 {lab=VS}
N 650 -340 760 -340 {lab=VS}
N 100 -100 310 -100 {lab=VSS}
N 250 -270 290 -270 {lab=VSS}
N 250 -270 250 -100 {lab=VSS}
N 100 -600 310 -600 {lab=VDD_1V8}
N 260 -500 290 -500 {lab=VSS}
N 250 -500 260 -500 {lab=VSS}
N 250 -500 250 -270 {lab=VSS}
N 400 -370 400 -300 {lab=REF_1V2}
N 310 -370 400 -370 {lab=REF_1V2}
N 400 -230 400 -100 {lab=VSS}
N 310 -100 400 -100 {lab=VSS}
N 400 -370 520 -370 {lab=REF_1V2}
N 400 -100 650 -100 {lab=VSS}
N 650 -160 650 -100 {lab=VSS}
N 630 -220 630 -100 {lab=VSS}
N 1040 -520 1080 -520 {lab=VDD_1V8}
N 1080 -550 1080 -520 {lab=VDD_1V8}
N 1040 -550 1080 -550 {lab=VDD_1V8}
N 310 -600 1040 -600 {lab=VDD_1V8}
N 1040 -600 1040 -550 {lab=VDD_1V8}
N 760 -540 800 -540 {lab=VDD_1V8}
N 800 -600 800 -540 {lab=VDD_1V8}
N 760 -600 760 -570 {lab=VDD_1V8}
N 600 -540 720 -540 {lab=VBP}
N 520 -540 560 -540 {lab=VDD_1V8}
N 520 -600 520 -540 {lab=VDD_1V8}
N 560 -600 560 -570 {lab=VDD_1V8}
N 560 -510 560 -400 {lab=VGSO}
N 760 -510 760 -400 {lab=VBP}
N 1000 -520 1000 -450 {lab=VGSO}
N 1040 -400 1090 -400 {lab=VDD_1V2}
N 690 -540 690 -490 {lab=VBP}
N 1040 -490 1040 -400 {lab=VDD_1V2}
N 650 -340 650 -290 {lab=VS}
N 610 -260 650 -260 {lab=VS,R1[1:0]}
N 650 -180 710 -180 {lab=R1[1:0],VSS}
N 800 -370 840 -370 {lab=LPI}
N 310 -540 360 -540 {lab=VDD_1V8,R2[1:0]}
N 310 -310 340 -310 {lab=REF_1V2,R3[4:0]}
N 310 -460 310 -420 {lab=R2[1:0],REF_1V2}
N 310 -420 360 -420 {lab=R2[1:0],REF_1V2}
N 310 -230 310 -200 {lab=R3[4:0],VSS}
N 310 -200 340 -200 {lab=R3[4:0],VSS}
N 690 -490 760 -490 {lab=VBP}
N 560 -450 1000 -450 {lab=VGSO}
N 910 -500 910 -450 {lab=VGSO}
N 910 -600 910 -570 {lab=VDD_1V8}
N 960 -530 960 -450 {lab=VGSO}
C {cborder/border_xs.sym} 0 0 0 0 {
user="wulff"
company="wulff"}
C {devices/ipin.sym} 100 -600 0 0 {name=p1 lab=VDD_1V8}
C {devices/ipin.sym} 100 -100 0 0 {name=p2 lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_11C5F0.sym} 520 -370 0 0 {name=xdiff1}
C {REY_ATR_SKY130A/REYATR_NCH_11C5F0.sym} 800 -370 0 1 {name=xdiff2}
C {devices/lab_wire.sym} 660 -370 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} 650 -260 1 0 {name=xres_vs1[2:0]}
C {devices/lab_wire.sym} 660 -340 0 0 {name=p4 sig_type=std_logic lab=VS}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} 310 -540 1 0 {name=xres2[2:0]}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} 310 -310 1 0 {name=xres1[5:0]}
C {REY_ATR_SKY130A/REYATR_CAPX1.sym} 400 -240 0 0 {name=xfcap[3:0]}
C {REY_ATR_SKY130A/REYATR_PCH_11C1F2.sym} 1000 -520 0 0 {name=xout1}
C {REY_ATR_SKY130A/REYATR_PCH_11C5F0.sym} 600 -540 0 1 {name=xload[1:0]}
C {REY_ATR_SKY130A/REYATR_PCH_11C5F0.sym} 720 -540 0 0 {name=xload1[1:0]}
C {devices/opin.sym} 1090 -400 2 1 {name=p5 lab=VDD_1V2}
C {devices/lab_wire.sym} 430 -370 0 1 {name=p6 sig_type=std_logic lab=REF_1V2}
C {devices/lab_wire.sym} 940 -450 0 1 {name=p7 sig_type=std_logic lab=VGSO}
C {devices/lab_wire.sym} 710 -490 0 1 {name=p8 sig_type=std_logic lab=VBP}
C {REY_ATR_SKY130A/REYATR_CAPX1.sym} 910 -560 2 0 {name=xgcap2[9:0]}
C {devices/lab_wire.sym} 610 -260 0 0 {name=p9 sig_type=std_logic lab=VS,R1[1:0]}
C {devices/lab_wire.sym} 710 -180 0 1 {name=p10 sig_type=std_logic lab=R1[1:0],VSS}
C {devices/ipin.sym} 840 -370 0 1 {name=p11 lab=LPI}
C {devices/lab_wire.sym} 310 -540 0 1 {name=p12 sig_type=std_logic lab=VDD_1V8,R2[1:0]}
C {devices/lab_wire.sym} 330 -420 0 1 {name=p13 sig_type=std_logic lab=R2[1:0],REF_1V2}
C {devices/lab_wire.sym} 310 -310 0 1 {name=p14 sig_type=std_logic lab=REF_1V2,R3[4:0]}
C {devices/lab_wire.sym} 310 -200 0 1 {name=p15 sig_type=std_logic lab=R3[4:0],VSS}
C {REY_ATR_SKY130A/REYATR_CAPX1.sym} 960 -590 2 1 {name=xhcap1[9:0]}
