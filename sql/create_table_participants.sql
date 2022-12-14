DROP TABLE IF EXISTS PARTICIPANTS;

CREATE TABLE IF NOT EXISTS PARTICIPANTS (
    participant_id      INT             AUTO_INCREMENT,
    summons_date        DATE            NOT NULL,
    undeliverable       TINYINT(1),
    perm_disq           TINYINT(1),
    last_name           VARCHAR(31)     NOT NULL,
    suffix              VARCHAR(31),
    first_name          VARCHAR(31)     NOT NULL,
    middle_name         VARCHAR(31),
    address             VARCHAR(127)    NOT NULL,
    city                VARCHAR(31)     NOT NULL,
    state               CHAR(2)         NOT NULL,
    zip                 VARCHAR(15)     NOT NULL,
    county              VARCHAR(31)     NOT NULL,
    dob                 VARCHAR(15)     NOT NULL,
    drivers_state       CHAR(2),
    voters_no           VARCHAR(31),
    ssn                 CHAR(9)         NOT NULL,
    race                VARCHAR(31),
    mvc_id              VARCHAR(31),
    gender              VARCHAR(31),
    hispanic            TINYINT(1),
    home_phone          VARCHAR(15),
    mobile_phone        VARCHAR(15),
    work_phone          VARCHAR(15),
    work_phone_ext      VARCHAR(15),
    email               VARCHAR(63),
    gov_employee        TINYINT(1),
    create_user_id      VARCHAR(31),
    create_datetime     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    maint_datetime      DATETIME        DEFAULT CURRENT_TIMESTAMP 
                                        ON UPDATE CURRENT_TIMESTAMP,
    maint_user_id       VARCHAR(31),
    perm_disq_reason    VARCHAR(255),
    opt_in              TINYINT(1),
    unique_id           VARCHAR(31),
    employer            VARCHAR(255),
    occupation          VARCHAR(255),
    occupation_other    VARCHAR(255),
    PRIMARY KEY (participant_id)
);
