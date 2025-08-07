from flask import Flask, request, jsonify
from etl.db import get_db_connection

app = Flask(__name__)

@app.route("/episodes", methods=["GET"])
def get_episodes():
    months = request.args.getlist("month")
    colors = request.args.getlist("color")
    subjects = request.args.getlist("subject")
    mode = request.args.get("mode", "and").lower()  # 'and' or 'or'

    conditions = []
    params = []

    # Filter by months (matching air_date month name)
    if months:
        month_conds = []
        for m in months:
            month_conds.append("TO_CHAR(painting.air_date, 'Month') ILIKE %s")
            params.append(f"%{m}%")
        conditions.append("(" + " OR ".join(month_conds) + ")")

    # Filter by colors
    if colors:
        color_conds = []
        for c in colors:
            color_conds.append("color.name ILIKE %s")
            params.append(f"%{c}%")
        conditions.append("(" + " OR ".join(color_conds) + ")")

    # Filter by subjects
    if subjects:
        subject_conds = []
        for s in subjects:
            subject_conds.append("subject.name ILIKE %s")
            params.append(f"%{s}%")
        conditions.append("(" + " OR ".join(subject_conds) + ")")

    connector = " AND " if mode == "and" else " OR "
    where_clause = f"WHERE {connector.join(conditions)}" if conditions else ""

    query = f"""
        SELECT
            painting.id,
            painting.title,
            painting.air_date,
            painting.season,
            painting.episode,
            COALESCE(
                json_agg(DISTINCT color.name) FILTER (WHERE color.name IS NOT NULL),
                '[]'
            ) AS colors,
            COALESCE(
                json_agg(DISTINCT subject.name) FILTER (WHERE subject.name IS NOT NULL),
                '[]'
            ) AS subjects
        FROM painting
        LEFT JOIN painting_color ON painting.id = painting_color.painting_id
        LEFT JOIN color ON color.id = painting_color.color_id
        LEFT JOIN painting_subject ON painting.id = painting_subject.painting_id
        LEFT JOIN subject ON subject.id = painting_subject.subject_id
        {where_clause}
        GROUP BY painting.id, painting.title, painting.air_date, painting.season, painting.episode
        ORDER BY painting.air_date
    """

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "title": row[1],
            "date": row[2].strftime('%Y-%m-%d') if row[2] else None,
            "season": row[3],
            "episode": row[4],
            "colors": row[5],
            "subjects": row[6]
        })

    cur.close()
    conn.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
