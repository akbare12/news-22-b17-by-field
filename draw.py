#!/usr/bin/env python3
"""news-image-20261122 b17 by-field: 48 stories, BY FIELD bar, hero trio + DATE CHECK."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (163, 22, 33)
RED_D = (122, 16, 24)
CREAM2 = (238, 230, 205)
LINE = (120, 110, 88)

FD = "/usr/share/fonts/truetype/dejavu"

def f_serif(sz, bold=False):
    return ImageFont.truetype(f"{FD}/DejaVuSerif{'-Bold' if bold else ''}.ttf", sz)

def f_sans(sz, bold=False):
    return ImageFont.truetype(f"{FD}/DejaVuSans{'-Bold' if bold else ''}.ttf", sz)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

CHIP = {
    "CONFIRMED": (31, 122, 51),
    "REPORTED": (31, 78, 121),
    "CLAIM": (176, 124, 11),
    "OFFICIAL": (85, 85, 85),
    "ONGOING": (198, 96, 20),
    "FORECAST": (107, 58, 122),
}
FIELD = {
    "W": ("WAR & SECURITY", (122, 31, 31)),
    "P": ("POLITICS", (31, 58, 95)),
    "S": ("SPORT", (31, 92, 46)),
    "M": ("MARKETS", (138, 109, 0)),
    "SO": ("SOCIETY", (107, 58, 122)),
    "H": ("HEALTH & SCIENCE", (15, 95, 107)),
}

def chip(d, x, y, label, h=13):
    f = f_sans(8, True)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 10, y + h], radius=2, fill=CHIP[label])
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return tw + 10

# n, field, kicker, title, body, source, chip, lat, lon
S = [
(1,"W","KYIV · WAR","186 drones fired, 161 shot down","Russia fires 186 drones overnight; air defences down 161. A five-storey block in Dymer falls: 1 dead, 14 unaccounted for. Strikes hit 18 sites.","Ukrainian Air Force · AP","REPORTED",50.4,30.5),
(2,"P","HONG KONG · POLITICS","Hong Kong votes: 98.79% turnout","856 candidates, 723 seats; 5,640 of 5,709 voters cast ballots.","SCMP · Reuters","CONFIRMED",22.3,114.2),
(3,"S","LAS VEGAS · SPORT","Verstappen wins by 0.639s","Beats Norris; Piastri third; 75th win.","F1 · Reuters","CONFIRMED",36.2,-115.1),
(4,"S","TURIN · SPORT","Alcaraz takes ATP Finals","Beats Zverev 6-2, 7-6(7); first title.","ATP · BBC","CONFIRMED",45.1,7.7),
(5,"W","TALLINN · WAR","Estonia closes 5 Russia crossings","Shuts five border crossings from 1 Dec after sabotage attempts.","Reuters","REPORTED",58.6,25.0),
(6,"W","COPENHAGEN · WAR","Denmark expels Russian attaché","Alleged plot to kill a US-Ukrainian rapper.","Reuters","REPORTED",55.7,12.6),
(7,"SO","BRUSSELS · SOCIETY","Belgium controllers join Monday strike","Air traffic controllers join national strike; most Monday flights cancelled.","Reuters","REPORTED",50.8,4.4),
(8,"W","MEDITERRANEAN · WAR","Sparta II still burning, towed home","Hit by drone Saturday; 16 crew safe. Finland blames Ukraine.","Reuters","REPORTED",38.0,18.0),
(9,"P","ANTALYA · POLITICS","COP31 collapses — NO DEAL","Final text drops all fossil-fuel language; EU and ~130 parties reject it. Talks end after 44 hours overtime — the first failure since 2009.","AP · Reuters · Guardian","CONFIRMED",36.9,30.7),
(10,"W","BAHRAIN · WAR","Iran claims 2 Patriot radars hit","Tehran says US Patriot radars at al-Riffa and Awali were hit. Bahrain denies a military strike — a civilian site at Sitra burns, 2 hurt, no deaths.","IRGC vs Bahrain MoI","CLAIM",26.2,50.6),
(11,"W","BENGHAZI · WAR","Corvette Merkury hit off Benghazi","Naval drone hits corvette; ship capsizes, several killed. Attribution disputed.","Reuters","CLAIM",32.1,20.1),
(12,"SO","TEHRAN · SOCIETY","Iran starts power rationing","Blackouts ~2h a day; gas output hit.","Reuters","REPORTED",35.7,51.4),
(13,"W","GAZA · WAR","Gaza: 4 killed as Hamas seeks talks","Israeli fire kills 4 in Gaza; Hamas asks mediators for talks.","AP · Reuters","REPORTED",31.5,34.5),
(14,"P","JERUSALEM · POLITICS","Eisenkot invites Likud to coalition talks","Bloc holds 48 seats, 13 short of a majority.","Reuters","REPORTED",31.8,35.2),
(15,"W","WEST BANK · WAR","Settlers burn 12 cars in Ramallah","Settlers torch cars in Ramallah.","Reuters","REPORTED",31.9,35.2),
(16,"SO","CIKANDE · SOCIETY","Candy-factory fire: 3 dead, 36 missing","Fire began Sat. night; 15 survived.","Detiknews · Basarnas","REPORTED",-6.3,106.3),
(17,"S","WELLINGTON · SPORT","India declare 720/9","Highest Test total in NZ; Rahul 136, Pant 128.","ESPNcricinfo","CONFIRMED",-41.3,174.8),
(18,"P","SEOUL · POLITICS","Minister quits in AI-cheat scandal","Education minister Choi resigns; 111 device cases in exam cheating.","Yonhap","CONFIRMED",37.6,127.0),
(19,"P","NEW DELHI · POLITICS","Nepal PM lands in Delhi, first trip abroad","Balendra Shah meets Modi Monday.","Reuters","REPORTED",28.6,77.2),
(20,"H","IMPHAL · HEALTH","Manipur liquor toll rises","Toll climbs; ~600 treated, 6 arrested.","Reuters","REPORTED",24.8,93.9),
(21,"M","JAKARTA · MARKETS","EU–Indonesia deal signed (date split)","Trade deal signed; date disputed (Sat 21 vs Sun 22).","Reuters","REPORTED",-6.2,106.8),
(22,"W","CANBERRA · WAR","Marles rejects US AUKUS sub report","Calls budget-office report on AUKUS subs 'wrong'.","Reuters","REPORTED",-35.3,149.1),
(23,"P","WASHINGTON · POLITICS","Democrats take the House: 258 seats","Largest majority since 1992; 4 races uncalled.","AP · Reuters","CONFIRMED",38.9,-77.0),
(24,"H","BRASÍLIA · HEALTH","Bolsonaro in intensive care","Acute bowel obstruction; stable, 71.","AP","REPORTED",-15.8,-47.9),
(25,"S","SAN ANTONIO · SPORT","Wembanyama scores 50","19 reb, 5 blk; Spurs win 114-91.","NBA · AP","CONFIRMED",29.4,-98.5),
(26,"H","CAPE CANAVERAL · SCIENCE","Falcon 9 launches NROL-136","Record 32h pad turnaround; booster lands.","SpaceX","OFFICIAL",28.4,-80.5),
(27,"SO","WASHINGTON · SOCIETY","FBI probes NCIC crime-database hack","Second breach in months; state delays dealer checks.","AP","REPORTED",47.6,-122.3),
(28,"W","KHARTOUM · WAR","Drones kill 4 near Khartoum","UN site hit; aid workers trapped.","Reuters","REPORTED",15.6,32.5),
(29,"SO","BAYELSA · SOCIETY","Mourners' boat capsizes: 24 dead","Boat carrying mourners overturns in Bayelsa.","Reuters","REPORTED",4.9,6.3),
(30,"H","DR CONGO · HEALTH","Ebola cases reach 11,613","WHO count; fighting traps medics.","WHO · Reuters","OFFICIAL",-2.9,23.7),
(31,"S","MELBOURNE · SPORT","Melbourne: 70 yrs since 1956 Games","Seventy years since the Olympics opened.","Reuters","REPORTED",-37.8,145.0),
(32,"SO","SYDNEY · SOCIETY","Fred Nile dies, 92","Died 21 Nov, announced 22 Nov.","Reuters","REPORTED",-33.9,151.2),
(33,"S","BRISBANE · SPORT","Cummins stays Test captain","Australia keeps Cummins as Test captain.","Reuters","REPORTED",-27.5,153.0),
(34,"M","WORLD · MARKETS","Bitcoin back above $60,000","Rises past $60,000; $60,020, +1.85%.","Reuters","REPORTED",20.0,-40.0),
(35,"M","SANTA CLARA · MARKETS","Nvidia faces SEC accounting probe","Shares fell ~14% on Friday.","Reuters","REPORTED",37.4,-122.0),
(36,"S","LIVERPOOL · SPORT","Liverpool rout Man Utd 4-0","Pochettino debut ends in a rout.","BBC Sport","CONFIRMED",53.4,-3.0),
(37,"SO","MILAN · SOCIETY","Paolo Bulgari dies, 89","Jewellery heir dies; empire spans a century. Died 21 Nov, announced 22 Nov.","Reuters","REPORTED",45.5,9.2),
(38,"SO","VATICAN · SOCIETY","Pope Leo hosts 1,300 poor guests","Pontiff welcomes 1,300 poor guests.","Vatican News","REPORTED",41.9,12.5),
(39,"W","RIYADH · WAR","Saudi intercepts Houthi missile","Saudi air defences intercept a Houthi missile.","Reuters","REPORTED",24.7,46.7),
(40,"W","SANAA · WAR","Yemen missile intercepted","A missile from Yemen is intercepted en route.","Reuters","REPORTED",15.4,44.2),
(41,"W","ABU DHABI · WAR","Bahrain blames Iran; UAE condemns","Bahrain blames Iran for the radar strike; UAE condemns it.","Reuters","REPORTED",24.5,54.4),
(42,"W","MANILA · WAR","Chinese bomber turns back","Bomber turns back 170 km from Manila.","Reuters","REPORTED",14.6,121.0),
(43,"W","TAIPEI · WAR","Taiwan holds live-fire drills","Taiwan stages live-fire drills.","Reuters","REPORTED",23.7,121.0),
(44,"M","OTTAWA · MARKETS","US–Canada trade deal 'fairly close'","Deal said to be fairly close.","Reuters","REPORTED",45.4,-75.7),
(45,"M","LONDON · MARKETS","Gold nears $3,553","Gold trades near $3,553 an ounce.","Reuters","REPORTED",51.5,-0.1),
(46,"W","GAZA CITY · WAR","Aid-van strike kills 3","Drone hits food-aid van in Tel al-Hawa. WCK: the van was not ours.","AP","REPORTED",31.5,34.5),
(47,"W","HEBRON · WAR","Settlers attack home in Hebron","Settlers attack a home in Hebron.","Reuters","REPORTED",31.9,35.2),
(48,"W","HELSINKI · WAR","Finland blames Ukraine over Sparta II","Helsinki blames Kyiv for the drone strike on Sparta II.","Reuters","REPORTED",60.2,25.0),
]
BY_ID = {s[0]: s for s in S}
HEROES = [9, 1, 10]
CARDS = [2, 3, 4, 16, 17, 18, 23, 25, 26, 30, 34, 36]
ALSO = [n for n in range(1, 49) if n not in HEROES and n not in CARDS]

OFF = {4:(-9,8), 37:(10,-8), 7:(0,-9), 38:(9,9), 11:(-9,9), 14:(-11,7), 15:(11,-7),
       46:(11,9), 47:(-11,-9), 39:(-9,7), 41:(9,7), 5:(10,7), 48:(-10,-7),
       36:(-8,-7), 45:(9,7), 21:(11,7), 33:(9,-7), 22:(-11,8), 35:(-10,-7),
       27:(-10,-8), 44:(10,-8)}

def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill=(31, 58, 95))
    # conference hall: windows
    for i in range(7):
        d.rectangle([x+14+i*44, y+h-58, x+44+i*44, y+h-14], fill=(240, 200, 90))
        d.line([x+14+i*44, y+h-36, x+44+i*44, y+h-36], fill=(31,58,95), width=2)
    # flags row
    cols = [(163,22,33),(31,92,46),(240,200,90),(31,78,121),(107,58,122),(240,120,40)]
    for i, c in enumerate(cols):
        d.rectangle([x+20+i*52, y+12, x+56+i*52, y+34], fill=c)
        d.line([x+38+i*52, y+34, x+38+i*52, y+52], fill=(230,230,220), width=2)
    # globe
    d.ellipse([x+w-92, y+14, x+w-34, y+72], fill=(120,180,210), outline=(255,255,255), width=2)
    d.arc([x+w-88, y+20, x+w-38, y+66], 200, 340, fill=(31,58,95), width=3)
    d.line([x+w-92, y+43, x+w-34, y+43], fill=(255,255,255), width=2)
    # NO DEAL stamp
    st = Image.new("RGBA", (150, 44), (0,0,0,0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([2,2,147,41], outline=(255,60,60), width=4)
    sd.text((12,9), "NO DEAL", font=f_sans(24, True), fill=(255,60,60))
    st = st.rotate(-10, expand=True, resample=Image.BICUBIC)
    img.paste(st, (x+90, y+58), st)

def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill=(13, 27, 46))
    # explosion glow (low, near rooftops)
    for r in (34, 24, 14):
        d.ellipse([x+w-100-r, y+h-34-r, x+w-100+r, y+h-34+r], fill=(230,120,30))
    # skyline
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 20:
        bw = rnd.randint(18, 34); bh = rnd.randint(28, 74)
        d.rectangle([bx, y+h-bh, bx+bw, y+h], fill=(8, 16, 28))
        for wy in range(y+h-bh+6, y+h-6, 12):
            for wx in range(bx+4, bx+bw-4, 10):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx+4, wy+6], fill=(240, 200, 90))
        bx += bw + 4
    # drones with red trails
    for (dx, dy, ln) in [(40, 26, 34), (120, 16, 26), (200, 34, 30), (260, 20, 22)]:
        d.line([x+dx, y+dy, x+dx+ln, y+dy+6], fill=(255, 60, 60), width=2)
        d.ellipse([x+dx-3, y+dy-3, x+dx+3, y+dy+3], fill=(255,255,255))
    d.ellipse([x+22, y+8, x+50, y+36], fill=(220, 220, 200))

def scene_radar(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill=(16, 24, 40))
    # moon
    d.ellipse([x+w-64, y+10, x+w-28, y+46], fill=(225, 225, 205))
    # radar dome
    d.pieslice([x+30, y+h-96, x+150, y+h-8], 180, 360, fill=(150, 155, 165))
    d.rectangle([x+30, y+h-30, x+150, y+h], fill=(110, 114, 124))
    # mast + beam
    d.line([x+200, y+h-10, x+200, y+26], fill=(200,200,200), width=4)
    d.line([x+200, y+26, x+252, y+52], fill=(255, 140, 40), width=3)
    d.ellipse([x+192, y+18, x+208, y+34], fill=(255,140,40))
    # ground lights
    for i in range(8):
        d.ellipse([x+170+i*16, y+h-12, x+178+i*16, y+h-4], fill=(240, 200, 90))
    # fire glow at base
    d.ellipse([x+w-96, y+h-52, x+w-40, y+h-4], fill=(230, 110, 30))
    d.ellipse([x+w-84, y+h-40, x+w-52, y+h-8], fill=(250, 180, 60))

SCENES = {9: scene_cop31, 1: scene_drones, 10: scene_radar}

def draw():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=RED)
    # masthead
    d.text((10, 12), "THE WORLD IN ONE DAY", font=f_sans(13, True), fill=RED_D)
    d.text((W-10, 12), "48 STORIES  ·  7 REGIONS  ·  6 FIELDS", font=f_sans(13, True), fill=INK, anchor="ra")
    d.text((W//2, 30), "Sunday 22 November 2026", font=f_serif(40, True), fill=INK, anchor="ma")
    d.text((W//2, 76), "COP31 fails  ·  186 drones  ·  Bahrain radar claim  —  the day the world said no",
           font=f_serif(14), fill=RED_D, anchor="ma")
    # number strip
    nums = [("186","drones fired"),("161","shot down"),("720/9","India declare"),
            ("98.79%","HK turnout"),("$120bn","adaptation dropped"),("35%","2035 power kept"),
            ("44h","COP31 overtime"),("50","Wembanyama pts"),("258","Dems seats"),("11,613","Ebola cases")]
    cw = (W-20)/10
    y0 = 94
    for i, (n, lab) in enumerate(nums):
        x0 = 10 + i*cw
        d.rectangle([x0, y0, x0+cw-2, y0+46], outline=LINE, width=1)
        d.text((x0+cw/2-1, y0+3), n, font=f_sans(19, True), fill=RED_D, anchor="ma")
        d.text((x0+cw/2-1, y0+28), lab, font=f_sans(9), fill=INK, anchor="ma")
    # BY FIELD bar
    counts = {}
    for s in S:
        counts[s[1]] = counts.get(s[1], 0) + 1
    order = ["W", "P", "S", "M", "SO", "H"]
    labels = {"W": "WAR & SECURITY", "P": "POLITICS", "S": "SPORT", "M": "MARKETS",
              "SO": "SOCIETY", "H": "HEALTH & SCI"}
    y0 = 146
    x = 10
    for k in order:
        name, col = FIELD[k]
        wseg = (W-20) * counts[k] / 48
        d.rectangle([x, y0, x+wseg-1, y0+22], fill=col)
        d.text((x+wseg/2, y0+5), f"{labels[k]} {counts[k]}", font=f_sans(9, True), fill=(255,255,255), anchor="ma")
        x += wseg
    # UTC strip
    y0 = 172
    d.rectangle([10, y0, W-10, y0+18], fill=(31, 58, 95))
    d.text((14, y0+3), "THE DAY IN UTC", font=f_sans(11, True), fill=(255, 210, 90))
    d.text((150, y0+3), "01:00 HK polls open  ·  03:00 COP31 objections close  ·  06:00 adoption vote  ·  ~16:00 COP31 fails  ·  18:13 Dems 258  ·  20:43 Alcaraz wins",
           font=f_sans(11), fill=(255,255,255))
    # heroes
    y0 = 196
    hw = (W-20-2*8)//3
    for i, n in enumerate(HEROES):
        s = BY_ID[n]
        x0 = 10 + i*(hw+8)
        d.rectangle([x0, y0, x0+hw, y0+196], outline=INK, width=1)
        SCENES[n](d, x0+1, y0+1, hw-2, 104)
        d.text((x0+8, y0+112), s[2], font=f_sans(9, True), fill=RED_D)
        chip(d, x0+hw-78, y0+110, s[6])
        ty = y0+128
        for ln in wrap(d, s[3], f_serif(15, True), hw-16):
            d.text((x0+8, ty), ln, font=f_serif(15, True), fill=INK)
            ty += 18
        for ln in wrap(d, s[4], f_sans(10), hw-16):
            d.text((x0+8, ty), ln, font=f_sans(10), fill=INK)
            ty += 12
        d.text((x0+8, y0+180), f"Source: {s[5]}", font=f_sans(8), fill=(90, 85, 70))
    # small cards: 4 cols x 3 rows
    y0 = 400
    cw2 = (W-20-3*6)//4
    ch2 = 78
    for idx, n in enumerate(CARDS):
        s = BY_ID[n]
        r, c = divmod(idx, 4)
        x0 = 10 + c*(cw2+6)
        yy = y0 + r*(ch2+6)
        name, col = FIELD[s[1]]
        d.rectangle([x0, yy, x0+cw2, yy+ch2], outline=INK, width=1)
        d.rectangle([x0+1, yy+1, x0+cw2-1, yy+15], fill=col)
        d.text((x0+6, yy+3), f"#{n}", font=f_sans(9, True), fill=(255,255,255))
        d.text((x0+cw2-6, yy+3), s[2].split(" · ")[-1], font=f_sans(8, True), fill=(255,255,255), anchor="ra")
        ty = yy+19
        for ln in wrap(d, s[3], f_sans(10, True), cw2-12)[:2]:
            d.text((x0+6, ty), ln, font=f_sans(10, True), fill=INK)
            ty += 12
        for ln in wrap(d, s[4], f_sans(9), cw2-12)[:2]:
            d.text((x0+6, ty), ln, font=f_sans(9), fill=INK)
            ty += 11
        chip(d, x0+6, yy+ch2-16, s[6], h=12)
        d.text((x0+cw2-6, yy+ch2-15), s[5], font=f_sans(8), fill=(90,85,70), anchor="ra")
    # map + ALSO
    my0, my1 = 654, 800
    d.text((10, 648), "THE WORLD — WHERE IT HAPPENED", font=f_sans(11, True), fill=RED_D)
    d.text((472, 648), "PIN = STORY NUMBER — red = reported · amber = claim", font=f_sans(8), fill=(90,85,70), anchor="ra")
    # continents
    NA=[(-168,66),(-140,70),(-125,71),(-110,68),(-95,69),(-85,66),(-75,62),(-65,60),(-55,52),(-60,47),(-70,44),(-75,39),(-80,32),(-81,26),(-84,30),(-90,21),(-97,26),(-105,20),(-110,23),(-114,29),(-120,34),(-125,40),(-124,48),(-130,54),(-140,60),(-155,58),(-165,60)]
    SA=[(-80,10),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-70,-50),(-68,-55),(-66,-55),(-65,-45),(-62,-40),(-58,-35),(-52,-32),(-48,-28),(-41,-23),(-39,-17),(-35,-9),(-35,-6),(-40,-3),(-44,-2),(-50,0),(-52,4),(-55,6),(-60,8),(-65,10),(-72,12),(-77,8)]
    EU=[(-10,36),(-9,43),(-2,44),(-1,46),(-4,48),(0,50),(2,51),(5,53),(8,55),(8,57),(10,59),(5,60),(5,62),(12,65),(18,69),(25,71),(30,70),(35,68),(40,67),(45,68),(50,69),(55,68),(60,69),(65,68),(68,66),(60,65),(55,60),(50,55),(45,50),(40,47),(35,45),(30,45),(28,44),(23,40),(22,37),(26,38),(30,36),(33,36),(30,38),(27,40),(23,40),(19,42),(15,44),(12,44),(8,44),(3,42),(0,40),(-2,37),(-6,36),(-9,37)]
    AF=[(-17,15),(-17,21),(-15,27),(-10,31),(-5,35),(0,36),(10,37),(11,34),(20,32),(25,32),(30,31),(32,31),(34,28),(35,23),(37,18),(39,15),(43,12),(48,11),(51,11),(51,12),(48,10),(44,5),(42,0),(40,-5),(40,-10),(36,-18),(35,-23),(32,-26),(28,-33),(26,-34),(20,-35),(17,-32),(15,-27),(13,-18),(12,-12),(13,-6),(9,-1),(9,4),(-8,4),(-13,8),(-17,12)]
    AS=[(30,36),(35,36),(36,33),(35,30),(40,30),(43,28),(48,30),(50,29),(52,27),(55,26),(57,25),(60,25),(62,25),(66,25),(70,24),(75,20),(77,15),(80,13),(80,10),(77,8),(80,7),(85,10),(88,15),(90,20),(92,21),(95,16),(97,10),(100,8),(103,5),(105,2),(108,5),(110,10),(112,15),(115,20),(118,25),(120,28),(122,32),(125,35),(127,38),(130,42),(132,43),(135,44),(138,46),(140,50),(142,55),(142,60),(140,65),(135,68),(130,70),(125,72),(120,72),(115,73),(110,74),(105,76),(100,77),(95,76),(90,75),(85,74),(80,73),(75,72),(70,72),(68,70),(65,68),(60,66),(55,66),(50,64),(48,60),(47,55),(45,50),(43,45),(40,42),(38,40),(35,38),(32,36)]
    AU=[(113,-22),(114,-30),(115,-34),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(147,-39),(150,-37),(153,-32),(153,-27),(151,-24),(146,-19),(142,-15),(142,-11),(140,-17),(136,-15),(135,-12),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20)]
    UK=[(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)]
    JP=[(130,31),(132,33),(135,34),(137,35),(139,36),(140,38),(141,40),(142,42),(143,44),(145,44),(143,42),(141,39),(140,36),(138,35),(136,33),(133,32)]
    NZ=[(167,-45),(170,-43),(173,-41),(175,-38),(177,-38),(175,-40),(173,-42),(170,-44),(168,-46)]
    mx0, my0b, mw, mh = 10, 664, 460, 132
    def proj(lon, lat):
        return (mx0 + (lon+170)/360*mw, my0b + (80-lat)/135*mh)
    d.rectangle([mx0-2, my0b-2, mx0+mw+2, my0b+mh+2], fill=(210, 225, 235), outline=LINE)
    for poly in (AS, AF, EU, NA, SA, AU, UK, JP, NZ):
        d.polygon([proj(lo, la) for lo, la in poly], fill=(222, 205, 160), outline=(150, 135, 105))
    # grid
    for gx in range(-150, 181, 30):
        x = proj(gx, 0)[0]
        d.line([x, my0b, x, my0b+mh], fill=(255,255,255), width=1)
    for gy in range(-45, 76, 30):
        y = proj(0, gy)[1]
        d.line([mx0, y, mx0+mw, y], fill=(255,255,255), width=1)
    # pins
    for s in S:
        n = s[0]
        px, py = proj(s[8], s[7])
        dx, dy = OFF.get(n, (0, 0))
        px += dx; py += dy
        col = (176, 124, 11) if s[6] == "CLAIM" else RED
        d.ellipse([px-6, py-6, px+6, py+6], fill=col, outline=(255,255,255), width=1)
        d.text((px, py-4), str(n), font=f_sans(7, True), fill=(255,255,255), anchor="ma")
    # ALSO list, 2 columns
    ax0 = 490
    d.text((ax0, 648), "ALSO ON SUNDAY — 33 MORE STORIES", font=f_sans(11, True), fill=RED_D)
    f9 = f_sans(9)
    col1 = ALSO[:17]; col2 = ALSO[17:]
    for ci, col in enumerate((col1, col2)):
        cx = ax0 + ci*272
        for ri, n in enumerate(col):
            s = BY_ID[n]
            yy = 668 + ri*8
            d.text((cx, yy), str(n), font=f_sans(8, True), fill=RED_D)
            d.text((cx+16, yy), s[3], font=f9, fill=INK)
    # DATE CHECK
    y0 = 812
    d.rectangle([10, y0, W-10, y0+128], outline=RED, width=2)
    d.text((16, y0+5), "DATE CHECK", font=f_sans(12, True), fill=RED_D)
    d.text((110, y0+5), "Every story above happened or was first reported on Sunday 22 November 2026.", font=f_sans(11, True), fill=INK)
    d.text((W-14, y0+5), "WIRES READ UP TO 23:00 UTC", font=f_sans(10, True), fill=RED_D, anchor="ra")
    f10 = f_sans(10)
    ly = y0+26
    for ln in wrap(d, "LEFT OUT (not 22 Nov):  400-drone barrage (19–20 Nov)  ·  El Chapo Isidro captured (20 Nov)  ·  BepiColombo Mercury orbit (21 Nov, burn 18:24 GMT)  ·  Kryvyi Rih (20 Nov night)  ·  Peru quake (20 Nov)  ·  Hormuz tankers hit (Sat 21 Nov 05:00 GMT, reported Sun 17:13 UTC).", f10, W-40):
        d.text((16, ly), ln, font=f10, fill=INK)
        ly += 13
    ly += 4
    for ln in wrap(d, "NOT YET:  Dymer final toll  ·  4 House races uncalled  ·  EU–Indonesia deal date split (Sat 21 vs Sun 22)  ·  Nigeria boat date (Fri 20 vs Sun 22)  ·  FBI hack date split (Fri 20 / Sat 21)  ·  Sparta II hit Sat 21, still burning Sun  ·  COP32 venue undecided.", f10, W-40):
        d.text((16, ly), ln, font=f10, fill=INK)
        ly += 13
    # footer
    fy = 950
    d.text((10, fy), "SOURCES: AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · Yonhap · Anadolu · Detiknews · WHO · SpaceX", font=f_sans(9), fill=INK)
    d.text((10, fy+13), "CONFIRMED = 2+ outlets  ·  REPORTED = carried by the wires today  ·  CLAIM = one side, unverified  ·  OFFICIAL = recorded result  ·  FORECAST = not yet decided", font=f_sans(9), fill=INK)
    d.text((W-10, fy+13), "Scenes are drawn illustrations, not photographs.", font=f_sans(9), fill=(90,85,70), anchor="ra")
    d.line([10, fy+28, W-10, fy+28], fill=RED, width=2)
    img.save("entry.png", optimize=True)
    print("saved", os.path.getsize("entry.png"), "bytes")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    draw()
