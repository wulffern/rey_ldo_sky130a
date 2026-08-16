REY_LDO: a 1.2 V low-dropout regulator. The reference is a
resistive divider from VDD_1V8 (no bandgap), buffered by a
two-stage amplifier driving a PMOS pass device; the load range
checked is 0 to 200 uA.


#### Loop stability (lstb)

Loop broken between VDD_1V2 and the feedback input LPI with a
Tian probe. Checked at both ends of the load range (Li: no
load, Lh: 200 uA).



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.000** | **60.000** | **120.000** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**23.452**</span> |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.404**</span> | <span style='color:red'>**27.600**</span> | 55.516 | |
|**Gain Margin**|**gm\_db** || **Spec**  | **-100.000** | **-10.000** | **-8.000** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -51.805 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-99.000 | -15.694 | <span style='color:red'>**-0.255**</span> | |
|**DC loop gain**|**lf\_gain** || **Spec**  | **25.000** | **40.000** | **80.000** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 43.686 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**21.098**</span> | 49.540 | 62.219 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **0.050** | **1.000** | **100.000** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 71.035 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|3.869 | 49.565 | <span style='color:red'>**190.913**</span> | |
|**Output voltage**|**v(vdd\_1v2)** || **Spec**  | **1.1000** | **1.2000** | **1.3000** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.1262 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.8747**</span> | 1.1437 | <span style='color:red'>**1.4524**</span> | |
|**Reference voltage**|**v(xdut.ref\_1v2)** || **Spec**  | **1.1000** | **1.2000** | **1.3000** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.1992 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|1.1309 | 1.1973 | 1.2731 | |

#### Transient (tran)

Load step 0 -> 200 uA -> 0 (100 ns edges) and a -100 mV line
dip, closed loop. Droop, overshoot, load and line regulation,
quiescent current.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Output voltage, no load**|**vout\_light** || **Spec**  | **1.1000** | **1.2000** | **1.3000** | **V** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.1568 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**1.0197**</span> | 1.1377 | <span style='color:red'>**1.4036**</span> | |
|**Output voltage, 200 uA load**|**vout\_heavy** || **Spec**  | **1.0500** | **1.2000** | **1.3000** | **V** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.1745 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.8747**</span> | 1.1288 | 1.2640 | |
|**Load step droop (absolute)**|**vload\_min** || **Spec**  | **0.9000** | **1.1000** | **1.3000** | **V** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**-3.9575**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-7.0407**</span> | <span style='color:red'>**-3.2298**</span> | <span style='color:red'>**-0.4327**</span> | |
|**Load release overshoot (absolute)**|**vload\_max** || **Spec**  | **1.1000** | **1.2500** | **1.4500** | **V** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**1.7319**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:orange'>**1.5014**</span> | <span style='color:red'>**1.6838**</span> | <span style='color:red'>**1.8709**</span> | |
|**Load regulation (0 to 200 uA)**|**loadreg\_v** || **Spec**  | **-10.000** | **20.000** | **100.000** | **mV** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**-17.675**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-100.922**</span> | 12.909 | <span style='color:red'>**263.223**</span> | |
|**Line regulation (-100 mV step)**|**linereg\_v** || **Spec**  | **40.000** | **67.000** | **90.000** | **mV** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**-31.691**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-147.176**</span> | 54.822 | <span style='color:red'>**298.344**</span> | |
|**Quiescent supply current**|**idd\_light** || **Spec**  | **2.000** | **20.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 27.684 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|15.938 | 24.027 | 33.084 | |

#### PSRR (psrr)

1 V AC on VDD_1V8, closed loop; PSRR = db(v(VDD_1V2)) over
10 Hz to 100 MHz, at both load ends.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**PSRR at DC (10 Hz)**|**psrr\_dc** || **Spec**  | **-10.000** | **-3.500** | **-2.000** | **dB** |
| | | |<a href='results/psrr_Sch_typical.html'>Sch_typ</a>| | -2.432 |  | |
| | | |<a href='results/psrr_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-17.146**</span> | -2.975 | <span style='color:red'>**20.751**</span> | |
|**PSRR at 1 kHz**|**psrr\_1k** || **Spec**  | **-10.000** | **-3.500** | **-2.000** | **dB** |
| | | |<a href='results/psrr_Sch_typical.html'>Sch_typ</a>| | -2.432 |  | |
| | | |<a href='results/psrr_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-17.146**</span> | -2.975 | <span style='color:red'>**20.751**</span> | |
|**PSRR at 100 kHz**|**psrr\_100k** || **Spec**  | **-10.000** | **-3.500** | **-1.000** | **dB** |
| | | |<a href='results/psrr_Sch_typical.html'>Sch_typ</a>| | -2.432 |  | |
| | | |<a href='results/psrr_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-17.146**</span> | -2.975 | <span style='color:red'>**20.718**</span> | |
|**PSRR at 1 MHz**|**psrr\_1meg** || **Spec**  | **-10.000** | **-3.500** | **-1.000** | **dB** |
| | | |<a href='results/psrr_Sch_typical.html'>Sch_typ</a>| | -2.439 |  | |
| | | |<a href='results/psrr_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-17.168**</span> | -2.982 | <span style='color:red'>**18.191**</span> | |
|**Worst PSRR (10 Hz to 10 MHz)**|**psrr\_worst** || **Spec**  | **-10.000** | **-2.000** | **1.000** | **dB** |
| | | |<a href='results/psrr_Sch_typical.html'>Sch_typ</a>| | -2.432 |  | |
| | | |<a href='results/psrr_Sch_etc.html'>Sch_etc</a>|-9.745 | -2.975 | <span style='color:red'>**20.751**</span> | |

