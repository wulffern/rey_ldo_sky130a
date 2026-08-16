[![GDS](../../actions/workflows/gds.yaml/badge.svg)](../../actions/workflows/gds.yaml)
[![DRC](../../actions/workflows/drc.yaml/badge.svg)](../../actions/workflows/drc.yaml)
[![LVS](../../actions/workflows/lvs.yaml/badge.svg)](../../actions/workflows/lvs.yaml)
[![DOCS](../../actions/workflows/docs.yaml/badge.svg)](../../actions/workflows/docs.yaml)

# Who
wulff

This block was laid out, verified and characterized in a two-hour
human+AI session — the story is in [AIDEMO.md](AIDEMO.md).

# Why

A 1.2 V low-dropout regulator for the REY family. The reference is a
resistive divider from VDD_1V8 (no bandgap), buffered by a two-stage
amplifier (nmos pair with resistor tail, pmos mirror) driving a PMOS
pass device. Load range 0 to 200 uA.

# How

- Schematic in xschem, devices from `rey_atr_sky130a`
  (REYATR_NCH/PCH 11C, REYATR_RES_36C2F0 ladders, REYATR_CAPX1 MiM).
- Layout is generated from one declarative sidecar,
  `design/REY_LDO_SKY130A/REY_LDO.py` (`cd work && make mag`):
  seven subcells and the assembled top, 73 x 68 um. DRC, KDRC,
  LVS and antenna clean, top and subcells.
- Simulations run with cicsim from `sim/REY_LDO/`
  (`make all`, or `make typical etc TB=<lstb|tran|psrr>`); results
  and spec checking in
  [sim/REY_LDO/README.md](sim/REY_LDO/README.md).

## Testbenches

| TB    | What it checks                                              |
| :---  | :---                                                        |
| lstb  | Loop stability (Tian probe between VDD_1V2 and LPI), at no load and 200 uA |
| tran  | Load step 0 -> 200 uA -> 0, line dip -100 mV, regulation, Iq |
| psrr  | Supply rejection 10 Hz to 100 MHz, both load ends            |

## Known issues (schematic, 2026-08-16)

- **The loop is marginally stable**: phase margin is ~0 at no load
  and 24 degrees at 200 uA (typical), and the transient testbench
  shows sustained ringing at light load. The compensation caps sit
  from VGSO to VDD_1V8 (a gate pole), not Miller across the pass
  device; the loop needs a compensation rework before this block is
  usable.
- **PSRR is -2 to -3.5 dB by construction**: the reference divider
  tracks the supply, so the output follows 2/3 of VDD_1V8. Real
  rejection needs a supply-independent reference.

# What

| What            |        Cell/Name |
| :----           |  :----:       |
| Schematic       | design/REY_LDO_SKY130A/REY_LDO.sch |
| Layout          | design/REY_LDO_SKY130A/REY_LDO.mag |
| Layout sidecar  | design/REY_LDO_SKY130A/REY_LDO.py |
| Simulations     | sim/REY_LDO/ |

# Signal interface

| Signal       | Direction | Domain  | Description                               |
| :---         | :---:     | :---:   | :---                                      |
| VDD_1V8      | Input     | VDD_1V8 | Main supply                               |
| VDD_1V2      | Output    | VDD_1V2 | Regulated 1.2 V output                    |
| LPI          | Input     | VDD_1V8 | Feedback input (tie to VDD_1V2)           |
| VSS          | Input     | Ground  |                                           |

# Key parameters

| Parameter           | Min     | Typ             | Max     | Unit  |
| :---                | :---:   | :---:           | :---:   | :---: |
| Technology          |         | Skywater 130 nm |         |       |
| AVDD                | 1.7     | 1.8             | 1.9     | V     |
| Output voltage      |         | 1.2             |         | V     |
| Load current        | 0       |                 | 200     | uA    |
| Quiescent current   | 16      | 24              | 33      | uA    |
| Temperature         | -40     | 27              | 125     | C     |
