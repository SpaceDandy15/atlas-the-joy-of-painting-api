CREATE TABLE painting (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    episode_number VARCHAR,
    season_number VARCHAR,
    air_date TIMESTAMP
);

CREATE TABLE color (
    id SERIAL PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE painting_color (
    painting_id INTEGER REFERENCES painting(id) ON DELETE CASCADE,
    color_id INTEGER REFERENCES color(id) ON DELETE CASCADE,
    UNIQUE (painting_id, color_id)
);

CREATE TABLE painting_subject (
    painting_id INTEGER REFERENCES painting(id) ON DELETE CASCADE,
    subject_id INTEGER REFERENCES subject(id) ON DELETE CASCADE,
    UNIQUE (painting_id, subject_id)
);
