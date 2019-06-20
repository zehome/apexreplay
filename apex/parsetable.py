#!/usr/bin/env python

# pip install pandas lxml html5lib bs4

import pandas as pd
import datetime

html="""<tbody><tr data-id="r0" class="head" data-pos="0"><td data-id="c1" data-type="grp" data-pr="6"></td><td data-id="c2" data-type="sta" data-pr="1"></td><td data-id="c3" data-type="rk" data-pr="1">Cla</td><td data-id="c4" data-type="no" data-pr="1">Kart</td><td data-id="c5" data-type="" data-pr="6" data-width="21">Colore</td><td data-id="c6" data-type="" data-pr="6" data-width="5" data-min="3">Club</td><td data-id="c7" data-type="dr" data-pr="1" data-width="24" data-min="16">Pilota</td><td data-id="c8" data-type="llp" data-pr="2" data-width="17" data-min="7">Ultimo T.</td><td data-id="c9" data-type="gap" data-pr="1" data-width="17" data-min="8">Distacco</td><td data-id="c10" data-type="blp" data-pr="6" data-width="14" data-min="7">M.giro</td></tr><tr data-id="r1" data-pos="1"><td data-id="r1c1" class="gs"></td><td data-id="r1c2" class="sr"></td><td class="rk"><div><p data-id="r1c3" class="">1</p></div></td><td class="no"><div data-id="r1c4" class="no2">7</div></td><td data-id="r1c5" class="in"></td><td data-id="r1c6" class="in"></td><td data-id="r1c7" class="dr">ELIA</td><td data-id="r1c8" class="tb">48.146</td><td data-id="r1c9" class="in">Giro 3</td><td data-id="r1c10" class="in">48.146</td></tr><tr data-id="r2" data-pos="3"><td data-id="r2c1" class="gf"></td><td data-id="r2c2" class="sr"></td><td class="rk"><div><p data-id="r2c3" class="">3</p></div></td><td class="no"><div data-id="r2c4" class="no2">20</div></td><td data-id="r2c5" class="in"></td><td data-id="r2c6" class="in"></td><td data-id="r2c7" class="dr">NICOLAS</td><td data-id="r2c8" class="ti">49.988</td><td data-id="r2c9" class="ib">5.974</td><td data-id="r2c10" class="in">49.988</td></tr><tr data-id="r3" data-pos="2"><td data-id="r3c1" class="gs"></td><td data-id="r3c2" class="sr"></td><td class="rk"><div><p data-id="r3c3" class="">2</p></div></td><td class="no"><div data-id="r3c4" class="no2">42</div></td><td data-id="r3c5" class="in"></td><td data-id="r3c6" class="in"></td><td data-id="r3c7" class="dr">TATIANO</td><td data-id="r3c8" class="ti">48.245</td><td data-id="r3c9" class="ib">2.786</td><td data-id="r3c10" class="in">48.245</td></tr><tr data-id="r4" data-pos="7"><td data-id="r4c1" class="gl"></td><td data-id="r4c2" class="sr"></td><td class="rk"><div><p data-id="r4c3" class="">7</p></div></td><td class="no"><div data-id="r4c4" class="no2">12</div></td><td data-id="r4c5" class="in"></td><td data-id="r4c6" class="in"></td><td data-id="r4c7" class="dr">SAM</td><td data-id="r4c8" class="ti">49.272</td><td data-id="r4c9" class="ib">16.658</td><td data-id="r4c10" class="in">49.272</td></tr><tr data-id="r5" data-pos="6"><td data-id="r5c1" class="gf"></td><td data-id="r5c2" class="sr"></td><td class="rk"><div><p data-id="r5c3" class="">6</p></div></td><td class="no"><div data-id="r5c4" class="no2">29</div></td><td data-id="r5c5" class="in"></td><td data-id="r5c6" class="in"></td><td data-id="r5c7" class="dr">MATTEO</td><td data-id="r5c8" class="ti">51.369</td><td data-id="r5c9" class="ib">16.222</td><td data-id="r5c10" class="in">51.369</td></tr><tr data-id="r6" data-pos="9"><td data-id="r6c1" class="gs"></td><td data-id="r6c2" class="su"></td><td class="rk"><div><p data-id="r6c3" class="">9</p></div></td><td class="no"><div data-id="r6c4" class="no2">18</div></td><td data-id="r6c5" class="in"></td><td data-id="r6c6" class="in"></td><td data-id="r6c7" class="dr">LORENZO</td><td data-id="r6c8" class="tn">53.483</td><td data-id="r6c9" class="ib">25.601</td><td data-id="r6c10" class="in">53.169</td></tr><tr data-id="r7" data-pos="10"><td data-id="r7c1" class="gf"></td><td data-id="r7c2" class="sd"></td><td class="rk"><div><p data-id="r7c3" class="">10</p></div></td><td class="no"><div data-id="r7c4" class="no2">13</div></td><td data-id="r7c5" class="in"></td><td data-id="r7c6" class="in"></td><td data-id="r7c7" class="dr">RAFFAELE</td><td data-id="r7c8" class="tn">1:00.184</td><td data-id="r7c9" class="ib">31.661</td><td data-id="r7c10" class="in">57.766</td></tr><tr data-id="r8" data-pos="4"><td data-id="r8c1" class="gl"></td><td data-id="r8c2" class="sr"></td><td class="rk"><div><p data-id="r8c3" class="">4</p></div></td><td class="no"><div data-id="r8c4" class="no2">77</div></td><td data-id="r8c5" class="in"></td><td data-id="r8c6" class="in"></td><td data-id="r8c7" class="dr">MARCO</td><td data-id="r8c8" class="ti">48.929</td><td data-id="r8c9" class="ib">6.565</td><td data-id="r8c10" class="in">48.929</td></tr><tr data-id="r9" data-pos="5"><td data-id="r9c1" class="gs"></td><td data-id="r9c2" class="sr"></td><td class="rk"><div><p data-id="r9c3" class="">5</p></div></td><td class="no"><div data-id="r9c4" class="no2">14</div></td><td data-id="r9c5" class="in"></td><td data-id="r9c6" class="in"></td><td data-id="r9c7" class="dr">FABRIZIO</td><td data-id="r9c8" class="ti">49.484</td><td data-id="r9c9" class="ib">10.112</td><td data-id="r9c10" class="in">49.484</td></tr><tr data-id="r10" data-pos="8"><td data-id="r10c1" class="gs"></td><td data-id="r10c2" class="sr"></td><td class="rk"><div><p data-id="r10c3" class="">8</p></div></td><td class="no"><div data-id="r10c4" class="no2">23</div></td><td data-id="r10c5" class="in"></td><td data-id="r10c6" class="in"></td><td data-id="r10c7" class="dr">ADRIAN</td><td data-id="r10c8" class="ti">52.994</td><td data-id="r10c9" class="ib">23.503</td><td data-id="r10c10" class="in">52.994</td></tr><tr data-id="r11" data-pos="11"><td data-id="r11c1" class="gl"></td><td data-id="r11c2" class="sr"></td><td class="rk"><div><p data-id="r11c3" class="">11</p></div></td><td class="no"><div data-id="r11c4" class="no2">16</div></td><td data-id="r11c5" class="in"></td><td data-id="r11c6" class="in"></td><td data-id="r11c7" class="dr">MAXICONO</td><td data-id="r11c8" class="ti">56.382</td><td data-id="r11c9" class="ib">32.309</td><td data-id="r11c10" class="in">56.382</td></tr><tr data-id="r12" data-pos="13"><td data-id="r12c1" class="gl"></td><td data-id="r12c2" class="sr"></td><td class="rk"><div><p data-id="r12c3" class="">13</p></div></td><td class="no"><div data-id="r12c4" class="no2">27</div></td><td data-id="r12c5" class="in"></td><td data-id="r12c6" class="in"></td><td data-id="r12c7" class="dr">NRICO</td><td data-id="r12c8" class="tn">1:00.528</td><td data-id="r12c9" class="ib">40.947</td><td data-id="r12c10" class="in">55.259</td></tr><tr data-id="r13" data-pos="12"><td data-id="r13c1" class="gf"></td><td data-id="r13c2" class="sr"></td><td class="rk"><div><p data-id="r13c3" class="">12</p></div></td><td class="no"><div data-id="r13c4" class="no2">4</div></td><td data-id="r13c5" class="in"></td><td data-id="r13c6" class="in"></td><td data-id="r13c7" class="dr">EDO</td><td data-id="r13c8" class="tn">1:02.287</td><td data-id="r13c9" class="ib">40.348</td><td data-id="r13c10" class="in">1:01.330</td></tr></tbody>"""

