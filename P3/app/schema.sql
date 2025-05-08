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
    College TEXT CHECK ((Affiliation = 'resident' AND College IS NULL) OR
        (Affiliation != 'resident' AND College IN ('Boston University', 'Northeastern University', 'Harvard University', 'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University', 'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston', 'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design')))
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
	ContactUserID INTEGER REFERENCES User(ID) ON DELETE SET NULL,
    Email TEXT REFERENCES User(Email) ON DELETE SET NULL,
    Address TEXT,
    CategoryID INTEGER,
    AffiliatedWithCollege BOOLEAN,
    College TEXT CHECK ((AffiliatedWithCollege = TRUE AND College IN ('Boston University', 'Northeastern University', 'Harvard University', 'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University', 'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston', 'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design')) 
OR (AffiliatedWithCollege = FALSE AND College IS NULL)),
    RequiresDues BOOLEAN,
    SkillLevel TEXT CHECK (SkillLevel IN ('beginner', 'intermediate', 'advanced')),
    FOREIGN KEY (CategoryID) REFERENCES Category(ID) ON DELETE SET NULL
);

CREATE TABLE Event (
    EventID INTEGER PRIMARY KEY,
    GroupID INTEGER NOT NULL REFERENCES ActivityGroup(ID) ON DELETE CASCADE,
    Name TEXT NOT NULL,
    Location TEXT,
    Description TEXT,
    Date DATE NOT NULL,
    StartTime TIME,
    EndTime TIME,
    Frequency TEXT
);

-- MEMBERSHIP TABLE (user ↔ activity group, includes role + join date)
CREATE TABLE Membership (
    Role TEXT CHECK (Role IN ('member', 'organizer')),
    JoinDate DATE,
    UserID INTEGER REFERENCES User(ID) ON DELETE CASCADE,
    GroupID INTEGER REFERENCES ActivityGroup(ID) ON DELETE CASCADE,
	PRIMARY KEY (UserID, GroupID)
);

-- USER INTERESTS TABLE (user ↔ category)
CREATE TABLE UserInterest (
    UserID INTEGER REFERENCES User(ID) ON DELETE CASCADE,
    CategoryID INTEGER REFERENCES Category(ID) ON DELETE CASCADE,
	PRIMARY KEY (UserID, CategoryID)
);
