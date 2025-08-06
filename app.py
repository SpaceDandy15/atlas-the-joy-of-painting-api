from flask import Flask, request, jsonify
from etl.db import get_db_connection

app = Flask(__name__)

@app.route("/episodes", methods=["GET"])
def get_episodes():
    # Get filter query parameters: multiple allowed for month, color, subject
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
            # Use PostgreSQL TO_CHAR on air_date to get month name
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

    # Combine conditions with AND or OR based on mode param
    connector = " AND " if mode == "and" else " OR "
    where_clause = f"WHERE {connector.join(conditions)}" if conditions else ""

    # Main query: select painting info + aggregate colors and subjects as JSON arrays
    query = f"""
        SELECT
            painting.id,
            painting.title,
            painting.air_date,
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
        GROUP BY painting.id, painting.title, painting.air_date
        ORDER BY painting.air_date
    """

    # Execute query with parameters safely
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    # Build list of results with fields from the query
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "title": row[1],
            "date": row[2].isoformat() if row[2] else None,
            "colors": row[3],
            "subjects": row[4]
        })

    cur.close()
    conn.close()

    # Return JSON response
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
