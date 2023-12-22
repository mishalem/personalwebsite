CREATE TABLE IF NOT EXISTS `transactions` (
`transaction_id`            int(11)  	   NOT NULL auto_increment	        COMMENT 'the id of this transaction',
`cost`                      int(11)        NOT NULL                         COMMENT 'the cost of the nft;',
`seller`                    varchar(100) NOT NULL            		        COMMENT 'the selers email',
`buyer`                     varchar(100) NOT NULL                           COMMENT 'the buyers email',
`owner`                     varchar(100)  NOT NULL                          COMMENT 'the owner of the nft',
`nft_id`                    int(11) NOT NULL                                COMMENT 'the token',
`date`                      varchar(100)  NOT NULL                          COMMENT 'the date of the transaction',
PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site transaction information";
