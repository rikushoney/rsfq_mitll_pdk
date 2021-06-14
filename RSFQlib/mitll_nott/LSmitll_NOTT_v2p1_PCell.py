import sys
import os
import spira.all as spira
from spira.technologies.mit.process.database import RDD
from spira.technologies.mit import devices as dev
from spira.yevon.geometry.coord import Coord
# Shorthand for long layer names
M0 = spira.RDD.PLAYER.M0.METAL
I0 = spira.RDD.PLAYER.I0.VIA
M1 = spira.RDD.PLAYER.M1.METAL
I1 = spira.RDD.PLAYER.I1.VIA
M2 = spira.RDD.PLAYER.M2.METAL
I2 = spira.RDD.PLAYER.I2.VIA
M3 = spira.RDD.PLAYER.M3.METAL
I3 = spira.RDD.PLAYER.I3.VIA
M4 = spira.RDD.PLAYER.M4.GND
I4 = spira.RDD.PLAYER.I4.VIA
M5 = spira.RDD.PLAYER.M5.METAL
J5 = spira.RDD.PLAYER.J5.JUNCTION
R5 = spira.RDD.PLAYER.R5.METAL
I5 = spira.RDD.PLAYER.I5.VIA
C5J = spira.RDD.PLAYER.C5J.VIA
C5R = spira.RDD.PLAYER.C5R.VIA
M6 = spira.RDD.PLAYER.M6.METAL
I6 = spira.RDD.PLAYER.I6.VIA
M7 = spira.RDD.PLAYER.M7.METAL
IXPORT = spira.RDD.PLAYER.IXPORT
TEXT = spira.Layer(number=182)
# Shorthand for rotations and reflections
r90 = spira.Rotation(90)
r180 = spira.Rotation(180)
r270 = spira.Rotation(270)
m0 = spira.Reflection(True)
m45 = r270 + spira.Reflection(True)
m90 = r180 + spira.Reflection(True)
m135 = r90 + spira.Reflection(True)
m270 = m135

## Parameterization
# Trackpitch in microns
tp = 10

# Inductor widths
Scaling = (1+(tp-10)*0.25)
L1_width = 0.15*tp*Scaling
L2_width = 0.072*tp*Scaling
L3_width = 0.105*tp*Scaling
L4_width = 0.14125*tp*Scaling
L5_width = 0.088*tp*Scaling
L7_width = 0.090*tp*Scaling
L8_width = 0.095*tp*Scaling
L9_width = 0.15*tp*Scaling
L10_width = 0.22*tp*Scaling
L11_width = 0.115*tp*Scaling
L12_width = 0.245*tp*Scaling
L13_width = 0.148*tp*Scaling
L14_width = 0.1*tp*Scaling
L15_width = 0.26*tp*Scaling
L16_1_width = 0.105*tp*Scaling
L16_2_width = 0.2*tp*Scaling
L17_width = 0.275*tp*Scaling
L18_width = 0.3*tp*Scaling
L19_width = 0.11*tp*Scaling
L20_width = 0.245*tp*Scaling
L21_width = 0.135*tp*Scaling
L22_width = 0.125*tp*Scaling
LB1_width = 0.14*tp*Scaling
LB2_width = 0.2*tp*Scaling


# Common Shapes
lowerHalf = spira.Shape(points=[
    (0.0,0.0),(0.0,0.875),(0.04,0.875),(0.04,0.125),(0.125,0.125),
    (0.125,0.04),(0.875,0.04),(0.875,0.125),(1.0,0.125),(1.0,0.0)
    ])
lowerHalf = [x * tp for x in lowerHalf]
upperHalf = spira.Shape(points=[
    (0.0,1.0),(1.0,1.0),(1.0,0.125),(0.96,0.125),(0.96,0.875),
    (0.875,0.875),(0.875,0.96),(0.125,0.96),(0.125,0.875),(0.0,0.875)
    ])
upperHalf = [x * tp for x in upperHalf]
middleCross = spira.Shape(points=[
    (0.28,0.04),(0.28,0.28),(0.04,0.28),(0.04,0.72),(0.28,0.72),(0.28,0.96),
    (0.72,0.96),(0.72,0.72),(0.96,0.72),(0.96,0.28),(0.72,0.28),(0.72,0.04)
    ])
middleCross = [x * tp for x in middleCross]

