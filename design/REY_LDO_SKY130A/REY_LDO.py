"""REY_LDO: a 1.2 V low-dropout regulator, laid out as a sidecar.

The circuit, read off ``work/xsch/REY_LDO.spice``:

  * ``xres2<2:0>`` and ``xres1<5:0>`` are ONE series ladder from
    VDD_1V8 down to VSS, nine REYATR_RES_36C2F0 units, tapped at
    REF_1V2 after six from the bottom -- so REF_1V2 = 6/9 of the
    supply, 1.2 V.  ``xfcap<3:0>`` filter that tap to VSS.
  * ``xdiff1``/``xdiff2`` are the nmos input pair: REF_1V2 against
    LPI, sharing the source node VS, which reaches VSS through the
    three-unit ladder ``xres_vs1<2:0>``.  A resistor tail, not a
    current source, so there is no bias branch anywhere in the cell.
  * ``xload1<1:0>`` is the diode leg of the pmos mirror (VBP) and
    ``xload<1:0>`` the mirrored leg (VGSO).  cicpy swaps the diode
    pair to the ``*D`` variant by itself -- VBP is on both D and G.
  * ``xout1`` is the pass device, gate on VGSO, drain VDD_1V2.
  * ``xgcap2<9:0>`` and ``xhcap1<9:0>`` are twenty compensation caps
    from VGSO to VDD_1V8 -- the dominant pole, and the bulk of the
    area.

So there are seven pieces and eight nets that cross between them,
which is what the class below says.  Nothing here is a coordinate:
the floorplan is `rows`, the crossing nets are channel tracks, and
the caps' grid is computed from the caps' own widths.
"""
import logging

from cicpy.core.path import (PITCH, SPACE, left_of_pins, pin,
                             right_of_pins, tab_lane, track)
from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("REY_LDO")


