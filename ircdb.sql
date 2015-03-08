DROP DATABASE IF EXISTS ircdb;
CREATE DATABASE ircdb;
\c ircdb;
CREATE EXTENSION pgcrypto;
-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE IF NOT EXISTS messages (
  id serial,
  username varchar(12) NOT NULL,
  text varchar(70) NOT NULL,
  messagetime timestamp NOT NULL,
  PRIMARY KEY (id)
) ;

--
-- Dumping data for table `messages`
--

INSERT INTO messages (username, text, messagetime) VALUES
('elvis', 'hello world', '2014-01-22 09:06:44'),
('ann', 'anyone here', '2014-01-21 02:02:02');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS users (
  id serial,
  username varchar(12) NOT NULL,
  password varchar(126) NOT NULL,
  PRIMARY KEY (id)
)  ;

--
-- Dumping data for table `users`
--

INSERT INTO users (username, password) VALUES
('raz', 'p00d13'),
('ann', 'changeme'),
('lazy', 'qwerty'),
('elvis', 'elvis');