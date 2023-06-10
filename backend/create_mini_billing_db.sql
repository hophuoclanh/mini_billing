create database mini_billing;

CREATE TABLE `mini_billing`.`user` (
  `user_id` VARCHAR(45) NOT NULL,
  `user_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `password` VARCHAR(72) NOT NULL,
  PRIMARY KEY (`user_id`)
);


CREATE TABLE `mini_billing`.`position` (
  `position_id` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`position_id`)
);
  

CREATE TABLE `mini_billing`.`permission` (
  `permission_id` VARCHAR(45) NOT NULL,
  `action` VARCHAR(10) NOT NULL,
  `resource` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`permission_id`)
);

CREATE TABLE `mini_billing`.`user_position` (
	`user_position_id` VARCHAR(45) NOT NULL,
    
	`user_id` VARCHAR(45) NOT NULL,
	`position_id` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`user_position_id`),
	FOREIGN KEY(`position_id`) REFERENCES `position` (`position_id`),
	FOREIGN KEY(`user_id`) REFERENCES `user` (`user_id`)
);


CREATE TABLE `mini_billing`.`position_permission` (
	`position_permission_id` VARCHAR(45) NOT NULL,
    
	`position_id` VARCHAR(45) NOT NULL,
	`permission_id` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`position_permission_id`),
	FOREIGN KEY(`position_id`) REFERENCES `position` (`position_id`),
	FOREIGN KEY(`permission_id`) REFERENCES `permission` (`permission_id`)
);

  
CREATE TABLE `mini_billing`.`order` (
	`order_id` VARCHAR(45) NOT NULL,
	`date` TIMESTAMP NOT NULL,
  	`total_amount` FLOAT NOT NULL,
    
	`user_id` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`order_id`),
	FOREIGN KEY(`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `mini_billing`.`category` (
	`category_id` VARCHAR(45) NOT NULL,
	`category_name` VARCHAR(45) NOT NULL,
	PRIMARY KEY(`category_id`)
);


CREATE TABLE `mini_billing`.`product`  (
	`product_id` VARCHAR(45) NOT NULL,
	`product_name` VARCHAR(45) NOT NULL,
	`descriptions` VARCHAR(255) NOT NULL,
	`unit_price` FLOAT NOT NULL,
	`unit_in_stock` INT NOT NULL,
    
	`category_id` VARCHAR(45) NOT NULL,
	PRIMARY KEY(`product_id`),
	FOREIGN KEY(`category_id`) REFERENCES category (`category_id`)
);


CREATE TABLE `mini_billing`.`order_detail`(
	`order_detail_id` varchar(45) NOT NULL,
	`quantity` INT NOT NULL,
  	`price_per_unit` FLOAT NOT NULL,
  	`total_amount_per_product` FLOAT NOT NULL,
    
	`order_id` varchar(45) NOT NULL,
	`product_id` varchar(45) NOT NULL,
	PRIMARY KEY (`order_detail_id`),
	FOREIGN KEY(`order_id`) REFERENCES `order` (`order_id`),
	FOREIGN KEY(`product_id`) REFERENCES `product` (`product_id`)
);








