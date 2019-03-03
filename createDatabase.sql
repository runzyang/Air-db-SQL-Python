
DROP TABLE IF EXISTS `Segment`;
DROP TABLE IF EXISTS `Flight`;
DROP TABLE IF EXISTS `Airplane`;
DROP TABLE IF EXISTS `AirlineCompany`;
DROP TABLE IF EXISTS `Airport`;
DROP TABLE IF EXISTS `FlightTicket`;
DROP TABLE IF EXISTS `Customer`;

CREATE TABLE Customer(
	ID 								BIGINT UNSIGNED 		NOT NULL				AUTO_INCREMENT,
	Password					VARCHAR(12) 				NOT NULL,
	firstName 					VARCHAR(15) 				NOT NULL,
	lastName 					VARCHAR(15) 				NOT NULL,
	birthday 						DATE,
	Country 						VARCHAR(3),
	Address		 				VARCHAR(100),
	ZIPcode 						INTEGER (10),
	Tele 							INTEGER 						Default NULL,
	Email 							VARCHAR(50)				NOT NULL     			UNIQUE,
    membership				INT 									NOT NULL 				DEFAULT 0,
    mileage 						BIGINT UNSIGNED		DEFAULT 0,	
	PRIMARY KEY(ID)
);

CREATE TABLE FlightTicket(
	TicketCode					VARCHAR(7)					NOT NULL				UNIQUE,
    passangerFirstName	VARCHAR(15) 				NOT NULL,
    passangerLastName	VARCHAR(15) 				NOT NULL,
	CustomerID     			BIGINT UNSIGNED,
	SegCount					INT									NOT NULL,
	Price							DOUBLE UNSIGNED		NOT NULL,
    passport						VARCHAR(10)				NOT NULL,
    ticketInfo						VARCHAR(300)				NOT NULL, # 10 Entries At Most // segment info included
	PRIMARY KEY(TicketCode),
	FOREIGN KEY(CustomerID) REFERENCES Customer(ID) ON DELETE SET NULL ON UPDATE CASCADE
    
);

CREATE TABLE Airport(	
	Name							VARCHAR(100)				NOT NULL,
	Code 							VARCHAR(3)					NOT NULL,
	City								VARCHAR(30),
	Country						VARCHAR(30),
	PRIMARY KEY(Code)
);

CREATE TABLE AirlineCompany(
	CompanyCode		VARCHAR(2)						NOT NULL,
    CompanyName		VARCHAR(50)					NOT NULL,
    Region						VARCHAR(20)					NOT NULL,
    PRIMARY KEY(CompanyCode)
);


CREATE TABLE Airplane(
	Company						VARCHAR(10)				NOT NULL,
	Model							VARCHAR(10)				NOT NULL,

	#First Class Seats
	FSeatNum					INT UNSIGNED				NOT NULL,
	FStartRow					INT UNSIGNED				NOT NULL,
	FEndRow					INT UNSIGNED				NOT NULL,

	#Business Class Seats
	BSeatNum  					INT UNSIGNED				NOT NULL,
	BStartRow					INT UNSIGNED				NOT NULL,
	BEndRow					INT UNSIGNED				NOT NULL,

	#Premium Economy Class Seats
	PSeatNum  					INT UNSIGNED				NOT NULL,
	PStartRow					INT UNSIGNED				NOT NULL,
	PEndRow					INT UNSIGNED				NOT NULL,

	#Economy Class Seats
	ESeatNum  					INT UNSIGNED				NOT NULL,
	EStartRow					INT UNSIGNED				NOT NULL,
	EEndRow					INT UNSIGNED				NOT NULL,

	PRIMARY KEY(Model)
);


CREATE TABLE Flight (	
	FlightNum					INT UNSIGNED				NOT NULL,
    FlightCompany			VARCHAR(2)					NOT NULL,
	Origin							VARCHAR(3)					NOT NULL,
	Destination					VARCHAR(3)					NOT NULL,
	TakeOffAt					TIME								NOT NULL,
	ArriveAt						TIME								NOT NULL,
    FlightTime					TIME								NOT NULL,
	CraftCompany				VARCHAR(10)				NOT NULL,
	Airplane           			VARCHAR(10)				NOT NULL,
    
	PRIMARY KEY(FlightNum, FlightCompany),
	FOREIGN KEY(Origin) REFERENCES Airport(Code) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(Destination) REFERENCES Airport(Code) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(FlightCompany) REFERENCES AirlineCompany(CompanyCode) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(Airplane) REFERENCES Airplane(Model) ON DELETE CASCADE ON UPDATE CASCADE
    
);

CREATE TABLE Segment(
	TicketCode		VARCHAR(7)				NOT NULL,
	Segment			INT								NOT NULL,
	FlightNum		INT UNSIGNED			NOT NULL,
    FlightCom		VARCHAR(2)				NOT NULL,
	FlightDate		DATETIME					NOT NULL,
	ClassCode		VARCHAR(1)				NOT NULL,
	Seat					VARCHAR(3)				NOT NULL,
	PRIMARY KEY(TicketCode, Segment),
	FOREIGN KEY(FlightNum) REFERENCES Flight(FlightNum) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY(FlightCom) REFERENCES Flight(FlightCompany) ON DELETE NO ACTION ON UPDATE CASCADE,
	FOREIGN KEY(TicketCode) REFERENCES FlightTicket(TicketCode) ON DELETE CASCADE ON UPDATE CASCADE

);









