#!/usr/bin/env python

from flask import Flask
from flask import jsonify
import psycopg2
import psycopg2.extras

db = psycopg2.connect(database="ed")
app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/tracks')
def tracks():
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM track ORDER BY name ASC")
        return jsonify(cur.fetchall())


@app.route('/api/track/<int:track_id>')
def sessions(track_id):
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT
                session.id,
                to_char(session.ts, 'DD/MM/YYYY HH24:MI:SS') AS ts,
                track.name,
                to_char(lap.bestlap, 'MI:SS.MS') AS bestlap,
                lap.bestlap_name
            FROM session
            JOIN track ON (session.id_track = track.id)
            JOIN LATERAL (
                SELECT
                    first_value(laps.id_session) OVER (PARTITION BY laps.id_session ORDER BY laps.laptime) AS id_session,
                    first_value(laps.laptime) OVER (PARTITION BY laps.id_session ORDER BY laps.laptime) AS bestlap,
                    first_value(laps.name) OVER (PARTITION BY laps.id_session ORDER BY laps.laptime) as bestlap_name
                FROM laps
            ) lap ON (lap.id_session = session.id)
            WHERE id_track=%s
            GROUP BY session.id, track.name, lap.bestlap, lap.bestlap_name
            ORDER BY session.ts DESC;
            """,
            (track_id,)
        )
        return jsonify(cur.fetchall())


@app.route('/api/session/<int:session_id>')
def laps(session_id):
    pilots = {}
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT name, to_char(laptime, 'MI:SS.MS') AS laptime FROM laps
            WHERE id_session=%s
            ORDER BY name, id ASC
            """,
            (session_id,)
        )
        for r in cur:
            pilots.setdefault(r["name"], []).append(r["laptime"])
        return jsonify([
            {"name": k, "laps": v} for k, v in pilots.items()])


if __name__ == '__main__':
    app.run(debug=True)