table_mapping = {
    0: "group",
    1: "unknown2",
    2: "position",
    3: "number",
    4: "color",
    5: "club",
    6: "name",
    7: "last_lap",
    8: "gap",
    9: "best_lap",
}

# interval str map: 1:01.330
def str_to_interval(v):
    v = v.strip()
    minutes = 0
    seconds = 0
    milliseconds = 0
    if ":" in v:
        vs = v.split(":", 1)
        minutes = int(vs[0]) if vs[0] else 0
        v = vs[1]
    if "." in v:
        vs = v.split(".")
        seconds = int(vs[0]) if vs[0] else 0
        v = vs[1]
    try:
        milliseconds = int(v) if v else 0
    except ValueError:
        milliseconds = 0
    return datetime.timedelta(seconds=60 * minutes + seconds, milliseconds=milliseconds)

type_mapping = {
    "position": int,
    "number": int,
    "last_lap": str_to_interval,
    "gap": str_to_interval,
    "best_lap": str_to_interval,
}



def parse_table(html):
    table = pd.read_html(f"<table>{html}</table>")[0]
    td = table.rename(index=int, columns=table_mapping)
    res = []
    for r in td[1:].to_dict(orient='records'):
        res.append({
            k: type_mapping.get(v, str)(v)
        for k, v in r.items() if k in table_mapping.values()})
    return res

parse_table(html)
