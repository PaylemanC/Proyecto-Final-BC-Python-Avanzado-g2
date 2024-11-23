-- Creation queries
CREATE TABLE IF NOT EXISTS congress(
    congress_id TEXT PRIMARY KEY,
    session TEXT NOT NULL,
    number INTEGER NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS bills(
    bill_id TEXT PRIMARY KEY,
    number INTEGER NOT NULL,
    type TEXT NOT NULL,
    description TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS roll_calls(
    roll_call_id TEXT PRIMARY KEY,
    bill_id TEXT NOT NULL,
    congress_id TEXT NOT NULL,
    status TEXT,
    date TEXT NOT NULL,
    loaded_etl_at TEXT NOT NULL,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (congress_id) REFERENCES congress(congress_id)
) STRICT;

CREATE TABLE IF NOT EXISTS parties(
    party_code TEXT PRIMARY KEY,
    name TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS states(
    state_code TEXT PRIMARY KEY,
    name TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS members(
    member_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    image_url TEXT,
    party_code TEXT NOT NULL,
    state_code TEXT NOT NULL,
    FOREIGN KEY (state_code) REFERENCES states(state_code)
    FOREIGN KEY (party_code) REFERENCES parties(party_code)
) STRICT;

CREATE TABLE IF NOT EXISTS votes(
    vote_id TEXT PRIMARY KEY,
    roll_call_id TEXT NOT NULL,
    member_id TEXT NOT NULL,
    vote TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (roll_call_id) REFERENCES roll_calls(roll_call_id)
) STRICT;

-- Insert queries
INSERT INTO congress (congress_id, session, number) VALUES ('118-1', '1st', '118');
INSERT INTO congress (congress_id, session, number) VALUES ('118-2', '2nd', '118');


INSERT INTO parties (party_code, name) VALUES ('D', 'Democratic');
INSERT INTO parties (party_code, name) VALUES ('R', 'Republican');
INSERT INTO parties (party_code, name) VALUES ('I', 'Independent');


INSERT INTO states (state_code, name) VALUES ('AL', 'Alabama');
INSERT INTO states (state_code, name) VALUES ('AK', 'Alaska');
INSERT INTO states (state_code, name) VALUES ('AZ', 'Arizona');
INSERT INTO states (state_code, name) VALUES ('AR', 'Arkansas');
INSERT INTO states (state_code, name) VALUES ('AS', 'American Samoa');
INSERT INTO states (state_code, name) VALUES ('CA', 'California');
INSERT INTO states (state_code, name) VALUES ('CO', 'Colorado');
INSERT INTO states (state_code, name) VALUES ('CT', 'Connecticut');
INSERT INTO states (state_code, name) VALUES ('DE', 'Delaware');
INSERT INTO states (state_code, name) VALUES ('DC', 'District of Columbia');
INSERT INTO states (state_code, name) VALUES ('FL', 'Florida');
INSERT INTO states (state_code, name) VALUES ('GA', 'Georgia');
INSERT INTO states (state_code, name) VALUES ('GU', 'Guam');
INSERT INTO states (state_code, name) VALUES ('HI', 'Hawaii');
INSERT INTO states (state_code, name) VALUES ('ID', 'Idaho');
INSERT INTO states (state_code, name) VALUES ('IL', 'Illinois');
INSERT INTO states (state_code, name) VALUES ('IN', 'Indiana');
INSERT INTO states (state_code, name) VALUES ('IA', 'Iowa');
INSERT INTO states (state_code, name) VALUES ('KS', 'Kansas');
INSERT INTO states (state_code, name) VALUES ('KY', 'Kentucky');
INSERT INTO states (state_code, name) VALUES ('LA', 'Louisiana');
INSERT INTO states (state_code, name) VALUES ('ME', 'Maine');
INSERT INTO states (state_code, name) VALUES ('MD', 'Maryland');
INSERT INTO states (state_code, name) VALUES ('MA', 'Massachusetts');
INSERT INTO states (state_code, name) VALUES ('MI', 'Michigan');
INSERT INTO states (state_code, name) VALUES ('MN', 'Minnesota');
INSERT INTO states (state_code, name) VALUES ('MS', 'Mississippi');
INSERT INTO states (state_code, name) VALUES ('MO', 'Missouri');
INSERT INTO states (state_code, name) VALUES ('MT', 'Montana');
INSERT INTO states (state_code, name) VALUES ('NE', 'Nebraska');
INSERT INTO states (state_code, name) VALUES ('NV', 'Nevada');
INSERT INTO states (state_code, name) VALUES ('NH', 'New Hampshire');
INSERT INTO states (state_code, name) VALUES ('NJ', 'New Jersey');
INSERT INTO states (state_code, name) VALUES ('NM', 'New Mexico');
INSERT INTO states (state_code, name) VALUES ('NY', 'New York');
INSERT INTO states (state_code, name) VALUES ('NC', 'North Carolina');
INSERT INTO states (state_code, name) VALUES ('ND', 'North Dakota');
INSERT INTO states (state_code, name) VALUES ('MP', 'Northern Mariana Islands');
INSERT INTO states (state_code, name) VALUES ('OH', 'Ohio');
INSERT INTO states (state_code, name) VALUES ('OK', 'Oklahoma');
INSERT INTO states (state_code, name) VALUES ('OR', 'Oregon');
INSERT INTO states (state_code, name) VALUES ('PA', 'Pennsylvania');
INSERT INTO states (state_code, name) VALUES ('RI', 'Rhode Island');
INSERT INTO states (state_code, name) VALUES ('SC', 'South Carolina');
INSERT INTO states (state_code, name) VALUES ('SD', 'South Dakota');
INSERT INTO states (state_code, name) VALUES ('TN', 'Tennessee');
INSERT INTO states (state_code, name) VALUES ('TX', 'Texas');
INSERT INTO states (state_code, name) VALUES ('UT', 'Utah');
INSERT INTO states (state_code, name) VALUES ('VT', 'Vermont');
INSERT INTO states (state_code, name) VALUES ('VA', 'Virginia');
INSERT INTO states (state_code, name) VALUES ('WA', 'Washington');
INSERT INTO states (state_code, name) VALUES ('WV', 'West Virginia');
INSERT INTO states (state_code, name) VALUES ('WI', 'Wisconsin');
INSERT INTO states (state_code, name) VALUES ('WY', 'Wyoming');


