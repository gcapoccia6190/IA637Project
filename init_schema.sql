CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100),
    Username VARCHAR(50) UNIQUE,
    PasswordHash VARCHAR(255),
    Email VARCHAR(100),
    Role ENUM('admin', 'reader') DEFAULT 'reader'
);

CREATE TABLE Book (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    ISBN VARCHAR(20) UNIQUE,
    Genre VARCHAR(50),
    Status ENUM('active', 'inactive') DEFAULT 'inactive',
    EditionNumber INT,
    PublishYear YEAR
);

CREATE TABLE BookInteraction (
    InteractionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    BookID INT,
    InteractionType ENUM('Comment', 'Rating') NOT NULL,
    Content TEXT,
    Rating INT,
    Event VARCHAR(100),
    Date DATE,
    Time TIME,
    Location VARCHAR(100),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

CREATE TABLE BookConfirmation (
    ConfirmationID INT AUTO_INCREMENT PRIMARY KEY,
    BookID INT,
    UserID INT,
    ConfirmationDate DATE DEFAULT CURRENT_DATE,
    Notes TEXT,
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- BOOKCONFIRMATION TABLE
CREATE TABLE BookConfirmation (
    ConfirmationID INT AUTO_INCREMENT PRIMARY KEY,
    BookID INT NOT NULL,
    UserID INT NOT NULL,
    ConfirmationDate DATE,
    Notes TEXT,
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);


-- Admin user
INSERT INTO User (FullName, Username, PasswordHash, Email, Role)
VALUES (
    'Test Admin',
    'admin',
    '$2b$12$7H1wT9OSacx1kfM9onx7EOBM75V.QdlfNHm/TMStIECSO7GqTnRmK',  -- 'admin123'
    'admin@example.com',
    'admin'
);
-- Regular user
INSERT INTO User (FullName, Username, PasswordHash, Email, Role)
VALUES (
    'Regular User',
    'user1',
    '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG',  -- 'userpass1'
    'user1@example.com',
    'reader'
);
-- Admin
INSERT INTO User (FullName, Username, PasswordHash, Email, Role)
VALUES ('Second Admin', 'admin2', '$2b$12$7H1wT9OSacx1kfM9onx7EOBM75V.QdlfNHm/TMStIECSO7GqTnRmK', 'admin2@example.com', 'admin');
-- Regular Users
INSERT INTO User (FullName, Username, PasswordHash, Email, Role)
VALUES 
('Alice Reader', 'alice', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'alice@example.com', 'reader'),
('Bob Reader', 'bob', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'bob@example.com', 'reader');
-- More Regular Users
INSERT INTO User (FullName, Username, PasswordHash, Email, Role) VALUES
('Charlie Reader', 'charlie', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'charlie@example.com', 'reader'),
('Dana Reviewer', 'dana', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'dana@example.com', 'reader'),
('Eli Bookworm', 'eli', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'eli@example.com', 'reader'),
('Fay Follower', 'fay', '$2b$12$GtRbN33fZP0INRXMfCqzVeV1lP1bF9DoycVjDTEXmVJ4R3oRjKYUbG', 'fay@example.com', 'reader');


INSERT INTO Book (Title, Author, ISBN, Genre, Status, EditionNumber, PublishYear)
VALUES
('Test Book 1', 'Jane Doe', '1234567890', 'Sci-Fi', 'inactive', 1, 2020),
('Test Book 2', 'John Smith', '9876543210', 'Mystery', 'active', 2, 2022);
INSERT INTO Book (Title, Author, ISBN, Genre, Status, EditionNumber, PublishYear)
VALUES 
('Quantum Computing 101', 'Dr. Qubit', '0001112223', 'Science', 'inactive', 1, 2023),
('Hidden History', 'L. Archive', '1112223334', 'History', 'active', 2, 2018),
('Dreams of Mars', 'A. Nova', '2223334445', 'Sci-Fi', 'inactive', 1, 2020),
('Cooking for Coders', 'Chef Stack', '3334445556', 'Non-Fiction', 'active', 1, 2021),
('Poems of the Sea', 'W. Wave', '4445556667', 'Poetry', 'inactive', 3, 2019);
INSERT INTO Book (Title, Author, ISBN, Genre, Status, EditionNumber, PublishYear) VALUES
('AI for Humans', 'Tech Bro', '5556667778', 'Technology', 'inactive', 1, 2024),
('Gardening the Moon', 'Green Thumb', '6667778889', 'Non-Fiction', 'inactive', 2, 2022),
('Battle of Syntax', 'Code Lord', '7778889990', 'Fantasy', 'active', 1, 2019),
('Haiku Highway', 'Zen Poet', '8889990001', 'Poetry', 'inactive', 1, 2020),
('Beneath the Stars', 'Luna Sky', '9990001112', 'Romance', 'active', 3, 2018),
('The Lost Algorithms', 'Algo Smith', '1112223339', 'Tech Fiction', 'inactive', 1, 2023),
('Biology of Belief', 'Cell Sage', '2223334446', 'Science', 'active', 1, 2017),
('Tales of Tenacity', 'Grit Strong', '3334445557', 'Biography', 'inactive', 2, 2016),
('Deep Dive SQL', 'Query Queen', '4445556668', 'Education', 'active', 1, 2021),
('Mindful Machines', 'Neural Net', '5556667779', 'AI/Philosophy', 'inactive', 1, 2025);




INSERT INTO BookInteraction (UserID, BookID, InteractionType, Content, Rating, Event, Date, Time, Location)
VALUES
(2, 1, 'Comment', 'Interesting book!', NULL, NULL, '2025-04-20', '10:30:00', 'Online'),
(2, 2, 'Rating', NULL, 5, NULL, '2025-04-20', '11:00:00', 'Library');
INSERT INTO BookInteraction (UserID, BookID, InteractionType, Content, Rating, Event, Date, Time, Location)
VALUES 
(2, 1, 'Comment', 'Interesting concept.', NULL, NULL, '2025-04-21', '14:00:00', 'Online'),
(3, 1, 'Rating', NULL, 4, NULL, '2025-04-21', '15:15:00', 'Library'),
(4, 2, 'Comment', 'Very detailed history.', NULL, NULL, '2025-04-22', '13:10:00', 'Museum Archive'),
(2, 3, 'Comment', 'Too futuristic for my taste.', NULL, NULL, '2025-04-23', '10:00:00', 'Online'),
(4, 5, 'Rating', NULL, 5, NULL, '2025-04-24', '11:30:00', 'Beachside');
INSERT INTO BookInteraction (UserID, BookID, InteractionType, Content, Rating, Event, Date, Time, Location) VALUES
(2, 6, 'Comment', 'Loved the chapter on ethics.', NULL, NULL, '2025-04-22', '10:00:00', 'Online'),
(3, 6, 'Rating', NULL, 4, NULL, '2025-04-22', '11:00:00', 'Library'),
(4, 7, 'Comment', 'Very practical.', NULL, NULL, '2025-04-22', '12:00:00', 'Cafe'),
(5, 8, 'Comment', 'Poems were okay.', NULL, NULL, '2025-04-22', '13:00:00', 'Home'),
(6, 9, 'Rating', NULL, 5, NULL, '2025-04-23', '14:00:00', 'Campus'),
(7, 10, 'Comment', 'Very dreamy writing.', NULL, NULL, '2025-04-23', '15:00:00', 'Bookstore'),
(3, 11, 'Rating', NULL, 3, NULL, '2025-04-23', '16:00:00', 'Classroom'),
(4, 12, 'Comment', 'Complicated topic but cool.', NULL, NULL, '2025-04-23', '17:00:00', 'Zoom'),
(5, 13, 'Rating', NULL, 4, NULL, '2025-04-24', '18:00:00', 'Park'),
(6, 14, 'Comment', 'Got emotional reading it.', NULL, NULL, '2025-04-24', '19:00:00', 'Porch'),
(7, 15, 'Rating', NULL, 5, NULL, '2025-04-24', '20:00:00', 'Deck');




INSERT INTO BookConfirmation (BookID, UserID, ConfirmationDate, Notes)
VALUES
(1, 2, '2025-04-20', 'I confirm this book is valid');
INSERT INTO BookConfirmation (BookID, UserID, ConfirmationDate, Notes)
VALUES 
(1, 2, '2025-04-21', 'Looks legit.'),
(1, 3, '2025-04-22', 'Useful for new learners.'),
(3, 2, '2025-04-23', 'Sounds exciting.'),
(5, 3, '2025-04-23', 'Lovely title.'),
(5, 4, '2025-04-24', 'Should be included.');
INSERT INTO BookConfirmation (BookID, UserID, ConfirmationDate, Notes) VALUES
(6, 2, '2025-04-20', 'Important subject'),
(6, 3, '2025-04-21', 'Should be included'),
(6, 4, '2025-04-22', 'Useful in tech courses'),
(7, 2, '2025-04-20', 'Interesting concept'),
(8, 3, '2025-04-21', 'Love the writing'),
(9, 5, '2025-04-22', 'Great poems'),
(10, 2, '2025-04-23', 'Very romantic'),
(10, 3, '2025-04-23', 'Popular in book clubs'),
(11, 4, '2025-04-24', 'Nice plot twist'),
(11, 5, '2025-04-24', 'Could be published soon'),
(12, 2, '2025-04-24', 'Too philosophical'),
(12, 3, '2025-04-24', 'Loved the idea'),
(13, 4, '2025-04-24', 'Highly recommended'),
(13, 5, '2025-04-24', 'Would recommend to students'),
(14, 6, '2025-04-24', 'Personal favorite'),
(15, 7, '2025-04-24', 'Poetic and insightful');


