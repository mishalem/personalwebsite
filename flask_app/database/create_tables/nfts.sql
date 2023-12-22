CREATE TABLE IF NOT EXISTS `nfts` (
`nft_id`         int(11)  	   NOT NULL auto_increment	  COMMENT 'the id of this nft',
`description`     varchar(100)  NOT NULL                   COMMENT 'the description of the nft;',
`owner`           varchar(100) NOT NULL            		  COMMENT 'the owner email',
`token`        int(11) NOT NULL                   COMMENT 'the token',
`image`         BLOB  NOT NULL  COMMENT 'the image data of the nft',
`onMarket`       BOOLEAN NOT NULL                   COMMENT 'the token',
PRIMARY KEY (`nft_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site nft information";
