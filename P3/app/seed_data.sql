INSERT INTO User (ID, Name, Email, Affiliation, College) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com', 'Student', 'Boston University'),
(2, 'Bob Smith', 'bob.smith@example.com', 'Alumnus', 'Northeastern University'),
(3, 'Carol White', 'carol.white@example.com', 'Resident', NULL),
(4, 'David Lee', 'david.lee@example.com', 'Student', 'Harvard University'),
(5, 'Emily Chen', 'emily.chen@example.com', 'Alumnus', 'Massachusetts Institute of Technology'),
(6, 'Frank Nguyen', 'frank.nguyen@example.com', 'Resident', NULL),
(7, 'Grace Kim', 'grace.kim@example.com', 'Student', 'Suffolk University'),
(8, 'Henry Zhao', 'henry.zhao@example.com', 'Student', 'Tufts University'),
(9, 'Isabel Torres', 'isabel.torres@example.com', 'Alumnus', 'Boston College'),
(10, 'Jake Martin', 'jake.martin@example.com', 'Resident', NULL),
(11, 'Kelly Brooks', 'kelly.brooks@example.com', 'Student', 'Lesley University'),
(12, 'Leo Patel', 'leo.patel@example.com', 'Alumnus', 'Emerson College'),
(13, 'Maria Gonzalez', 'maria.gonzalez@example.com', 'Student', 'Berklee College of Music'),
(14, 'Nina Rossi', 'nina.rossi@example.com', 'Alumnus', 'Massachusetts College of Art and Design'),
(15, 'Oscar Rivera', 'oscar.rivera@example.com', 'Resident', NULL);

INSERT INTO Category (ID, Name, Description) VALUES
(1, 'Sports', 'Athletic and recreational activities'),
(2, 'Music', 'Musical performance and appreciation groups'),
(3, 'Technology', 'Clubs focused on programming, robotics, and innovation'),
(4, 'Volunteering', 'Community service and volunteering opportunities'),
(5, 'Art', 'Visual and performing arts groups'),
(6, 'Cooking', 'Culinary groups and cooking clubs'),
(7, 'Outdoors', 'Outdoor recreation and nature activities');

INSERT INTO ActivityGroup (ID, Name, Description, Website, ContactUserID, Email, Address, CategoryID, AffiliatedWithCollege, College, RequiresDues, SkillLevel) VALUES
(1, 'Boston Runners', 'A running club for all levels', 'http://bostonrunners.org', 1, 'alice.johnson@example.com', '123 Boylston St, Boston, MA', 1, TRUE, 'Boston University', TRUE, 'Intermediate'),
(2, 'Tech Innovators', 'A club for technology enthusiasts', 'http://techinnovators.com', 2, 'bob.smith@example.com', '456 Massachusetts Ave, Boston, MA', 3, TRUE, 'Northeastern University', FALSE, 'Advanced'),
(3, 'Boston Volunteers', 'Volunteer work across the city', 'http://bostonvolunteers.org', 3, 'carol.white@example.com', '789 Commonwealth Ave, Boston, MA', 4, FALSE, NULL, FALSE, 'Beginner'),
(4, 'Boston Jazz Band', 'Local jazz music group', 'http://bostonjazz.org', 4, 'david.lee@example.com', '321 Huntington Ave, Boston, MA', 2, TRUE, 'Harvard University', TRUE, 'Advanced'),
(5, 'Outdoor Explorers', 'Hiking and nature trips around Boston', 'http://outdoorexplorers.org', 5, 'emily.chen@example.com', '555 Beacon St, Boston, MA', 7, FALSE, NULL, FALSE, 'Intermediate'),
(6, 'Culinary Collective', 'Cooking classes and recipe sharing', 'http://culinarycollective.com', 6, 'frank.nguyen@example.com', '12 Tremont St, Boston, MA', 6, FALSE, NULL, TRUE, 'Beginner'),
(7, 'Boston Artists', 'Collaborative art projects and workshops', 'http://bostonartists.org', 7, 'grace.kim@example.com', '78 Newbury St, Boston, MA', 5, TRUE, 'Suffolk University', TRUE, 'Intermediate'),
(8, 'CodeCraft', 'Coding bootcamps and hackathons', 'http://codecraft.org', 8, 'henry.zhao@example.com', '246 Albany St, Boston, MA', 3, TRUE, 'Tufts University', FALSE, 'Advanced'),
(9, 'Symphony Society', 'Classical music appreciation and performance', 'http://symphonysociety.org', 9, 'isabel.torres@example.com', '111 Huntington Ave, Boston, MA', 2, TRUE, 'Boston College', TRUE, 'Advanced'),
(10, 'Volunteer Heroes', 'Helping underserved communities', 'http://volunteerheroes.org', 10, 'jake.martin@example.com', '333 Washington St, Boston, MA', 4, FALSE, NULL, FALSE, 'Beginner');

