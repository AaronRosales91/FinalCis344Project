CREATE DATABASE restaurant_reservations;

USE restaurant_reservations;

CREATE TABLE customers (
    customerId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerName VARCHAR(45) NOT NULL,
    contactInfo VARCHAR(200),
    PRIMARY KEY (customerId)
);

CREATE TABLE reservations (
    reservationId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerId INT NOT NULL,
    reservationTime DATETIME NOT NULL,
    numberOfGuests INT NOT NULL,
    specialRequests VARCHAR(200),
    PRIMARY KEY (reservationId),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);

CREATE TABLE diningpreferences (
    preferenceId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerId INT NOT NULL,
    favoriteTable VARCHAR(45),
    dietaryRestrictions VARCHAR(200),
    PRIMARY KEY (preferenceId),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);

DELIMITER $$
CREATE PROCEDURE findReservations(IN customerId INT)
BEGIN
    SELECT * FROM Reservations WHERE customerId = customerId;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE addSpecialRequest(IN reservationId INT, IN requests VARCHAR(200))
BEGIN
    UPDATE Reservations SET specialRequests = requests WHERE reservationId = reservationId;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE addReservation(IN customerName VARCHAR(45), IN contactInfo VARCHAR(200), IN reservationTime DATETIME, IN numberOfGuests INT, IN specialRequests VARCHAR(200))
BEGIN
    DECLARE cid INT;

    SELECT customerId INTO cid FROM Customers WHERE customerName = customerName AND contactInfo = contactInfo;

    IF cid IS NULL THEN
        INSERT INTO Customers (customerName, contactInfo) VALUES (customerName, contactInfo);
        SET cid = LAST_INSERT_ID();
    END IF;

    INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (cid, reservationTime, numberOfGuests, specialRequests);
END$$
DELIMITER ;

INSERT INTO Customers (customerName, contactInfo) VALUES
('John Doe', 'john.doe@example.com'),
('Jane Smith', 'jane.smith@example.com'),
('Michael Johnson', 'michael.johnson@example.com');

INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES
(1, '2024-05-15 19:00:00', 4, 'Window seat preferred'),
(2, '2024-05-16 18:30:00', 2, NULL),
(3, '2024-05-17 20:00:00', 6, 'Vegetarian meal required');

INSERT INTO DiningPreferences (customerId, favoriteTable, dietaryRestrictions) VALUES
(1, 'Table 5', 'None'),
(2, 'Table 3', 'Gluten-free'),
(3, 'Table 8', 'None');





