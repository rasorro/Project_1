CREATE TABLE IF NOT EXISTS [Authentication] (
    [UserID] INTEGER PRIMARY KEY REFERENCES User(ID) ON DELETE CASCADE,
    [PasswordHash] TEXT NOT NULL,
    [SessionID] Text
);

CREATE TABLE IF NOT EXISTS [User] (
    [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
    [Name] TEXT NOT NULL,
    [Email] TEXT UNIQUE NOT NULL,
    [Affiliation] TEXT CHECK ([Affiliation] IN ('Student', 'Alumnus', 'Resident')),
    [College] TEXT DEFAULT NULL CHECK (([Affiliation] = 'Resident' AND [College] IS NULL) OR
        ([Affiliation] != 'resident' AND [College] IN ('Boston University', 'Northeastern University', 'Harvard University',
        'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University',
        'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston',
        'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design')))
);

CREATE TABLE IF NOT EXISTS [Category] (
    [ID] INTEGER PRIMARY KEY,
    [Name] TEXT UNIQUE NOT NULL,
    [Description] TEXT
);

CREATE TABLE IF NOT EXISTS [ActivityGroup] (
    [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
    [Name] TEXT NOT NULL,
    [Description] TEXT,
    [Website] TEXT,
    [ContactUserID] INTEGER REFERENCES [User]([ID]) ON DELETE SET NULL,
    [Email] TEXT REFERENCES [User]([Email]) ON DELETE SET NULL,
    [Address] TEXT,
    [CategoryID] INTEGER,
    [AffiliatedWithCollege] BOOLEAN,
    [College] TEXT CHECK (([AffiliatedWithCollege] = 1 AND [College] IN ('Boston University', 'Northeastern University', 'Harvard University',
        'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University',
        'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston',
        'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design', 'Other'))
    OR ([AffiliatedWithCollege] = 0 AND [College] IS NULL)),
    [RequiresDues] BOOLEAN,
    [SkillLevel] TEXT CHECK ([SkillLevel] IN ('Beginner', 'Intermediate', 'Advanced')),
    FOREIGN KEY ([CategoryID]) REFERENCES [Category]([ID]) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS [Event] (
    [EventID] INTEGER PRIMARY KEY,
    [GroupID] INTEGER NOT NULL REFERENCES [ActivityGroup]([ID]) ON DELETE CASCADE,
    [Name] TEXT NOT NULL,
    [Location] TEXT,
    [Description] TEXT,
    [Date] DATE NOT NULL,
    [StartTime] TIME,
    [EndTime] TIME,
    [Frequency] TEXT
);

CREATE TABLE IF NOT EXISTS [Membership] (
    [Role] TEXT CHECK ([Role] IN ('Member', 'Organizer')),
    [JoinDate] DATE,
    [UserID] INTEGER REFERENCES [User]([ID]) ON DELETE CASCADE,
    [GroupID] INTEGER REFERENCES [ActivityGroup]([ID]) ON DELETE CASCADE,
    PRIMARY KEY ([UserID], [GroupID])
);

CREATE TABLE IF NOT EXISTS [UserInterest] (
    [UserID] INTEGER REFERENCES [User]([ID]) ON DELETE CASCADE,
    [CategoryID] INTEGER REFERENCES [Category]([ID]) ON DELETE CASCADE,
    PRIMARY KEY ([UserID], [CategoryID])
);