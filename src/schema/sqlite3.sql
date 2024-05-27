CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL UNIQUE
);

CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    aliases TEXT -- JSON array of aliases
);

CREATE TABLE artist_genres (
    artist_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id),
    PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE albums (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    record_label TEXT,
    release_date TEXT, -- ISO 8601 format
    play_count INTEGER
);

CREATE TABLE album_genres (
    album_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id),
    PRIMARY KEY (album_id, genre_id)
);

CREATE TABLE album_moods (
    album_id INTEGER,
    mood TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id),
    PRIMARY KEY (album_id, mood)
);

CREATE TABLE album_artists (
    album_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums(id),
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    length REAL NOT NULL, -- Length in seconds
    album_id INTEGER,
    play_count INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

CREATE TABLE track_genres (
    track_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id),
    PRIMARY KEY (track_id, genre_id)
);

CREATE TABLE track_moods (
    track_id INTEGER,
    mood TEXT,
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    PRIMARY KEY (track_id, mood)
);

CREATE TABLE track_artists (
    track_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE track_composers (
    track_id INTEGER,
    composer_id INTEGER,
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (composer_id) REFERENCES artists(id),
    PRIMARY KEY (track_id, composer_id)
);

CREATE TABLE track_play_history (
    id INTEGER PRIMARY KEY,
    track_id INTEGER,
    played_at TEXT, -- ISO 8601 format
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

-- Index for the 'name' column in the Artist table, as it will likely be used frequently in search queries
CREATE INDEX idx_artist_name ON artists(name);

-- Indexes for the Genre and Mood tables to speed up lookups by value
CREATE INDEX idx_genre_value ON genres(value);

-- Index for Album table to speed up lookups by name and release date
CREATE INDEX idx_album_name ON albums(name);
CREATE INDEX idx_album_release_date ON albums(release_date);

-- Index for the 'name' column in Track table to speed up lookups by title
CREATE INDEX idx_track_title ON tracks(title);

-- Indexes for TrackPlayHistory to speed up queries based on track_id and played_at
CREATE INDEX idx_trackplayhistory_track_id ON track_play_history(track_id);
CREATE INDEX idx_trackplayhistory_played_at ON track_play_history(played_at);

CREATE INDEX idx_trackmood_mood ON track_moods(mood);
