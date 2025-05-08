CREATE TABLE Authentication (
    UserID INTEGER PRIMARY KEY REFERENCES User(ID) ON DELETE CASCADE,
    PasswordHash TEXT NOT NULL,
    SessionID Text
);

CREATE TABLE User (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Affiliation TEXT CHECK (Affiliation IN ('student', 'alumnus', 'resident')),
    College TEXT
);

CREATE TABLE Category (
    ID INTEGER PRIMARY KEY,
    Name TEXT UNIQUE NOT NULL,
    Description TEXT
);

CREATE TABLE ActivityGroup (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Description TEXT,
    Website TEXT,
    ContactName TEXT,
    Email TEXT,
    Address TEXT,
    CategoryID INTEGER,
    AffiliatedWithCollege BOOLEAN,
    College TEXT,
    RequiresDues BOOLEAN,
    SkillLevel TEXT CHECK (SkillLevel IN ('beginner', 'intermediate', 'advanced')),
    FOREIGN KEY (CategoryID) REFERENCES Category(ID) ON DELETE SET NULL
);

CREATE TABLE Event (
    EventID INTEGER PRIMARY KEY,
    GroupID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Location TEXT,
    Description TEXT,
    Date TEXT NOT NULL,
    StartTime TEXT,
    EndTime TEXT,
    Frequency TEXT,
    FOREIGN KEY (GroupID) REFERENCES ActivityGroup(ID) ON DELETE CASCADE
);

-- MEMBERSHIP TABLE (user ↔ activity group, includes role + join date)
CREATE TABLE Membership (
    UserID INTEGER,
    GroupID INTEGER,
    Role TEXT CHECK (Role IN ('member', 'organizer')),
    JoinDate TEXT,
    PRIMARY KEY (UserID, GroupID),
    FOREIGN KEY (UserID) REFERENCES User(ID) ON DELETE CASCADE,
    FOREIGN KEY (GroupID) REFERENCES ActivityGroup(ID) ON DELETE CASCADE
);

-- USER INTERESTS TABLE (user ↔ category)
CREATE TABLE UserInterest (
    UserID INTEGER,
    CategoryID INTEGER,
    PRIMARY KEY (UserID, CategoryID),
    FOREIGN KEY (UserID) REFERENCES User(ID) ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) REFERENCES Category(ID) ON DELETE CASCADE
);