INSERT INTO Event (EventID, GroupID, Name, Location, Description, Date, StartTime, EndTime, Frequency) VALUES
(1, 1, 'Weekly Long Run', 'Boston Common', 'Sunday morning long run', '2025-05-11', '08:00', '10:30', 'Weekly'),
(2, 2, 'Hackathon', 'MIT Media Lab', '24-hour coding event', '2025-06-01', '10:00', '10:00', 'Annual'),
(3, 3, 'Community Cleanup', 'Charles River Esplanade', 'Help clean up the riverbank', '2025-05-15', '09:00', '12:00', 'Monthly'),
(4, 4, 'Jazz Night', 'Scullers Jazz Club', 'Evening jazz performance', '2025-05-20', '19:00', '22:00', 'Monthly'),
(5, 5, 'Spring Hike', 'Blue Hills Reservation', 'Group hike to enjoy nature', '2025-05-22', '09:00', '15:00', 'Quarterly'),
(6, 6, 'Cooking Workshop', 'Boston Public Market', 'Learn to make pasta', '2025-06-10', '17:00', '19:00', 'Monthly'),
(7, 7, 'Gallery Showcase', 'ICA Boston', 'Showcase of member artwork', '2025-06-18', '18:00', '21:00', 'Quarterly'),
(8, 8, 'Python Bootcamp', 'Tufts Computer Lab', 'Two-day intensive Python course', '2025-07-01', '09:00', '17:00', 'Semiannual'),
(9, 9, 'Chamber Concert', 'Jordan Hall', 'Evening chamber music concert', '2025-07-15', '19:30', '21:30', 'Annual'),
(10, 10, 'Food Drive', 'Boston Food Bank', 'Volunteer to collect and sort donations', '2025-05-30', '10:00', '14:00', 'Monthly');

INSERT INTO Membership (Role, JoinDate, UserID, GroupID) VALUES
('Member', '2025-01-10', 1, 1),
('Organizer', '2024-09-05', 2, 2),
('Member', '2025-03-15', 3, 3),
('Organizer', '2023-12-01', 4, 4),
('Member', '2025-02-20', 5, 5),
('Member', '2025-04-05', 6, 6),
('Organizer', '2024-11-15', 7, 7),
('Member', '2025-01-25', 8, 8),
('Organizer', '2024-10-10', 9, 9),
('Member', '2025-03-30', 10, 10),
('Member', '2025-02-01', 11, 7),
('Member', '2025-03-10', 12, 2),
('Organizer', '2024-07-01', 13, 9),
('Member', '2025-02-18', 14, 5),
('Member', '2025-03-27', 15, 3);

INSERT INTO UserInterest (UserID, CategoryID) VALUES
(1, 1),
(1, 3),
(2, 3),
(3, 4),
(4, 2),
(5, 1),
(5, 3),
(6, 4),
(7, 5),
(8, 3),
(9, 2),
(10, 4),
(11, 5),
(12, 6),
(13, 2),
(14, 5),
(15, 4);