class _Caps(Stack):
    """A MiM cap bank laid out as a GRID, and wired as a COMB.

    ``Stack`` stacks in y and has no horizontal form, so twenty
    8 x 8 um caps in one column would be 160 um tall against a cell
    that is otherwise 60.  ``ncol`` columns are laid in `beforePlace`,
    off the instances' own boxes, so the arrangement survives another
    cap cell and another technology.

    The wiring matters more than the shape.  Left to the maze router
    the bank comes out as a snake: nineteen hops, each a full M1..M4
    via stack down and up again between neighbours (read
    ``REY_LDO.routes.py`` before this hook existed -- 34 DRC errors in
    c_comp, 2 in c_ref, all mcon and via2 spacing where two stacks
    landed in one 0.8 um gutter).  But a MiM needs no router at all:
    both plates SPAN their tile on their own layer, so a bar laid over
    the bank IS the connection, with no cut anywhere.  cicpy's layers
    sit one above magic's -- the REYATR cap's A plate (magic met3) is
    M4 and its B plate (met4) is M5 -- and every cap in one of these
    banks carries the same net pair, so there is no unrelated metal
    for a bar to land on and capm.11 has nothing to say.

    One bar per grid column plus one across them is the comb: it
    reaches every tile by two routes rather than nineteen in series,
    which is also the low-resistance way to tie a compensation cap.
    """

    ncol = 1
    fill = False

    #- (net, layer): the bottom plate first.  Read off the netlist --
    #- REYATR_CAPX1 is `.subckt A B` with `XC1 B A cap_mim_m3_1`, so
    #- the FIRST terminal of the instance line is the M4 plate.
    plates = ()

    def beforePlace(self, entry):
        insts = list(self.instances)
        if not insts:
            return
        x0, y0 = int(insts[0].x1), int(insts[0].y1)
        w = int(insts[0].width())
        h = int(insts[0].height())
        for i, inst in enumerate(insts):
            inst.moveTo(x0 + (i % self.ncol) * w,
                        y0 + (i // self.ncol) * h)
        self.updateBoundingRect()

    def beforeRoute(self, entry):
        for net, layer in self.plates:
            self._comb(net, layer)
        #- the whole bank is this hook's; the built-in router must not
        #- lay a second set of wires over the plates
        return True

    def _comb(self, net, layer, widthmult=3):
        """Vertical bars down each grid column, one horizontal across.

        Every bar is a plain rect on the plate's own layer -- no cut,
        because the plate is already that layer.  Positions come from
        the instance boxes, so the comb follows the grid.
        """
        from cicpy.core.rect import Rect
        from cicpy.core.rules import Rules

        insts = list(self.instances)
        if len(insts) < 2:
            self.layout.log.warning(
                f"{self.name}/{net}: {len(insts)} member(s), no comb")
            return
        w = int(Rules.getInstance().get(layer, "width") * widthmult)
        cols = {}
        for inst in insts:
            cols.setdefault(int(inst.x1) + int(inst.width()) // 2,
                            []).append(inst)
        y1 = min(int(i.y1) for i in insts)
        y2 = max(int(i.y2) for i in insts)
        x1 = min(int(i.x1) for i in insts)
        x2 = max(int(i.x2) for i in insts)

        bars = [Rect(layer, cx - w // 2, y1 + w, w, y2 - y1 - 2 * w)
                for cx in sorted(cols)]
        bars.append(Rect(layer, x1 + w, (y1 + y2) // 2 - w // 2,
                         x2 - x1 - 2 * w, w))
        for bar in bars:
            bar.setNet(net)
            self.layout.add(bar)
            self.layout.detachPlacementChild(bar, keepParent=self)
            self.add(bar)
            self.dummy_routes.append(bar)
        self.layout.log.info(f"{self.name}/{net}: {layer} comb, "
                             f"{len(cols)} column bar(s) + 1 crossbar")


class _ResCol(Stack):
    """A resistor column, MIRRORED IN Y so the chain can ascend.

    Inside REYATR_RES_36C2F0 the P terminal sits BELOW N (P at
    y 0.9..1.1 um of the 4 um row, N at 1.3..1.5, same x lane).  With
    the chain ascending in that orientation, each P(k)->N(k+1) link
    spans 4.4 um and OVERLAPS the next link in the one lane they
    share -- the first build put every other link on M2 and left four
    unanchored maze flyovers because of it.  Mirroring every unit MX
    puts P ABOVE N, and then the ascending chain's links are 3.6 um
    M1 verticals with a 0.4 um gap between consecutive ones: all of
    them in one lane, one layer, no cuts -- and the netlist order IS
    the placement order, so the ladder ends come out where the
    schematic says.
    """
    group = "res"
    fill = False

    def afterPlace(self, entry):
        #- the same setAngle + re-pin dance StackGroup.mirror() does
        #- for MY: setAngle leaves the instance in the mirrored frame,
        #- so pin it back where it was
        for inst in self.instances:
            x, y = inst.x1, inst.y1
            inst.setAngle("MX")
            inst.moveTo(int(x), int(y))
            inst.updateBoundingRect()
        self.updateBoundingRect()


class REY_LDO(SidecarCell):

    #- ------------------------------------------------------------
    #- the resistors
    #- ------------------------------------------------------------

    class r_div1(_ResCol):
        """The VSS half of the reference ladder: six units, VSS up
        to REF_1V2.

        The ladder used to be ONE nine-unit column, 40.8 um tall in
        a row of 17 um blocks -- 24 um of dead band across the cell.
        Split at REF_1V2, the two halves are 28.8 and 16.8 um, and
        REF_1V2 was already a crossing net (n_diff's gate, c_ref)
        so joining them costs nothing new.

        Mirrored and ascending (see _ResCol), VSS (xres1<0>.N) comes
        out at the BOTTOM -- one jog from the tap row below it, which
        the hook draws -- and REF_1V2 at the top, a short drop from
        the mid channel.

        REYATR_RES_36C2F0 carries its own slice of the bulk ring and
        stacks like a transistor, so this is an ordinary column --
        but it takes no dummies (`fill = False`): a fill resistor is
        not a supply device and there is none in the schematic.
        """
        match = r'^xres1<\d+>$'
        channel = "div1"
        order = [r'xres1<0>', r'xres1<1>', r'xres1<2>',
                 r'xres1<3>', r'xres1<4>', r'xres1<5>']
        #- the five series links, each an M1 vertical on the tab
        #- lane spanning its own two pins
        paths = [
            dict(net=n, layer="M1", steps=[("trunk", tab_lane())])
            for n in ("R3<0>", "R3<1>", "R3<2>", "R3<3>", "R3<4>")
        ]
        blocked = [
            ('VSS', "routed by this class's beforeRoute: one jog from "
                    'xres1<0>.N onto its own guard slice'),
        ]

        def beforeRoute(self, entry):
            #- the ladder end is a real terminal, not a bulk -- but
            #- the guard is one jog away: xres1<0> carries VSS twice,
            #- its N pin and its own guard slice's B, corner to
            #- corner.  The taps publish no pins at all, so the jog
            #- is drawn between the device's own two rects.
            self.layout.addConnectivityRoute(
                "M1", "^VSS$", "-|--", "", 1, "", r"^xres1<0>$")
            return None

    class r_div2(_ResCol):
        """The VDD half of the ladder: three units, REF_1V2 up to
        VDD_1V8 -- mirrored and ascending like r_div1, so VDD_1V8
        comes out at the TOP, facing the ring it belongs to.

        The pin still cannot leave on M1: the tap row above it straps
        VSS across the column's full width, so an M1 stretch from the
        pin to the ring crosses the guard (and before the mirror, the
        strap ran the whole column and merged REF_1V2, VDD_1V8, VSS
        and every ladder net into one 1109-rect component).  The hook
        lifts the pin IN PLACE: a short M2 riser over the tap row to
        a pad at the column's top edge, the port republished on the
        pad, and the parent's strap then arrives on M2.
        """
        match = r'^xres2<\d+>$'
        channel = "div2"
        order = [r'xres2<0>', r'xres2<1>', r'xres2<2>']
        #- the two series links
        paths = [
            dict(net=n, layer="M1", steps=[("trunk", tab_lane())])
            for n in ("R2<0>", "R2<1>")
        ]
        blocked = [
            ('VDD_1V8', "routed by this class's beforeRoute: an M2 "
                        'riser over the tap row to a pad at the top '
                        "edge, so the parent's strap never crosses "
                        'the guard on M1'),
        ]

        def beforeRoute(self, entry):
            from cicpy.core.rect import Rect
            layout = self.layout
            r = None
            for c in getattr(
                    layout.getInstanceFromInstanceName("xres2<2>"),
                    "children", []) or []:
                if getattr(c, "name", "") == "VDD_1V8" and hasattr(c, "get"):
                    r = c.get()
                    break
            if r is None:
                log.error("r_div2: no VDD_1V8 pin on xres2<2>")
                return None
            #- the pad hugs the pin's RIGHT end, narrow: REF_1V2's
            #- channel drop enters this column down the same lane,
            #- aligned left -- a full-width pad at the top edge sat
            #- straight in its way (measured, one REF_1V2|VDD_1V8
            #- component of 647 rects)
            pad = Rect("M2", int(r.x2) - 8000, int(self.y2) - 4000,
                       8000, 4000)
            pad.setNet("VDD_1V8")
            p = layout.path("VDD_1V8", "M1", start=[r], stop=[pad])
            p.start()
            p.up()
            p.movex(p.landing("x"))
            p.movey(p.landing("y"))
            p.end()
            layout.add(pad)
            self._vdd_pad = pad
            return None

        def afterPorts(self, entry):
            self.layout.updatePort("VDD_1V8", self._vdd_pad,
                                   routeLayer="M2")

    class r_vs(_ResCol):
        """The tail resistor: VSS up to VS in three units, mirrored
        and ascending like the ladder halves.  VSS (xres_vs1<0>.N)
        comes out at the bottom beside the tap row, VS at the top
        facing the nmos pair's channel drop.
        """
        match = r'^xres_vs1<\d+>$'
        channel = "vs"
        order = [r'xres_vs1<0>', r'xres_vs1<1>', r'xres_vs1<2>']
        #- the two series links, same form as r_div1's
        paths = [
            dict(net=n, layer="M1", steps=[("trunk", tab_lane())])
            for n in ("R1<0>", "R1<1>")
        ]
        blocked = [
            ('VSS', "routed by this class's beforeRoute: one jog from "
                    'xres_vs1<0>.N into the tap row directly below it'),
        ]

        def beforeRoute(self, entry):
            #- N pin to the device's own guard B, see r_div1
            self.layout.addConnectivityRoute(
                "M1", "^VSS$", "-|--", "", 1, "", r"^xres_vs1<0>$")
            return None

    #- ------------------------------------------------------------
    #- the amplifier
    #- ------------------------------------------------------------

    class n_diff(Stack):
        """REF_1V2 against LPI, sources tied on VS."""
        match = r'^xdiff[12]$'
        group = "nmos"
        channel = "diff"
        fill = False
        order = ['xdiff1', 'xdiff2']
        blocked = [
            ('VSS', 'the bulk, and the guard carries it'),
        ]
        #- the shared source node, one M1 rail on the pins' left edge
        paths = [
            dict(net="VS", layer="M1", steps=[("trunk", left_of_pins())]),
        ]

    class p_load(Stack):
        """The pmos mirror: the diode leg at the bottom.

        The two diodes go below the two mirrored devices so the VBP
        gate-tab rail spans upward over them -- the same reason
        OTAR's N stacks put their gate device at the bottom.
        """
        match = r'^xload1?<\d+>$'
        group = "pmos"
        channel = "load"
        fill = False
        order = ['xload1<0>', 'xload1<1>', 'xload<0>', 'xload<1>']
        blocked = [
            ('VDD_1V8', 'the sources and bulks; the guard carries it'),
        ]
        #- VBP is every gate in the column -- the two diodes' and the
        #- two mirrored devices' -- so ONE rail on the gate-tab lane
        #- ties the net, and the diodes' drains are already on it
        #- inside the *D cell.  M1, the pins' own layer, so there is
        #- no cut: the search's M2 trunktab with two cuts put a via
        #- column beside the diode tie's own contacts and that was all
        #- 24 DRC errors (mcon.2, li.3, met1.2, twice on each diode).
        #- VGSO is the two mirrored drains, adjacent rows, one M1 rail
        #- on their right edge.
        paths = [
            dict(net="VBP", layer="M1", steps=[("trunk", tab_lane())]),
            dict(net="VGSO", layer="M1",
                 steps=[("trunk", right_of_pins())]),
        ]

    class p_out(Stack):
        """The pass device, on its own so the drain can leave wide."""
        match = r'^xout1$'
        group = "pmos"
        channel = "out"
        fill = False
        order = ['xout1']
        blocked = [
            ('VDD_1V8', 'source and bulk; the guard carries it'),
        ]

    #- ------------------------------------------------------------
    #- the capacitors
    #- ------------------------------------------------------------

    class c_ref(_Caps):
        """Four caps decoupling REF_1V2 to VSS, two by two."""
        match = r'^xfcap<\d+>$'
        group = "caps"
        channel = "cref"
        ncol = 2
        order = [r'xfcap<\d+>']
        plates = (("REF_1V2", "M4"), ("VSS", "M5"))

    class c_comp(_Caps):
        """Twenty compensation caps, VGSO to VDD_1V8, five wide."""
        match = r'^x(gcap2|hcap1)<\d+>$'
        group = "caps"
        channel = "ccomp"
        ncol = 5
        order = [r'xhcap1<\d+>', r'xgcap2<\d+>']
        plates = (("VGSO", "M4"), ("VDD_1V8", "M5"))

    #- ------------------------------------------------------------
    #- the floorplan, bottom row first
    #- ------------------------------------------------------------
    #- TWO ROWS, and the split is not cosmetic: an nmos column abutted
    #- against a pmos one is "This layer can't abut or partially
    #- overlap between subcells" plus "Can't overlap those layers"
    #- (measured, one error at the n_diff/p_load seam when all three
    #- amplifier columns shared a row) -- the nwell edge lands inside
    #- the nmos column's own ring.  So the bottom row is everything
    #- p-substrate -- resistors, the nmos pair, the reference caps --
    #- and the top row is everything in an nwell, plus the MiM bank
    #- which sits in neither.
    #-
    #- Within the bottom row the order follows the SIGNAL: the tail
    #- resistor beside the pair whose source it sets, then the caps
    #- that filter the reference, then the ladder halves at the far
    #- right (r_div2 outermost, its M2 VDD pad nearest the ring's
    #- right side).  Splitting the ladder took the bottom row from
    #- 40.8 um tall to 28.8.
    rows = [
        [r_vs, n_diff, c_ref, r_div1, r_div2],
        [p_load, p_out, c_comp],
    ]

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    channel = 4

    #- The crossing nets, one ChannelRoute each in the mid channel.
    #- Drops are discovered (every subcell exposing the net, M2,
    #- centered, two cuts); entries below only override:
    #-   * the cap banks are met on M4, their plates' own layer;
    #-   * r_div2's REF_1V2 pin shares its tab lane with the R2<0>
    #-     link rail 0.4 um above it, so that drop's pad goes LEFT,
    #-     off the rail's x.
    #- VBP and VGSO both have a drain pin in n_diff, and the two
    #- drain bars share their x -- centered drops put both verticals
    #- in one lane (measured: two M2 verticals at x 206500, one
    #- component of 434 rects).  Their n_diff drops split left/right.
    routes = [
        {"net": "VS", "track": 0},
        #- REF's n_diff drop takes ONE cut: the two-cut pad at the
        #- bar slid away from REF's own vertical and stopped 0.04 um
        #- from VGSO's drop lane (met1.2, measured)
        {"net": "REF_1V2", "track": 1,
         "drops": [[r_div2, "M2", "left"],
                   {"inst": n_diff, "layer": "M2", "cuts": 1},
                   [c_ref, "M4", "center"]]},
        #- ...and in p_load the diode's D/G bar spans the column, so
        #- VBP's centered pin cut landed exactly in VGSO's drop lane
        #- (the drain rail's x): flush left clears it.
        {"net": "VBP", "track": 2,
         "drops": [[n_diff, "M2", "left"],
                   [p_load, "M2", "left"]]},
        {"net": "VGSO", "track": 3,
         "drops": [[n_diff, "M2", "right"],
                   [c_comp, "M4", "center"]]},
    ]
