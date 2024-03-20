CREATE USER IF NOT EXISTS myaccount@'%' identified BY 'myaccount';
CREATE USER IF NOT EXISTS myaccount@localhost identified BY 'myaccount';
GRANT ALL PRIVILEGES ON *.* TO myaccount@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO myaccount@localhost WITH GRANT OPTION;

CREATE TABLE IF NOT EXISTS mst_users(
  user_id VARCHAR (32) NOT NULL,
  user_name VARCHAR (32) NOT NULL,
  user_password VARCHAR (256) NOT NULL,
  is_admin INT (11) NOT NULL DEFAULT 0,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id)
)
;

CREATE TABLE IF NOT EXISTS trn_keijiban(
  keijiban_id INT (11) NOT NULL auto_increment,
  keijiban_subject VARCHAR(100) NOT NULL,
  user_id VARCHAR (32) NOT NULL,
  PRIMARY KEY (keijiban_id)
)
;