class PCELL(spira.PCell):
    __name_prefix__ = "LSmitll_NOTT_v2p1"
    def create_elements(self, elems):
        M6M5Strips = spira.SRef(M6M5_strips())
        IXports = spira.SRef(IX_ports())
        M0M4M7tracks = spira.SRef(M0M4M7_tracks())
        jjfill = spira.SRef(junction_fill())
        M4M5M6M7conns = spira.SRef(M4M5M6M7_connections())
        vias = spira.SRef(M5M6_connections())
        bias = spira.SRef(biasing())
        jjs = spira.SRef(junctions())
        res = spira.SRef(resistors())
        tblocks = spira.SRef(trackblocks())
        elems += [M6M5Strips, IXports, M0M4M7tracks, jjfill, M4M5M6M7conns,
                  vias, bias, jjs, res, tblocks]
        # Bias ports
        PB1N = spira.Port(name='PB1N',midpoint=bias.reference.elements['bias1'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB1S = spira.Port(name='PB1S',midpoint=bias.reference.elements['bias1'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB2W = spira.Port(name='PB2W',midpoint=bias.reference.elements['bias2'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB2E = spira.Port(name='PB2E',midpoint=bias.reference.elements['bias2'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB3W = spira.Port(name='PB3W',midpoint=bias.reference.elements['bias3'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB3E = spira.Port(name='PB3E',midpoint=bias.reference.elements['bias3'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB4W = spira.Port(name='PB4W',midpoint=bias.reference.elements['bias4'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB4E = spira.Port(name='PB4E',midpoint=bias.reference.elements['bias4'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB5W = spira.Port(name='PB5W',midpoint=bias.reference.elements['bias5'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB5E = spira.Port(name='PB5E',midpoint=bias.reference.elements['bias5'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB6N = spira.Port(name='PB6N',midpoint=bias.reference.elements['bias6'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB6S = spira.Port(name='PB6S',midpoint=bias.reference.elements['bias6'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PB7N = spira.Port(name='PB7N',midpoint=bias.reference.elements['bias7'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PB7S = spira.Port(name='PB7S',midpoint=bias.reference.elements['bias7'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        # Bias Input Port
        PBias = spira.Port(name='PBias',midpoint=(9.5*tp,7.0*tp),process=spira.RDD.PROCESS.M6)
        # Resistor Ports
        PR1N = spira.Port(name='PR1N',midpoint=res.reference.elements['R1'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PR1S = spira.Port(name='PR1S',midpoint=res.reference.elements['R1'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        PR2N = spira.Port(name='PR2N',midpoint=res.reference.elements['R2'].ports['M6:PN'].midpoint,process=spira.RDD.PROCESS.M6)
        PR2S = spira.Port(name='PR2S',midpoint=res.reference.elements['R2'].ports['M6:PS'].midpoint,process=spira.RDD.PROCESS.M6)
        # Junction ports
        PJ1 = spira.Port(name="PJ1",midpoint=jjs.reference.elements['J1'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ2 = spira.Port(name="PJ2",midpoint=jjs.reference.elements['J2'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ3 = spira.Port(name="PJ3",midpoint=jjs.reference.elements['J3'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ4 = spira.Port(name="PJ4",midpoint=jjs.reference.elements['J4'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ5 = spira.Port(name="PJ5",midpoint=jjs.reference.elements['J5'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ6 = spira.Port(name="PJ6",midpoint=jjs.reference.elements['J6'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ7 = spira.Port(name="PJ7",midpoint=jjs.reference.elements['J7'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ8 = spira.Port(name="PJ8",midpoint=jjs.reference.elements['J8'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ9 = spira.Port(name="PJ9",midpoint=jjs.reference.elements['J9'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ10 = spira.Port(name="PJ10",midpoint=jjs.reference.elements['J10'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ11 = spira.Port(name="PJ11",midpoint=jjs.reference.elements['J11'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        PJ12 = spira.Port(name="PJ12",midpoint=jjs.reference.elements['J12'].ports['M6:PJ'].midpoint,process=spira.RDD.PROCESS.M6)
        # Pin Ports
        PA = spira.Port(name="PA",midpoint=IXports.reference.elements['A'].center-(0,0.25*tp),process=spira.RDD.PROCESS.M6)
        PCLK = spira.Port(name="PCLK",midpoint=IXports.reference.elements['CLK'].center+(0,0.25*tp),process=spira.RDD.PROCESS.M6)
        PQ = spira.Port(name="PQ",midpoint=(8.5*tp,1.55*tp),process=spira.RDD.PROCESS.M6)
        # VIAs
        PV1 = spira.Port(name="PV1",midpoint=vias.reference.elements['via1'].ports['M6:PV'].midpoint,process=spira.RDD.PROCESS.M6)
        PV2 = spira.Port(name="PV2",midpoint=vias.reference.elements['via2'].ports['M6:PV'].midpoint,process=spira.RDD.PROCESS.M6)
        PV3 = spira.Port(name="PV3",midpoint=vias.reference.elements['via3'].ports['M6:PV'].midpoint,process=spira.RDD.PROCESS.M6)
        # Nodes 
        PN5 = spira.Port(name="PN5",midpoint=(2.5*tp,2.5*tp),process=spira.RDD.PROCESS.M6)
        PN9 = spira.Port(name="PN9",midpoint=(4.51*tp,1.4725*tp),process=spira.RDD.PROCESS.M6)
        PN21 = spira.Port(name="PN21",midpoint=(2.5*tp,5.4975*tp),process=spira.RDD.PROCESS.M6)
        PN25 = spira.Port(name="PN25",midpoint=(4.455*tp,5.5*tp),process=spira.RDD.PROCESS.M6)
        PN29 = spira.Port(name="PN29",midpoint=(4.4425*tp,3.7775*tp),process=spira.RDD.PROCESS.M6)
        PN32 = spira.Port(name="PN32",midpoint=(4.5*tp,3.485*tp),process=spira.RDD.PROCESS.M6)
        PN39 = spira.Port(name="PN39",midpoint=(7.5*tp,4.5*tp),process=spira.RDD.PROCESS.M6)
        PGND = spira.Port(name="PGND",midpoint=(3.45*tp,2.9725*tp),process=spira.RDD.PROCESS.M6)

        # Inductors
        L1 = spira.RoutePath(port1=PA,port2=PJ1,path=[(PA.x,PJ1.y)],width=L1_width,layer=M6)
        L2 = spira.RoutePath(port1=PJ1,port2=PN5,path=[(PN5.x,PJ1.y)],width=L2_width,layer=M6)
        L3 = spira.RoutePath(port1=PN5,port2=PJ2,path=[(PN5.x,PJ2.y)],width=L3_width,layer=M6)
        L4 = spira.RoutePath(port1=PJ2,port2=PN9,path=[(PJ2.x,PN9.y)],width=L4_width,layer=M6)
        L5 = spira.RoutePath(port1=PN9,port2=PJ3,path=[(PN9.x,1.7475*tp),(4.605*tp,1.7475*tp),
                                                       (4.605*tp,2.0*tp),(4.395*tp,2.0*tp),
                                                       (4.395*tp,2.255*tp),(PJ3.x,2.255*tp)],width=L5_width,layer=M6)
        L7 = spira.RoutePath(port1=PJ3,port2=PR1S,path=[(4.105*tp,PJ3.y),(4.105*tp,2.385*tp),
                                                        (3.8475*tp,2.385*tp),(3.8475*tp,PR1S.y)],width=L7_width,layer=M6)
        L8_1 = spira.RoutePath(port1=PJ3,port2=PV1,path=[(PJ3.x,PV1.y)],width=L8_width,layer=M6)
        L8_2 = spira.RoutePath(port1=PV1,port2=PJ4,path=[(PV1.x,(PV1.y+PJ4.y)/2),(PJ4.x,(PV1.y+PJ4.y)/2)],width=L8_width,layer=M5)
        L8_3 = spira.RoutePath(port1=PJ4,port2=PN32,path=[(PJ4.x,(PJ4.y+PN32.y)/2),(PN32.x,(PJ4.y+PN32.y)/2)],width=L8_width,layer=M6)
        L9 = spira.RoutePath(port1=PCLK,port2=PJ6,path=[(PCLK.x,PJ6.y)],width=L9_width,layer=M6)
        L10 = spira.RoutePath(port1=PJ6,port2=PN21,path=[(PN21.x,PJ6.y)],width=L10_width,layer=M6)
        L11 = spira.RoutePath(port1=PN21,port2=PJ7,path=[(PN21.x,PJ7.y)],width=L11_width,layer=M6)
        L12 = spira.RoutePath(port1=PJ7,port2=PN25,path=[(PJ7.x,PN25.y)],width=L12_width,layer=M6)
        L13 = spira.RoutePath(port1=PN25,port2=PJ8,path=[(PJ8.x,PN25.y)],width=L13_width,layer=M6)
        L14 = spira.RoutePath(port1=PJ8,port2=PN29,path=[(5.24*tp,PJ8.y),(5.24*tp,4.9025*tp),
                                                         (4.405*tp,4.9025*tp),(4.405*tp,4.6275*tp),
                                                         (4.635*tp,4.6275*tp),(4.635*tp,4.345*tp),
                                                         (PN29.x,4.345*tp)],width=L14_width,layer=M6)
        L15 = spira.RoutePath(port1=PN29,port2=PN32,path=[(PN29.x,(PN29.y+PN32.y)/2),(PN32.x,(PN29.y+PN32.y)/2)],width=L15_width,layer=M6)
        L16_1 = spira.RoutePath(port1=PJ8,port2=PJ9,path=[(PJ8.x,PJ9.y)],width=L16_1_width,layer=M6)
        L16_2 = spira.RoutePath(port1=PJ9,port2=PV2,path=[(PJ9.x,PV2.y)],width=L16_2_width,layer=M5)
        L17_1 = spira.RoutePath(port1=PN32,port2=PJ5,path=[((PN32.x+PJ5.x)/2,PN32.y),((PN32.x+PJ5.x)/2,PJ5.y)],width=L17_width,layer=M6)
        L17_2 = spira.RoutePath(port1=PJ5,port2=PV2,path=[((PJ5.x+PV2.x)/2,PJ5.y),((PJ5.x+PV2.x)/2,PV2.y)],width=L17_width,layer=M5)
        L18 = spira.RoutePath(port1=PV2,port2=PJ10,path=[(PV2.x,PJ10.y)],width=L18_width,layer=M6)
        L19 = spira.RoutePath(port1=PJ10,port2=PN39,path=[(6.5*tp,PJ10.y),(6.5*tp,3.5*tp),(PN39.x,3.5*tp)],width=L19_width,layer=M6)
        L20 = spira.RoutePath(port1=PN39,port2=PJ11,path=[(PN39.x,PJ11.y)],width=L20_width,layer=M6)
        L21 = spira.RoutePath(port1=PJ11,port2=PJ12,path=[(PJ12.x,PJ11.y)],width=L21_width,layer=M6)
        L22_1 = spira.RoutePath(port1=PJ12,port2=PR2N,path=[(PR2N.x,PJ12.y)],width=L22_width,layer=M6)
        L22_2 = spira.RoutePath(port1=PR2S,port2=PQ,path=[(PR2S.x,PQ.y)],width=L22_width,layer=M6)

        elems += [L1, L2, L3, L4, L5, L7, L8_1, L8_2, L8_3, L9, L10, L11, L12, 
                  L13, L14, L15, L16_1, L16_2, L17_1, L17_2, L18, L19, L20, L21, L22_1, L22_2]

        # Bias inductors
        LB1_1 = spira.RoutePath(port1=PN5,port2=PB1N,path=[(PN5.x,PB1N.y)],width=LB1_width,layer=M6)
        LB1_2 = spira.RoutePath(port1=PB1S,port2=PV3,path=[(PB1S.x,0.5*tp),(PV3.x,0.5*tp)],width=LB2_width,layer=M6)
        LB2_1 = spira.RoutePath(port1=PN9,port2=PB2W,path=[(PN9.x,PB2W.y)],width=LB1_width,layer=M6)
        LB2_2 = spira.RoutePath(port1=PB2E,port2=PV3,path=[(PB2E.x,0.5*tp),(PV3.x,0.5*tp)],width=LB2_width,layer=M6)
        LB3_1 = spira.RoutePath(port1=PN21,port2=PB3E,path=[(PN21.x,PB3E.y)],width=LB1_width,layer=M6)
        LB3_2 = spira.RoutePath(port1=PB3W,port2=PV3,path=[(0.5*tp,PB3W.y),(0.5*tp,0.5*tp),
                                                           (PV3.x,0.5*tp)],width=LB2_width,layer=M6)
        LB4_1 = spira.RoutePath(port1=PN25,port2=PB4W,path=[(PN25.x,PB4W.y)],width=LB1_width,layer=M6)
        LB4_2 = spira.RoutePath(port1=PB4E,port2=PV3,path=[(PB4E.x,PV3.y)],width=LB2_width,layer=M6)
        LB5_1 = spira.RoutePath(port1=PN29,port2=PB5E,path=[(3.435*tp,PN29.y),(3.435*tp,PB5E.y)],width=LB1_width,layer=M6)
        LB5_2 = spira.RoutePath(port1=PB5W,port2=PV3,path=[(0.5*tp,PB5W.y),(0.5*tp,0.5*tp),
                                                           (PV3.x,0.5*tp)],width=LB2_width,layer=M6)
        LB6_1 = spira.RoutePath(port1=PN39,port2=PB6S,path=[(PN39.x,PB6S.y)],width=LB1_width,layer=M6)
        LB6_2 = spira.RoutePath(port1=PB6N,port2=PV3,path=[(PB6N.x,PV3.y)],width=LB2_width,layer=M6)
        LB7_1 = spira.RoutePath(port1=PJ12,port2=PB7N,path=[(PB7N.x,PJ12.y)],width=LB1_width,layer=M6)
        LB7_2 = spira.RoutePath(port1=PB7S,port2=PV3,path=[(PB7S.x,0.5*tp),(PV3.x,0.5*tp)],width=LB2_width,layer=M6)

        elems += [LB1_1, LB1_2, LB2_1, LB2_2, LB3_1, LB3_2, LB4_1, LB4_2,
                  LB5_1, LB5_2, LB6_1, LB6_2, LB7_1, LB7_2]

        LGND = spira.RoutePath(port1=PR1N,port2=PGND,path=[(PGND.x,PGND.y)],width=LB1_width,layer=M6)
        LBias = spira.RoutePath(port1=PV3,port2=PBias,path=[(PBias.x,PBias.y)],width=LB2_width,layer=M5)

        elems += [LGND, LBias]

        # Text Labels
        elems += spira.Label(text="P3 M6 M4",position=(8.5025*tp,2.23*tp),layer=TEXT)
        elems += spira.Label(text="PB7 M6 M4",position=(7.5025*tp,2.2725*tp),layer=TEXT)
        elems += spira.Label(text="J12 M6 M5",position=(8.495*tp,2.5*tp),layer=TEXT)
        elems += spira.Label(text="J11 M6 M5",position=(8.155*tp,4.485*tp),layer=TEXT)
        elems += spira.Label(text="PB6 M6 M4",position=(7.48*tp,5.0625*tp),layer=TEXT)
        elems += spira.Label(text="J10 M6 M5",position=(5.5*tp,3.115*tp),layer=TEXT)
        elems += spira.Label(text="J5 M6 M5",position=(4.995*tp,3.455*tp),layer=TEXT)
        elems += spira.Label(text="PB5 M6 M4",position=(3.14*tp,3.5725*tp),layer=TEXT)
        elems += spira.Label(text="J9 M6 M5",position=(5.5*tp,3.8875*tp),layer=TEXT)
        elems += spira.Label(text="J8 M6 M5",position=(5.565*tp,4.71*tp),layer=TEXT)
        elems += spira.Label(text="PB4 M6 M4",position=(4.455*tp,6.5025*tp),layer=TEXT)
        elems += spira.Label(text="J7 M6 M5",position=(3.5725*tp,5.5025*tp),layer=TEXT)
        elems += spira.Label(text="PB3 M6 M4",position=(1.92*tp,6.4975*tp),layer=TEXT)
        elems += spira.Label(text="J6 M6 M5",position=(1.5025*tp,4.5025*tp),layer=TEXT)
        elems += spira.Label(text="P2 M6 M4",position=(1.5125*tp,5.18*tp),layer=TEXT)
        elems += spira.Label(text="J4 M6 M5",position=(4.5125*tp,3.2075*tp),layer=TEXT)
        elems += spira.Label(text="PR1 M6 M4",position=(3.4525*tp,2.53*tp),layer=TEXT)
        elems += spira.Label(text="J3 M6 M5",position=(4.5*tp,2.5925*tp),layer=TEXT)
        elems += spira.Label(text="PB2 M6 M4",position=(4.985*tp,1.47*tp),layer=TEXT)
        elems += spira.Label(text="J2 M6 M5",position=(3.7775*tp,1.5675*tp),layer=TEXT)
        elems += spira.Label(text="PB1 M6 M4",position=(2.495*tp,1.5725*tp),layer=TEXT)
        elems += spira.Label(text="J1 M6 M5",position=(1.5025*tp,2.4975*tp),layer=TEXT)
        elems += spira.Label(text="q",position=(8.5*tp,1.5*tp),layer=TEXT)
        elems += spira.Label(text="clk",position=(1.5*tp,5.5*tp),layer=TEXT)
        elems += spira.Label(text="a",position=(1.5*tp,1.5*tp),layer=TEXT)
        elems += spira.Label(text="P1 M6 M4",position=(1.4975*tp,1.81*tp),layer=TEXT)
        elems += spira.Label(text="bias_in",position=(9.5*tp,7*tp),layer=TEXT)
        return elems

class M6M5_strips(spira.Cell):
    __name_prefix__ = "M6M5_strips"
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.025*tp,height=0.315*tp,center=(0.0125*tp,6.4925*tp))
        elems += spira.Box(layer=M6,width=0.025*tp,height=0.315*tp,center=(0.0125*tp,4.4925*tp))
        elems += spira.Box(layer=M6,width=0.315*tp,height=0.025*tp,center=(9.4925*tp,0.0125*tp))
        elems += spira.Box(layer=M5,width=0.025*tp,height=0.315*tp,center=(0.0125*tp,6.4925*tp))
        elems += spira.Box(layer=M5,width=0.025*tp,height=0.315*tp,center=(0.0125*tp,4.4925*tp))
        elems += spira.Box(layer=M5,width=0.315*tp,height=0.025*tp,center=(9.4925*tp,0.0125*tp))

        elems += spira.Box(layer=M5,width=0.25*tp,height=0.02*tp,center=(8.54*tp,5.02*tp))
        elems += spira.Box(layer=M5,width=0.055*tp,height=0.075*tp,center=(6.4025*tp,5.6625*tp))
        elems += spira.Box(layer=M5,width=0.03*tp,height=0.075*tp,center=(6.39*tp,5.3375*tp))
        elems += spira.Box(layer=M5,width=0.025*tp,height=0.325*tp,center=(6.4175*tp,5.4625*tp))
        elems += spira.Box(layer=M5,width=0.25*tp,height=0.02*tp,center=(6.5*tp,5.29*tp))
        elems += spira.Box(layer=M5,width=0.02*tp,height=0.4*tp,center=(6.84*tp,5.5*tp))
        elems += spira.Box(layer=M5,width=0.25*tp,height=0.02*tp,center=(6.5*tp,5.71*tp))
        elems += spira.Box(layer=M5,width=0.02*tp,height=0.4*tp,center=(8.21*tp,5.5*tp))
        elems += spira.Box(layer=M5,width=0.02*tp,height=0.25*tp,center=(8.63*tp,5.5*tp))
        elems += spira.Box(layer=M5,width=0.25*tp,height=0.02*tp,center=(8.495*tp,5.71*tp))
        elems += spira.Box(layer=M5,width=0.4*tp,height=0.02*tp,center=(6.5*tp,2.21*tp))
        elems += spira.Box(layer=M5,width=0.025*tp,height=0.4*tp,center=(3.5075*tp,4.5*tp))
        elems += spira.Box(layer=M5,width=0.25*tp,height=0.025*tp,center=(3.5*tp,4.2875*tp))
        elems += spira.Box(layer=M5,width=0.045*tp,height=0.095*tp,center=(8.6425*tp,5.3275*tp))
        elems += spira.Box(layer=M5,width=0.205*tp,height=0.02*tp,center=(8.5175*tp,5.29*tp))
        elems += spira.Box(layer=M5,width=0.4*tp,height=0.02*tp,center=(3.5*tp,6.49*tp))
        return elems

class IX_ports(spira.Cell):
    __name_prefix__ = "IX_ports"
    def create_elements(self, elems):
        elems += spira.Box(layer=IXPORT,width=0.2*tp,height=0*tp,center=(1.5*tp,5.18*tp),alias='CLK')
        elems += spira.Box(layer=IXPORT,width=0.2*tp,height=0*tp,center=(1.5*tp,1.81*tp),alias='A')
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(4.455*tp,6.5*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(1.915*tp,6.5*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(3.14*tp,3.57*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(3.45*tp,2.53*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(2.495*tp,1.567*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(4.985*tp,1.47*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(7.485*tp,5.065*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(7.5*tp,2.272*tp))
        elems += spira.Box(layer=IXPORT,width=0.052*tp,height=0.052*tp,center=(8.5*tp,2.231*tp))
       
        return elems

class M0M4M7_tracks(spira.Cell):
    __name_prefix__ = "M0M4M7_tracks"
    def create_elements(self, elems):
        shape=spira.Shape(points=[(3.72*tp,0.72*tp),(3.72*tp,1.28*tp),(3.96*tp,1.28*tp),(3.96*tp,0.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(3.72*tp,3.04*tp),(3.72*tp,3.28*tp),(4.28*tp,3.28*tp),(4.28*tp,3.04*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(3.72*tp,3.72*tp),(3.72*tp,3.96*tp),(4.28*tp,3.96*tp),(4.28*tp,3.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(5.72*tp,3.04*tp),(5.72*tp,3.28*tp),(6.28*tp,3.28*tp),(6.28*tp,3.04*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(5.72*tp,3.72*tp),(5.72*tp,3.96*tp),(6.28*tp,3.96*tp),(6.28*tp,3.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(4.845*tp,3.72*tp),(4.845*tp,4.28*tp),(5.1425*tp,4.28*tp),(5.1425*tp,3.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(4.72*tp,4.72*tp),(4.72*tp,4.96*tp),(6.28*tp,4.96*tp),(6.28*tp,4.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        shape=spira.Shape(points=[(8.04*tp,4.72*tp),(8.04*tp,5.28*tp),(8.28*tp,5.28*tp),(8.28*tp,4.72*tp)])
        elems += spira.Polygon(shape=shape,layer=M0)
        elems += spira.Polygon(shape=shape,layer=M4)
        elems += spira.Polygon(shape=shape,layer=M7)
        
        return elems

class junction_fill(spira.Cell):
    __name_prefix__ = "junction_fill"
    def create_elements(self, elems):
        sys.stdout.write("Adding junction fill.\n")
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2.5*tp,3.87*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6.5*tp,5.155*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8.54*tp,4.885*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8.765*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6.5*tp,5.845*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6.55*tp,4.805*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(4*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(4*tp,5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(4*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8.495*tp,5.845*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(7*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(9*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3.5*tp,4.15*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(5*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(5*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,4*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1.5*tp,3.875*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(6.28*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,1*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(1*tp,3*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(5*tp,6*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(5*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(4*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(8.54*tp,5.155*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(2*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_1p5x1p5um(),midpoint=(3*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(6.5*tp,2*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(3.72*tp,4.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(3.5*tp,6.7*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(2.5*tp,3.2*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(6.5*tp,4.26*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(7.05*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(3.295*tp,4.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(8.42*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(8*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(3.5*tp,6.28*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(6.63*tp,5.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(1.5*tp,3.2*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(6.5*tp,2.42*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(7*tp,1.5*tp))
        elems += spira.SRef(ls_FakeJJ_3umx3um(),midpoint=(7*tp,2.5*tp))
        return elems

class M4M5M6M7_connections(spira.Cell):
    __name_prefix__ = "M4M5M6M7_connections"
    def create_elements(self, elems):
        sys.stdout.write('Adding M4M5M6M7 connections.\n')
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.325*tp,5.7525*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.33*tp,3.1*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.335*tp,6.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,6.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.335*tp,0.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.3325*tp,5.115*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,5.845*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.3175*tp,4.1225*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.3375*tp,4.11*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(6.3525*tp,2.815*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.8025*tp,3.4125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,1.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,1.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.3425*tp,1.8325*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.3525*tp,2.7425*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.78*tp,4.3275*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.335*tp,0.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.32*tp,3.235*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.3325*tp,1.075*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.85*tp,3.4175*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.335*tp,0.025*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.3325*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(6.3325*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,0.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.335*tp,2.7625*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.7875*tp,4.535*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.3525*tp,2.7425*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.3425*tp,5.7525*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(6.335*tp,3.755*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,6.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(6.335*tp,6.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(6.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.335*tp,6.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.335*tp,2.015*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,0.735*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.335*tp,0.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.3425*tp,2.125*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.335*tp,1.015*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.32*tp,2.9425*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.335*tp,1.015*tp))
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.875*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.49*tp,0.9*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.985*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.265*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.265*tp,2.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.165*tp,0.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.255*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(3.085*tp,2.3475*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.155*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.265*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.265*tp,4.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,4.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.235*tp,4.33*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.925*tp,4.33*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.9525*tp,5.345*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.985*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(5.9025*tp,2.3475*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,2.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.27*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.265*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,0.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.875*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.25*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(7.9075*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.265*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.9025*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.265*tp,3.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.985*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.9425*tp,6.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.165*tp,6.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.15*tp,6.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.875*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(1.155*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.265*tp,5.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(0.265*tp,4.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(4.2025*tp,4.32*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(2.875*tp,4.345*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(8.155*tp,1.335*tp),transformation=r90)
        elems += spira.SRef(ls_conn_M4M5M6M7(),midpoint=(9.875*tp,6.335*tp),transformation=r90)
        return elems

class M5M6_connections(spira.Cell):
    __name_prefix__ = "M5M6_connections"
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6(),midpoint=(4.415*tp,2.815*tp),alias='via1')
        elems += spira.SRef(ls_conn_M5M6(),midpoint=(5.415*tp,3.3975*tp),alias='via2')
        elems += spira.SRef(ls_conn_M5M6(),midpoint=(9.415*tp,6.415*tp),alias='via3')
        return elems

class biasing(spira.Cell):
    __name_prefix__ = "biasing"
    def create_elements(self, elems):
        elems += spira.SRef(ls_ib_095(),midpoint=(4.4*tp,6.5*tp),transformation=r270,alias='bias4')
        elems += spira.SRef(ls_ib_097(),midpoint=(3.195*tp,3.57*tp),transformation=r90,alias='bias5')
        elems += spira.SRef(ls_ib_102(),midpoint=(4.93*tp,1.47*tp),transformation=r270,alias='bias2')
        elems += spira.SRef(ls_ib_108(),midpoint=(7.485*tp,5.01*tp),alias='bias6')
        elems += spira.SRef(ls_ib_146(),midpoint=(2.495*tp,0.445*tp),alias='bias1')
        elems += spira.SRef(ls_ib_181(),midpoint=(1.97*tp,6.5*tp),transformation=r90,alias='bias3')
        elems += spira.SRef(ls_ib_187(),midpoint=(7.5*tp,1.375*tp),alias='bias7')
        return elems

class junctions(spira.Cell):
    __name_prefix__ = "junctions"
    def create_elements(self, elems):
        elems += spira.SRef(ls_jj_077_s(),midpoint=(4.995*tp,3.455*tp),alias='J5')
        elems += spira.SRef(ls_jj_104_sg(),midpoint=(5.5*tp,3.115*tp),transformation=r180,alias='J10')
        elems += spira.SRef(ls_jj_122_s(),midpoint=(4.515*tp,3.205*tp),transformation=r90,alias='J4')
        elems += spira.SRef(ls_jj_122_sg(),midpoint=(5.565*tp,4.705*tp),transformation=r270,alias='J8')
        elems += spira.SRef(ls_jj_162_sg(),midpoint=(1.5*tp,4.5*tp),transformation=r90,alias='J6')
        elems += spira.SRef(ls_jj_162_sg(),midpoint=(1.5*tp,2.5*tp),transformation=r90,alias='J1')
        elems += spira.SRef(ls_jj_135_s(),midpoint=(5.5*tp,3.89*tp),transformation=r270,alias='J9')
        elems += spira.SRef(ls_jj_141_sg(),midpoint=(8.155*tp,4.49*tp),alias='J11')
        elems += spira.SRef(ls_jj_142_sg(),midpoint=(3.775*tp,1.565*tp),transformation=r180,alias='J2')
        elems += spira.SRef(ls_jj_172_sg(),midpoint=(4.5*tp,2.585*tp),transformation=r270,alias='J3')
        elems += spira.SRef(ls_jj_221_sg(),midpoint=(3.57*tp,5.5*tp),transformation=r180,alias='J7')
        elems += spira.SRef(ls_jj_285_sg(),midpoint=(8.5*tp,2.5*tp),transformation=r270,alias='J12')
        return elems

class resistors(spira.Cell):
    __name_prefix__ = "resistors"
    def create_elements(self, elems):
        elems += spira.SRef(ls_res_1p36(),midpoint=(8.5*tp,1.98*tp),alias='R2')
        elems += spira.SRef(ls_res_3p54(),midpoint=(3.45*tp,2.475*tp),alias='R1')
        return elems

class trackblocks(spira.Cell):
    __name_prefix__ = "trackblocks"
    def create_elements(self, elems):
        T = spira.Rotation(180)
        sys.stdout.write("Adding trackblocks.\n")
        for y in range(0, 7):
            for x in range(0, 10):
                if (x == 1 and y in [1,5]) or (x == 8 and y == 1):
                    elems += spira.SRef(ls_tr_PTLconnection(),midpoint=(0+x*tp,0+y*tp))
                else:
                    elems += spira.SRef(ls_tr_u_M4(),midpoint=(0+x*tp,0+y*tp))
                    elems += spira.SRef(ls_tr_M7(),midpoint=(0+x*tp,0+y*tp))
        return elems

# 1.5um junction fill cell
class ls_FakeJJ_1p5x1p5um(spira.Device):
    __name_prefix__ = 'ls_FakeJJ_1p5umx1p5um'
    def create_elements(self, elems):
        elems += spira.Box(layer=M4,width=0.25*tp,height=0.25*tp)
        elems += spira.Box(layer=M5,width=0.25*tp,height=0.25*tp)
        elems += spira.Box(layer=J5,width=0.15*tp,height=0.15*tp)
        elems += spira.Box(layer=C5J,width=0.13*tp,height=0.13*tp)
        elems += spira.Box(layer=M6,width=0.2*tp,height=0.2*tp)

        return elems

# 3um junction fill cell
class ls_FakeJJ_3umx3um(spira.Cell):
    __name_prefix__ = 'ls_FakeJJ_3umx3um'
    def create_elements(self, elems):
        elems += spira.Box(layer=M4,width=0.4*tp,height=0.4*tp)
        elems += spira.Box(layer=M5,width=0.4*tp,height=0.4*tp)
        elems += spira.Box(layer=J5,width=0.3*tp,height=0.3*tp)
        elems += spira.Box(layer=C5J,width=0.28*tp,height=0.28*tp)
        elems += spira.Box(layer=M6,width=0.35*tp,height=0.35*tp)

        return elems

# M4 to M7 connector cell
class ls_conn_M4M5M6M7(spira.Cell):
    __name_prefix__ = 'ls_conn_M4M5M6M7'
    def create_elements(self, elems):
        elems += spira.Box(layer=M4,width=0.14*tp,height=0.14*tp,center=(0.07*tp,0.07*tp))
        elems += spira.Box(layer=I4,width=0.08*tp,height=0.08*tp,center=(0.07*tp,0.07*tp))
        shape = spira.Shape(points=[
            [0.16,-0.015],[0.16,0.0],[0.0,0.0],[0.0,0.14],
            [0.16,0.14],[0.16,0.155],[0.33,0.155],[0.33,-0.015]
            ])
        shape = [x * tp for x in shape]
        elems += spira.Polygon(shape=shape, layer=M5)
        elems += spira.Box(layer=I5,width=0.07*tp,height=0.07*tp,center=(0.245*tp,0.07*tp))
        elems += spira.Box(layer=M6,width=0.315*tp,height=0.14*tp,center=(0.1575*tp,0.07*tp))
        elems += spira.Box(layer=I6,width=0.07*tp,height=0.07*tp,center=(0.07*tp,0.07*tp))
        elems += spira.Box(layer=M7,width=0.14*tp,height=0.14*tp,center=(0.07*tp,0.07*tp))

        return elems

# M5 to M6 connector cell
class ls_conn_M5M6(spira.Cell):
    __name_prefix__ = 'ls_conn_M5M6'
    def create_elements(self, elems):
        elems += spira.Box(layer=M5,width=0.17*tp,height=0.17*tp,center=(0.085*tp,0.085*tp))
        elems += spira.Box(layer=I5,width=0.07*tp,height=0.07*tp,center=(0.085*tp,0.085*tp))
        elems += spira.Box(layer=M6,width=0.14*tp,height=0.14*tp,center=(0.085*tp,0.085*tp))
        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PV",midpoint=(0.085*tp,0.085*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 95uA cell
class ls_ib_095(spira.Cell):
    __name_prefix__ = 'ls_ib_095'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0*tp,1.66875*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0*tp,0.05375*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0*tp,1.668*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0*tp,0.055*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=1.7225*tp,center=(0.0*tp,0.86125*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0*tp,1.66875*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0*tp,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 97uA cell
class ls_ib_097(spira.Cell):
    __name_prefix__ = 'ls_ib_097'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,1.64*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=1.6925*tp,center=(0.0,0.84625*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,1.64*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,1.64*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 102uA cell
class ls_ib_102(spira.Cell):
    __name_prefix__ = 'ls_ib_102'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,1.57*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=1.6225*tp,center=(0.0,0.81125*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,1.57*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,1.57*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 108uA cell
class ls_ib_108(spira.Cell):
    __name_prefix__ = 'ls_ib_108'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,1.4775*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=1.53*tp,center=(0.0,0.765*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,1.478*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,1.4775*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 146uA cell
class ls_ib_146(spira.Cell):
    __name_prefix__ = 'ls_ib_146'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,1.12125*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=1.175*tp,center=(0.0,0.5875*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,1.122*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,1.12125*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 181uA cell
class ls_ib_181(spira.Cell):
    __name_prefix__ = 'ls_ib_181'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.92375*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=0.9775*tp,center=(0.0,0.48875*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.923*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,0.92375*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# Bias 187uA cell
class ls_ib_187(spira.Cell):
    __name_prefix__ = 'ls_ib_187'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.89625*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=0.95*tp,center=(0.0,0.475*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.897*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0.0,0.89625*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0.0,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports


# JJ 77uA shunted cell
class ls_jj_077_s(spira.Cell):
    __name_prefix__ = 'ls_jj_077_s'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=1.8,height=3.05,center=(0.0,0.625))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,7.5625))
        elems += spira.Box(layer=M5,width=2.1,height=3.3,center=(0.0,0.6))
        elems += spira.Box(layer=M5,width=1.75,height=6.85,center=(0.0,5.675))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,8.225))
        elems += spira.Box(layer=R5,width=1.15,height=6.375,center=(0.0,4.1625))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.51))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,6.81))
        elems += spira.Circle(layer=C5J,box_size=(0.74, 0.74))
        elems += spira.Circle(layer=J5,box_size=(1.04, 1.04))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports


# JJ 104uA shunted and grounded cell
class ls_jj_104_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_104_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,6.725))
        elems += spira.Box(layer=M6,width=1.95,height=3.2,center=(0.0,0.625))
        elems += spira.Box(layer=M6,width=1.45,height=2.75,center=(0.0,6.4))
        elems += spira.Box(layer=M5,width=2.25,height=3.45,center=(0.0,0.6))
        elems += spira.Box(layer=M5,width=1.75,height=5.6,center=(0.0,5.125))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.6))
        elems += spira.Box(layer=R5,width=1.15,height=5.125,center=(0.0,3.6125))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.58))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,5.65))
        elems += spira.Circle(layer=C5J,box_size=(0.9, 0.9))
        elems += spira.Circle(layer=J5,box_size=(1.2, 1.2))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 122uA shunted cell
class ls_jj_122_s(spira.Cell):
    __name_prefix__ = 'ls_jj_122_s'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=2.05,height=3.3,center=(0.0,0.625))
        elems += spira.Box(layer=M6,width=1.45,height=2.75,center=(0.0,5.925))
        elems += spira.Box(layer=M5,width=2.35,height=3.55,center=(0.0,0.6))
        elems += spira.Box(layer=M5,width=1.75,height=5.075,center=(0.0,4.9125))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,6.575))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.65))
        elems += spira.Box(layer=R5,width=1.15,height=4.6,center=(0.0,3.4))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.63))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,5.17))
        elems += spira.Circle(layer=C5J,box_size=(1.0, 1.0))
        elems += spira.Circle(layer=J5,box_size=(1.29, 1.29))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 122uA shunted and grounded cell
class ls_jj_122_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_122_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,6.25))
        elems += spira.Box(layer=M6,width=2.05,height=3.3,center=(0.0,0.625))
        elems += spira.Box(layer=M6,width=1.45,height=2.75,center=(0.0,5.925))
        elems += spira.Box(layer=M5,width=2.35,height=3.55,center=(0.0,0.6))
        elems += spira.Box(layer=M5,width=1.75,height=5.075,center=(0.0,4.9125))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.65))
        elems += spira.Box(layer=R5,width=1.15,height=4.6,center=(0.0,3.4))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.63))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,5.17))
        elems += spira.Circle(layer=C5J,box_size=(1.0, 1.0))
        elems += spira.Circle(layer=J5,box_size=(1.29, 1.29))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 162uA shunted cell and grounded
class ls_jj_162_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_162_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5.55))
        elems += spira.Box(layer=M5,width=1.75,height=4.35,center=(0.0,4.6))
        elems += spira.Box(layer=M5,width=2.55,height=3.7,center=(0.0,0.575))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,5.9))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.75))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,5.2375))
        elems += spira.Box(layer=M6,width=2.25,height=3.45,center=(0.0,0.6))
        elems += spira.Box(layer=R5,width=1.15,height=3.85,center=(0.0,3.1))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.49))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.7))
        elems += spira.Circle(layer=J5,box_size=(1.48, 1.48))
        elems += spira.Circle(layer=C5J,box_size=(1.18, 1.18))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 135uA shunted cell
class ls_jj_135_s(spira.Cell):
    __name_prefix__ = 'ls_jj_135_s'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=2.1,height=3.325,center=(0.0,0.6125))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,5.6375))
        elems += spira.Box(layer=M5,width=2.4,height=3.575,center=(0.0,0.5875))
        elems += spira.Box(layer=M5,width=1.75,height=4.8,center=(0.0,4.775))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,6.3))
        elems += spira.Box(layer=R5,width=1.15,height=4.325,center=(0.0,3.2625))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.64))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.89))
        elems += spira.Circle(layer=C5J,box_size=(1.06, 1.06))
        elems += spira.Circle(layer=J5,box_size=(1.35, 1.35))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 141uA shunted and grounded cell
class ls_jj_141_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_141_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5.85))
        elems += spira.Box(layer=M6,width=2.15,height=3.35,center=(0.0,0.6))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,5.5375))
        elems += spira.Box(layer=M5,width=2.45,height=3.6,center=(0.0,0.575))
        elems += spira.Box(layer=M5,width=1.75,height=4.7,center=(0.0,4.725))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,6.2))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.7))
        elems += spira.Box(layer=R5,width=1.15,height=4.2,center=(0.0,3.225))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.65))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.79))
        elems += spira.Circle(layer=C5J,box_size=(1.08, 1.08))
        elems += spira.Circle(layer=J5,box_size=(1.38, 1.38))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 142uA shunted and grounded cell
class ls_jj_142_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_142_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5.875))
        elems += spira.Box(layer=M6,width=2.15,height=3.4,center=(0.0,0.625))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,5.5375))
        elems += spira.Box(layer=M5,width=2.45,height=3.65,center=(0.0,0.6))
        elems += spira.Box(layer=M5,width=1.75,height=4.65,center=(0.0,4.75))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.7))
        elems += spira.Box(layer=R5,width=1.15,height=4.175,center=(0.0,3.2375))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.68))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.8))
        elems += spira.Circle(layer=C5J,box_size=(1.08, 1.08))
        elems += spira.Circle(layer=J5,box_size=(1.39, 1.39))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 172uA shunted and grounded cell
class ls_jj_172_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_172_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5.45))
        elems += spira.Box(layer=M6,width=2.25,height=3.475,center=(0.0,0.6125))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,5.1375))
        elems += spira.Box(layer=M5,width=2.55,height=3.725,center=(0.0,0.5875))
        elems += spira.Box(layer=M5,width=1.75,height=4.225,center=(0.0,4.5625))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,5.8))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.75))
        elems += spira.Box(layer=R5,width=1.15,height=3.75,center=(0.0,3.05))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.72))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.38))
        elems += spira.Circle(layer=C5J,box_size=(1.22, 1.22))
        elems += spira.Circle(layer=J5,box_size=(1.52, 1.52))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports

# JJ 221uA shunted and grounded cell
class ls_jj_221_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_221_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5.075))
        elems += spira.Box(layer=M6,width=2.45,height=3.675,center=(0.0,0.6125))
        elems += spira.Box(layer=M6,width=1.45,height=2.775,center=(0.0,4.7625))
        elems += spira.Box(layer=M5,width=2.75,height=3.925,center=(0.0,0.5875))
        elems += spira.Box(layer=M5,width=1.75,height=3.75,center=(0.0,4.425))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.0,5.425))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.85))
        elems += spira.Box(layer=R5,width=1.15,height=3.275,center=(0.0,2.9125))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,1.82))
        elems += spira.Box(layer=C5R,width=0.52,height=0.52,center=(0.0,4.01))
        elems += spira.Circle(layer=C5J,box_size=(1.42, 1.42))
        elems += spira.Circle(layer=J5,box_size=(1.72, 1.72))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports


# JJ 285uA shunted and grounded cell
class ls_jj_285_sg(spira.Cell):
    __name_prefix__ = 'ls_jj_285_sg'
    def create_elements(self, elems):
        elems += spira.SRef(ls_conn_M5M6M7(), (-0.35,5))
        elems += spira.Box(layer=M6,width=2.7,height=3.925,center=(0.0,0.6125))
        elems += spira.Box(layer=M6,width=1.45,height=2.75,center=(0.0,4.675))
        elems += spira.Box(layer=M5,width=3.0,height=4.175,center=(0.0,0.5875))
        elems += spira.Box(layer=M5,width=1.75,height=3.525,center=(0.0,4.4375))
        elems += spira.Box(layer=I4,width=1,height=1,center=(0.0,2.975))
        elems += spira.Box(layer=R5,width=1.25,height=3.05,center=(0.0,2.925))
        elems += spira.Box(layer=C5R,width=0.68,height=0.52,center=(0.0,1.93))
        elems += spira.Box(layer=C5R,width=0.68,height=0.52,center=(0.0,3.92))
        elems += spira.Circle(layer=C5J,box_size=(1.64, 1.64))
        elems += spira.Circle(layer=J5,box_size=(1.94, 1.94))

        return elems
    def create_ports(self,ports):
        ports += spira.Port(name="PJ",midpoint=(0,0),process=spira.RDD.PROCESS.M6)

        return ports



# M5 to M7 connector cell
class ls_conn_M5M6M7(spira.Cell):
    __name_prefix__ = 'ls_conn_M5M6M7'
    def create_elements(self, elems):
        elems += spira.Box(layer=M5,width=1.7,height=1.7,center=(0.35,0.35))
        elems += spira.Box(layer=I5,width=0.7,height=0.7,center=(0.35,0.35))
        elems += spira.Box(layer=M6,width=2.0,height=2.0,center=(0.35,0.35))
        elems += spira.Box(layer=I6,width=1.3,height=1.3,center=(0.35,0.35))
        elems += spira.Box(layer=M7,width=2.0,height=2.0,center=(0.35,0.35))

        return elems

# 1.36 Ohm resistor
class ls_res_1p36(spira.Cell):
    __name_prefix__ = 'ls_res_1p36'
    def create_elements(self, elems):
        elems += spira.Box(layer=R5,width=0.4*tp,height=0.31*tp,center=(0.0,0.155*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.256*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.25625*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0*tp,0.25625*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0*tp,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# 3.54 Ohm resistor
class ls_res_3p54(spira.Cell):
    __name_prefix__ = 'ls_res_3p54'
    def create_elements(self, elems):
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.05375*tp))
        elems += spira.Box(layer=M6,width=0.125*tp,height=0.1275*tp,center=(0.0,0.30125*tp))
        elems += spira.Box(layer=R5,width=0.115*tp,height=0.355*tp,center=(0.0,0.1775*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.302*tp))
        elems += spira.Box(layer=C5R,width=0.052*tp,height=0.052*tp,center=(0.0,0.055*tp))

        return elems
    def create_ports(self, ports):
        ports += spira.Port(name="PN",midpoint=(0*tp,0.30125*tp),process=spira.RDD.PROCESS.M6)
        ports += spira.Port(name="PS",midpoint=(0*tp,0.05375*tp),process=spira.RDD.PROCESS.M6)

        return ports

# M7 Track block fill cell
class ls_tr_M7(spira.Cell):
    __name_prefix__ = 'ls_tr_M7'
    def create_elements(self, elems):
        elems += spira.Polygon(shape=lowerHalf, layer=M7)
        elems += spira.Polygon(shape=upperHalf, layer=M7)
        elems += spira.Polygon(shape=middleCross, layer=M7)

        return elems

# PTL connection cell
class ls_tr_PTLconnection(spira.Cell):
    __name_prefix__ = 'ls_tr_PTLconnection'
    def create_elements(self, elems):
        # Common shape
        top = spira.Shape(points=[
            (0.0,0.875),(0.0,1.0),(1.0,1.0),(1.0,0.125),(0.96,0.125),(0.96,0.28),
            (0.77,0.28),(0.77,0.72),(0.96,0.72),(0.96,0.875),(0.875,0.875),(0.875,0.96),
            (0.72,0.96),(0.72,0.77),(0.28,0.77),(0.28,0.96),(0.125,0.96),(0.125,0.875)
            ])
        top = [x * tp for x in top]
        bot = spira.Shape(points=[
            (0.0,0.0),(0.0,0.875),(0.04,0.875),(0.04,0.72),(0.23,0.72),(0.23,0.28),
            (0.04,0.28),(0.04,0.125),(0.125,0.125),(0.125,0.04),(0.28,0.04),(0.28,0.23),
            (0.72,0.23),(0.72,0.04),(0.875,0.04),(0.875,0.125),(1.0,0.125),(1.0,0.0)
            ])
        bot = [x * tp for x in bot]

        elems += spira.Polygon(shape=lowerHalf, layer=M0)
        elems += spira.Polygon(shape=upperHalf, layer=M0)
        elems += spira.Polygon(shape=middleCross, layer=M0)
        elems += spira.Box(layer=I0,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.935*tp))
        elems += spira.Box(layer=I0,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.065*tp))
        elems += spira.Box(layer=M1,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.9375*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.9375*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.0625*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.0625*tp))
        elems += spira.Box(layer=I1,width=0.12*tp,height=0.12*tp,center=(0.61*tp,0.61*tp))
        elems += spira.Box(layer=I1,width=0.12*tp,height=0.12*tp,center=(0.39*tp,0.39*tp))
        elems += spira.Box(layer=I1,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.935*tp))
        elems += spira.Box(layer=I1,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.065*tp))
        elems += spira.Polygon(shape=top, layer=M2)
        elems += spira.Polygon(shape=bot, layer=M2)
        elems += spira.Box(layer=M2,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.Box(layer=I2,width=0.12*tp,height=0.12*tp,center=(0.39*tp,0.61*tp))
        elems += spira.Box(layer=I2,width=0.12*tp,height=0.12*tp,center=(0.61*tp,0.39*tp))
        elems += spira.Box(layer=I2,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.935*tp))
        elems += spira.Box(layer=I2,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.065*tp))
        elems += spira.Box(layer=M3,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.9375*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.9375*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.0625*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.0625*tp))
        elems += spira.Box(layer=I3,width=0.12*tp,height=0.12*tp,center=(0.61*tp,0.61*tp))
        elems += spira.Box(layer=I3,width=0.12*tp,height=0.12*tp,center=(0.39*tp,0.39*tp))
        elems += spira.Box(layer=I3,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.935*tp))
        elems += spira.Box(layer=I3,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.065*tp))
        elems += spira.Polygon(shape=top, layer=M4)
        elems += spira.Polygon(shape=bot, layer=M4)
        elems += spira.Box(layer=M4,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.Box(layer=I4,width=0.12*tp,height=0.12*tp,center=(0.39*tp,0.61*tp))
        elems += spira.Box(layer=I4,width=0.12*tp,height=0.12*tp,center=(0.61*tp,0.39*tp))
        elems += spira.Box(layer=M5,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.Box(layer=I5,width=0.12*tp,height=0.12*tp,center=(0.61*tp,0.61*tp))
        elems += spira.Box(layer=I5,width=0.12*tp,height=0.12*tp,center=(0.39*tp,0.39*tp))
        elems += spira.Box(layer=M6,width=0.44*tp,height=0.44*tp,center=(0.5*tp,0.5*tp))
        elems += spira.SRef(ls_tr_M7())

        return elems

# Track block cell
class ls_tr_u_M4(spira.Cell):
    __name_prefix__ = 'ls_tr_u_M4'
    def create_elements(self, elems):
        elems += spira.Polygon(shape=lowerHalf, layer=M0)
        elems += spira.Polygon(shape=upperHalf, layer=M0)
        elems += spira.Polygon(shape=middleCross, layer=M0)
        elems += spira.Box(layer=I0,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.935*tp))
        elems += spira.Box(layer=I0,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.065*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.9375*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.9375*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.0625*tp))
        elems += spira.Box(layer=M1,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.0625*tp))
        elems += spira.Box(layer=I1,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.935*tp))
        elems += spira.Box(layer=I1,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.065*tp))
        elems += spira.Polygon(shape=lowerHalf, layer=M2)
        elems += spira.Polygon(shape=upperHalf, layer=M2)
        elems += spira.Box(layer=I2,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.935*tp))
        elems += spira.Box(layer=I2,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.065*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.9375*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.9375*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.9375*tp,0.0625*tp))
        elems += spira.Box(layer=M3,width=0.125*tp,height=0.125*tp,center=(0.0625*tp,0.0625*tp))
        elems += spira.Box(layer=I3,width=0.06*tp,height=0.06*tp,center=(0.935*tp,0.935*tp))
        elems += spira.Box(layer=I3,width=0.06*tp,height=0.06*tp,center=(0.065*tp,0.065*tp))
        elems += spira.Polygon(shape=lowerHalf, layer=M4)
        elems += spira.Polygon(shape=upperHalf, layer=M4)
        elems += spira.Polygon(shape=middleCross, layer=M4)

        return elems

sys.stdout.write("Adjusting settings.\n")
F = RDD.FILTERS.OUTPUT.PORTS
F['cell_ports'] = False
F['edge_ports'] = False
F['contact_ports'] = False
F = RDD.FILTERS.PCELL.DEVICE
F['boolean'] = True
F['contact_attach'] = True
F = RDD.FILTERS.PCELL.CIRCUIT
F['boolean'] = False

D = PCELL()
sys.stdout.write("Writing output.\n")
D.gdsii_output(os.path.splitext(__file__)[0])