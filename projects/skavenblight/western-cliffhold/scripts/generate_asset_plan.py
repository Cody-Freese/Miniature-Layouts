"""Reconstructed, editable Western Cliffhold schematic asset plan.

This recreates the visual design and shared coordinates of the reference PNG;
the original unrecovered Matplotlib session is not claimed to be preserved.

Run from the Miniature-Layouts repository root:
    python projects/skavenblight/western-cliffhold/scripts/generate_asset_plan.py
    python projects/skavenblight/western-cliffhold/scripts/generate_asset_plan.py --svg

Measurements are conceptual terrain-planning inches, not dimensions of
Printablescenery STL meshes.  The 3D HTML viewer is independent and currently
holds its own matching coordinates in the project viewer/index.html.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Ellipse, PathPatch, Polygon, Rectangle
import matplotlib.patheffects as pe
import numpy as np

# ---------------------------------------------------------------------------
# All coordinates are inches on the hypothetical 96 × 96 inch display.
# West is x=0; north is y=96.
# ---------------------------------------------------------------------------
SIZE_IN = 96
CENTER = (59.0, 49.0)
WALL = (59.0, 49.0, 32.6, 30.8)
TERRACES = [
    (59.6, 51.0, 25.0, 22.0, 4.2),   # inner ground
    (61.6, 54.0, 17.5, 15.8, 9.1),   # second level
    (63.1, 56.1, 10.7, 9.5, 16.0),  # third level
]
PITS = [(44.5, 37.3, 8.0, 9.5), (82.0, 50.0, 7.1, 11.2)]
TOWER = (63.1, 56.1)

BG = '#101b19'
STONE = '#7c796b'
PALE = '#d6c4a8'
WARP = '#aaff70'
MARSH = '#1c6159'
GRID = '#a6a79b'


def ring_polygon(cx, cy, rx, ry, phase=0.0, n=240, irregularity=0.04):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + irregularity * np.sin(5 * a + phase) + 0.018 * np.cos(9 * a - phase)
    return np.column_stack((cx + rx * r * np.cos(a), cy + ry * r * np.sin(a)))


def draw_terrain(ax):
    ax.set_facecolor('#172722')
    rng = np.random.default_rng(713)
    xx = np.linspace(0, SIZE_IN, 420)
    yy = np.linspace(0, SIZE_IN, 420)
    X, Y = np.meshgrid(xx, yy)
    west = 53 / (1 + np.exp(np.clip((X - 18) / 3.6, -50, 50)))
    north = 29 / (1 + np.exp(np.clip((75 - Y) / 4.2, -50, 50)))
    ridges = (0.79 + 0.12*np.sin(Y / 7.6 + X / 9.2)**2 + 0.11*np.cos(Y/5.1-X/4.0)**2)
    noise = (0.6*np.sin(X*0.9 + Y*0.31) + 0.75*np.cos(Y*0.77-X*0.18)
             + .35*np.sin(X*1.93-Y*.48))
    height = (west + north * (X < 95)) * ridges + noise
    # The western cliff fades to the city instead of surrounding the entire site.
    cmap = LinearSegmentedColormap.from_list('cliffs',
        ['#172622', '#2d3933', '#45504a', '#65706e', '#9ba3a4', '#dee7e9'])
    ax.pcolormesh(X, Y, np.ma.masked_where(height < 5, height),
                  cmap=cmap, vmin=5, vmax=60, shading='nearest', rasterized=True, zorder=1)
    ax.contour(X, Y, height, levels=[7, 12, 19, 27, 36, 46],
               colors=['#87928c'], linewidths=.36, alpha=.55, zorder=2)
    # Puddles and swamps: brighter near the southeast and southwest borders.
    for x, y, rx, ry in [(16, 12, 19, 13), (35, 3, 30, 13), (72, 6, 25, 12),
                         (92, 24, 11, 21), (92, 77, 11, 15), (29, 19, 14, 10)]:
        ax.add_patch(Ellipse((x, y), rx*2, ry*2, angle=rng.uniform(-25,25),
                             facecolor=MARSH, edgecolor='#419b90', lw=.65,
                             alpha=.68, zorder=3))
    for i in range(120):
        x, y = rng.uniform(0, 96), rng.uniform(0, 96)
        if (y < 21 or x > 86) and rng.random() > .2:
            ax.plot([x-.3, x+.08], [y-.25, y+.5], color='#9ba45c',
                    lw=.43, alpha=.7, zorder=4)
    # The square grid marks possible removable 24-inch scenery sections.
    for q in range(0, 97, 24):
        ax.plot([q,q],[0,96], color=GRID, lw=.48, ls=':', alpha=.65, zorder=30)
        ax.plot([0,96],[q,q], color=GRID, lw=.48, ls=':', alpha=.65, zorder=30)


def draw_city(ax):
    rng = np.random.default_rng(15142)
    # Large outer ground district and stacked terraces. Draw in ascending order.
    for cx,cy,rx,ry,col in [(59,49,33,31,'#252925'),
                             (59.6,51,25,22,'#41443b'),
                             (61.6,54,17.5,15.8,'#5e5d52'),
                             (63.1,56.1,10.7,9.5,'#7d7664')]:
        ax.add_patch(Polygon(ring_polygon(cx,cy,rx,ry),closed=True,
                             facecolor=col,edgecolor='#b8ad96',lw=2.8,zorder=7))
        ax.add_patch(Polygon(ring_polygon(cx,cy,rx*.98,ry*.98,.2),closed=True,
                             facecolor='none',edgecolor='#e4d4b4',lw=.85,zorder=8))
    for cx,cy,rx,ry in PITS:
        ax.add_patch(Ellipse((cx,cy),rx*2,ry*2,facecolor='#102d17',
                             edgecolor='#b8aa8f',lw=3,zorder=11))
        ax.add_patch(Ellipse((cx,cy),rx*1.72,ry*1.70,facecolor='#285b30',
                             edgecolor=WARP,lw=1.15,zorder=12,alpha=.94))
        for offset in [-.40, .0,.40]:
            ax.plot([cx-rx*.60,cx+rx*.60],[cy+offset*ry,cy+offset*ry+1.3],
                    color='#779c65',lw=1.1,alpha=.52,zorder=13)
        ax.text(cx,cy,'INDUSTRIAL\nVOID',color='#d9f8c8',size=6.2,
                ha='center',va='center',fontweight='bold',zorder=20)
    # Three grand routes, ramshackle stone ramps. Broken by chasms.
    roads = [((60,18),(61,42)),((61,42),(63.1,56.1)),
             ((36,46),(56,54)),((68,59),(84,66)),((20,18),(30,22))]
    for (x1,y1),(x2,y2) in roads:
        ax.plot([x1,x2],[y1,y2],color='#292923',lw=7,zorder=13)
        ax.plot([x1,x2],[y1,y2],color='#c6b18a',lw=3.1,ls='--',zorder=14)
    # The city wall is thick stone, with uneven perimeter towers.
    outer = ring_polygon(*WALL, .4, irregularity=.026)
    ax.plot(*outer.T, color='#443f35',lw=7.3,zorder=19)
    ax.plot(*outer.T, color=PALE,lw=4.0,zorder=20)
    for j in range(0,len(outer),15):
        x,y = outer[j]
        ax.add_patch(Rectangle((x-1.7,y-1.7),3.4,3.4,
                               angle=21,facecolor='#514d43',edgecolor=PALE,
                               lw=.5,zorder=21))
    # Distinct southern city gate and outer armory/forge.
    for x,y,w,h in [(60.5,18.8,6.7,5.2),(27.0,20.5,4,4),
                      (83.4,13.0,4.2,4.2),(26.5,56.1,5,4)]:
        ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='#504337',
                               edgecolor='#dec397',lw=1.2,zorder=22))
    # Original Kavzar remnants, later buildings, and chimneys by elevation.
    for _ in range(220):
        x,y = rng.uniform(29,89), rng.uniform(20,82)
        if ((x-59)/33)**2 + ((y-49)/31)**2 >= 0.92:
            continue
        if any(((x-px)/(prx+1.0))**2+((y-py)/(pry+1.0))**2 < 1
               for px,py,prx,pry in PITS):
            continue
        if ((x-TOWER[0])/7.3)**2 + ((y-TOWER[1])/7.3)**2 < 1:
            continue
        tier = sum(((x-cx)/rx)**2+((y-cy)/ry)**2 < .91
                   for cx,cy,rx,ry,_ in TERRACES)
        w,h = rng.uniform(1.0,2.7),rng.uniform(.7,2.4)
        stone=['#403d36','#534c40','#615a4b','#777063'][tier]
        edge=['#807763','#ada18b','#c3b69d','#d2c1a0'][tier]
        ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor=stone,
                               edgecolor=edge,lw=.3,zorder=14+tier))
        if rng.random()<.24:
            ax.plot([x, x], [y+h/2,y+h/2+rng.uniform(1,3)],
                    color='#c8844b',lw=.7,alpha=.7,zorder=17)
    # Tower/Temple: ancient pale ring, patched black central building.
    ax.add_patch(Circle(TOWER,6.25,facecolor='#212320',
                        edgecolor='#dfc6a5',lw=3.2,zorder=23))
    for th in np.linspace(0,2*np.pi,13,endpoint=False):
        x=TOWER[0]+6.2*np.cos(th); y=TOWER[1]+6.2*np.sin(th)
        ax.plot([x,x+np.cos(th)*1.2],[y,y+np.sin(th)*1.2],
                color='#cdb79c',lw=2,zorder=24)
    ax.add_patch(Circle(TOWER,2.1,facecolor='#a5e961',
                        edgecolor='#d9f5ab',lw=1,zorder=25))
    # Green fissures (exposed Skaven underworks) in the ancient districts.
    for x,y in [(39,63),(40,49),(55,37),(73,34),(73,72)]:
        ax.plot([x-1,x+1.2,x-.5,x+1],[y-4,y-1,y+1,y+4],
                color='#99ff6d',lw=2,zorder=26)
    for x,y in [(45,37),(82,50)]:
        ax.text(x,y+8.8,'',color='#dce6d0')


def draw_outer_features(ax):
    # Outer siege road, great southern causeway, and forgotten works.
    roads=[[(0,19),(19,20),(31,26)],[(60,0),(68,17),(62,27)],
           [(77,0),(83,15),(91,24)]]
    for road in roads:
        a=np.array(road)
        ax.plot(a[:,0],a[:,1],color='#6c5e4d',lw=3,zorder=6)
        ax.plot(a[:,0],a[:,1],color='#b29a6b',lw=1.3,ls='--',zorder=7)
    # Mountain cave portals / underground access.
    for x,y in [(45,78),(88,72)]:
        ax.add_patch(Circle((x,y),2.1,color='#172020',ec='#96ff58',lw=2,zorder=16))
    # A few masonry remains beyond the city.
    for x,y in [(12,29),(88,12),(91,35),(24,17)]:
        ax.add_patch(Rectangle((x-2,y-1.5),4,3,facecolor='#50483d',
                               ec='#bb9f79',lw=.6,zorder=17))


def label(ax, x, y, text, fontsize=7.4, rotation=0):
    ax.text(x,y,text,color='#f3edda',ha='center',va='center',
            fontweight='bold',fontsize=fontsize,rotation=rotation,zorder=50,
            path_effects=[pe.withStroke(
                linewidth=2.6,foreground='#111a18')])


def draw_labels(ax):
    label(ax,11,54,'1  WESTERN MASSIF',9,90)
    label(ax,55,89,'2  NORTHERN RIDGES',8)
    label(ax,61,12,'3  SOUTH GATE',8)
    label(ax,67,25,'4  OUTER WARRENS',7.7)
    label(ax,52,61,'5  CRACKED GROUND',7)
    label(ax,67,42,'6  SECOND TERRACE',7)
    label(ax,66,67,'7  THIRD TERRACE',7)
    label(ax,63.1,56.1,'8  BELL',7.0)
    label(ax,44.5,35.8,'9',9.5)
    label(ax,82,43,'10',9.5)
    label(ax,15,11,'11  SWAMP',7.5)
    label(ax,85,9,'12  RUINS / FORGE',7.2)
    ax.text(95,94,'N ↑',ha='right',va='top',color='#f3ecdc',
            size=10,fontweight='bold',zorder=50)


def make_figure():
    plt.rcParams.update({'font.family':'DejaVu Sans'})
    fig=plt.figure(figsize=(16.4,12.3),facecolor='#0e1816')
    fig.text(.026,.948,'SKAVENBLIGHT / WESTERN CLIFFHOLD  ·  SCHEMATIC TERRAIN PLACEMENT',
             color='#f5f0df',fontsize=17,fontweight='bold')
    fig.text(.026,.918,'Reconstructed placement diagram, 96 × 96 inches.  Dotted 24-inch grid marks sixteen potential removable sections.',
             color='#b1bcb5',fontsize=9)
    ax=fig.add_axes([.05,.12,.62,.77]);
    ax.set_xlim(0,96);ax.set_ylim(0,96);ax.set_aspect('equal');
    for spine in ax.spines.values():
        spine.set_visible(True);spine.set_color('#e6d6be');spine.set_linewidth(.7)
    ax.set_xticks([]);ax.set_yticks([])
    draw_terrain(ax)
    draw_outer_features(ax)
    draw_city(ax)
    draw_labels(ax)
    legend=fig.add_axes([.74,.11,.24,.79]);legend.axis('off')
    legend.text(0,1,'WESTERN CLIFFHOLD',color='#f3eddb',fontsize=17,
                fontweight='bold',va='top',transform=legend.transAxes)
    legend.text(0,.943,'96 × 96 in · proposed asset masterplan',color='#aec1b6',
                fontsize=10,va='top',transform=legend.transAxes)
    legend.text(0,.889,'ZONE / BUILD COMPONENT',color='#afe2a5',fontsize=10,
                fontweight='bold',va='top',transform=legend.transAxes)
    zone=[
        ('Western massif','XPS carved cliff; Dwarf mines, bridges'),
        ('Northern ridges','Snow peaks; galleries, Skryre forges'),
        ('Outer wall & main gate','Ramshackle ramparts + gatehouses'),
        ('Ground districts','Tenements, warehouses, markets'),
        ('Fractured inner ground','Ruined foundations + green lighting'),
        ('Second terrace +9 in','Stairs, retaining walls, bridges'),
        ('Third terrace +16 in','Cathedral walls and temple ruins'),
        ('Screaming Bell tower','Watch tower + giant bell conversion'),
        ('West undercity pit','Industrial walkways, pipes, crystals'),
        ('East forge pit','Stacks, machinery and green lighting'),
        ('Blighted marsh','Water effects, dead trees, black corn'),
        ('Outer defenses','Armory, forge, siege roads, gnawholes'),
    ]
    for i,(name,desc) in enumerate(zone):
        y=.855-i*.0658
        legend.text(0,y,str(i+1),color='#a9fd69',fontsize=10,
                    fontweight='bold',va='top',transform=legend.transAxes)
        legend.text(.11,y,name,color='#efe8d4',fontsize=9.3,
                    fontweight='bold',va='top',transform=legend.transAxes)
        legend.text(.11,y-.031,desc,color='#acb8b0',fontsize=8.0,
                    va='top',transform=legend.transAxes)
    fig.text(.035,.067,'WEST / SUNSET LIGHT   →',color='#e8b76c',fontsize=11,
             fontweight='bold')
    fig.text(.533,.067,'EAST   →',color='#e8b76c',fontsize=11,fontweight='bold')
    return fig


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1] / 'outputs' / 'maps' / 'asset_plan.png')
    parser.add_argument('--svg',action='store_true',help='Also write an editable SVG.')
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    fig=make_figure()
    fig.savefig(args.output,dpi=140,facecolor=fig.get_facecolor(),bbox_inches='tight')
    print('Wrote',args.output)
    if args.svg:
        svg=args.output.with_suffix('.svg')
        fig.savefig(svg,facecolor=fig.get_facecolor(),bbox_inches='tight')
        print('Wrote',svg)
    plt.close(fig)


if __name__=='__main__':
    main()
