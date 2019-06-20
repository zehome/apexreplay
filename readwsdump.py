#!/usr/bin/env python

import datetime
import psycopg2
import psycopg2.extras
import re
from dataclasses import dataclass, field
from apex.parsetable import parse_table, str_to_interval
from typing import List
from string import Formatter

sessions = []

def td_to_str(td):
    minutes, remainder = divmod(int(td.total_seconds()), 60)
    seconds, _ = divmod(remainder, 1)
    milliseconds = td.microseconds // 1000
    return f"{minutes}:{seconds}.{milliseconds}"


@dataclass()
class Lap:
    last_lap: datetime.timedelta = None
    # gap: datetime.timedelta = None
    # best_lap: datetime.timedelta = None

    def __str__(self):
        return td_to_str(self.last_lap)

@dataclass(order=True)
class Pilot:
    group: str = field(default="", repr=False)
    position: int = field(default=0, repr=False)
    number: int = field(default=0, repr=False, hash=True)
    color: str = field(default="", repr=False)
    club: str = field(default="", repr=False)
    name: str = field(default="", repr=True, compare=True, hash=True)
    laps: List[Lap] = field(default_factory=list)

    def best_lap(self):
        bestlap = None
        for lap in self.laps:
            if lap.last_lap is None:
                continue
            if bestlap is None or lap.last_lap < bestlap.last_lap:
                bestlap = lap
        return bestlap


@dataclass()
class Session:
    name: str
    date: datetime.datetime
    grid_raw: str
    grid: any
    pilots: List[Pilot] = field(default_factory=list)

    def is_valid(self):
        for p in self.pilots:
            if p.best_lap() is not None:
                return True
        return False

    def append(self, pilot):
        self.pilots.append(pilot)

    def pilot(self, row_number):
        return self.pilots[row_number - 1]

    def best_laps(self):
        return {
            p.name: str(p.best_lap())
            for p in sorted(self.pilots)
        }


wsmap = {
    3: "position",
    8: "last_lap",
    9: "gap",
    10: "best_lap",
}

class WsReader:
    def __init__(self, db):
        self.db = db
        self.tracks = {}
        self.sessions = {}
        self.init_tracks()

    def init_tracks(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT id, name FROM track")
            for r in cur:
                self.tracks[r[1]] = r[0]

    def save_session(self, session):
        # for pilot in session.pilots:
        #     print(f"Pilot: {pilot.name}")
        #     print("Laps: {}".format([str(l) for l in pilot.laps]))
        if not session.is_valid():
            return
        print(f"[{session.name}][{session.date.strftime('%Y-%m-%d %H:%M')}]: {session.best_laps()}")
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO session(id_track, ts, grid) VALUES (%s, %s, %s) RETURNING id",
                (self.tracks[session.name], session.date, session.grid_raw),
            )
            id_session = cur.fetchone()[0]
            for pilot in session.pilots:
                for lap in pilot.laps:
                    cur.execute(
                        "INSERT INTO laps(id_session, name, laptime) VALUES (%s, %s, %s)",
                        (id_session, pilot.name, lap.last_lap),
                    )
        self.db.commit()
        del self.sessions[session.name]

    def read_db(self):
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            res = cur.execute("SELECT * FROM apex_live_ws where processed is null ORDER BY name, id ASC")
            for r in cur.fetchall():
                print(".", end='', flush=True)
                session = self.sessions.get(r["name"])
                for line in r["frame"].splitlines():
                    self.readline(line, session, name=r["name"], ts=r["ts"])
                cur.execute("UPDATE apex_live_ws SET processed=%s WHERE id=%s", (datetime.datetime.now(), r["id"]))
        self.db.commit()

    def readline(self, line, session, name, ts=None):
        ls = line.split("|")
        if ls[0] == "init" and session:
            self.save_session(session)
        elif ls[0] == "grid":
            html = "<table>{0}</table>".format(ls[2])
            t = parse_table(html)
            if t:
                session = Session(
                    date=ts if ts else datetime.datetime.now(),
                    name=name,
                    grid=t,
                    grid_raw=html,
                )
                self.sessions[name] = session
                for r in t:
                    if r:
                        session.append(Pilot(
                            group=r["group"],
                            position=r["position"],
                            number=r["number"],
                            name=r["name"],
                        ))
        elif session is not None:
            m = re.match(r"r([0-9]+)c([0-9]+)", ls[0])
            if m:
                row = int(m.group(1))
                column = wsmap.get(int(m.group(2)))
                if column == "last_lap":
                    last_lap = str_to_interval(ls[2])
                    pilot = session.pilot(row)
                    pilot.laps.append(Lap(last_lap=last_lap))
        return session

if __name__ == "__main__":
    import sys, time
    session = None
    db = psycopg2.connect(database="ed")
    worker = WsReader(db)
    while True:
        worker.read_db()
        time.sleep(30)
