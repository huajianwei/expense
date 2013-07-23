CREATE TABLE `expense`
(
  gid integer primary key,
  time timestamp,
  direction integer,
  amount float default 0.0,
  remain float default 0.0,
  who integer,
  reason text,
  remark text
);

CREATE TABLE `money`
(
    money float default 0.0
);
INSERT INTO money VALUES (0);
