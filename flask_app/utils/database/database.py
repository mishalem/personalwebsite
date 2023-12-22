import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow
import base64
import datetime

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    """
    Creates SQL tables for the database, Calls insert rows to populate tables
    :param data_path: path to data folder
    :param purge: if True, deletes all rows in tables before inserting new rows
    :return: None
     """
    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print('I create and populate database tables.')
        # in case i need to clear sql tables.
        # self.query("DELETE FROM skills;")
        # self.query("DELETE FROM experiences;")
        # self.query("DELETE FROM positions;")
        # self.query("DELETE FROM institutions;")

        #self.query("DROP TABLE IF EXISTS `nfts`;")
        file_list = ["institutions.sql", "positions.sql", "experiences.sql", "skills.sql", "feedback.sql", "users.sql", "nfts.sql", "transactions.sql"] 
        for file in file_list:
            path = data_path+"create_tables/" + file
            with open(path, "r") as file:
                sql = file.read()
                sql.strip()
                return_value = self.query(sql)
                file.close()
        
             
            
        csv_files =["institutions.csv", "positions.csv", "experiences.csv", "skills.csv", "nfts.csv"]
        for file_name in csv_files:
            path = data_path+"initial_data/" + file_name
            file = open(path)
            csv_reader = csv.reader(file)
            lines = next(csv_reader)
            for row in csv_reader:  
                        random = 'somerandome'
                        self.insertRows(file_name, random, row)
                

            
            
             
    """
    Inserts a row into a table from csv files
    :return: None
    """
    def insertRows(self, table='table', params=['x','y'], columns=[['v11','v12'],['v21','v22']]):
        print('I insert things into the database.')
        if (table == "experiences.csv"):
            experience_id = columns[0]
            position_id = columns[1]
            name = columns[2]
            description = columns[3]
            hyperlink = columns[4]
            start_date = columns[5]
            end_date = columns[6]
            my_str = "('"+experience_id+"', '"+position_id+"', '"+name+"', '"+description+"', '"+hyperlink+"', '"+start_date+"', '"+end_date+"')"
            self.query("INSERT IGNORE INTO `experiences` (`experience_id`, `position_id`, `name`, `description`, `hyperlink`, `start_date`, `end_date`) VALUES " + my_str)
        elif (table == "skills.csv"):
            skill_id = columns[0]
            experience_id = columns[1]
            name = columns[2]
            skill_level = columns[3]
            my_str = "('"+skill_id+"', '"+experience_id+"', '"+name+"', '"+skill_level+"')"
            self.query("INSERT IGNORE INTO `skills` (`skill_id`, `experience_id`, `name`, `skill_level`) VALUES " + my_str)
        elif (table == "institutions.csv"):
            inst_id = str(columns[0])
            type = str(columns[1])
            name = str(columns[2])
            department = str(columns[3])
            address = str(columns[4])
            city = str(columns[5])
            state = str(columns[6]) 
            zip = str(columns[7])
            my_str = "('"+inst_id+"', '"+type+"', '"+name+"', '"+department+"', '"+address+"', '"+city+"', '"+state+"', '"+zip+"')"
            self.query("INSERT IGNORE INTO `institutions` (`inst_id`, `type`, `name`, `department`, `address`, `city`, `state`, `zip`) VALUES " + my_str)
        elif (table == "positions.csv"):
            position_id = str(columns[0])
            inst_id = str(columns[1])
            title = str(columns[2])
            responsibilities = str(columns[3])
            start_date = str(columns[4])
            end_date = str(columns[5])
            my_str = "('"+position_id+"', '"+inst_id+"', '"+title+"', '"+responsibilities+"', '"+start_date+"', '"+end_date+"')"
            self.query("INSERT IGNORE INTO `positions` (`position_id`, `inst_id`, `title`, `responsibilities`, `start_date`, `end_date`) VALUES " + my_str)
        elif (table == "feedback.sql"):
            name = str(columns[0])
            email = str(columns[1])
            comment = str(columns[2])
            feedbakcs = self.query("SELECT * FROM feedback")
            comment_id = str(len(feedbakcs))
            my_str = "('"+comment_id+"', '"+name+"', '"+email+"', '"+comment+"')"
            self.query("INSERT IGNORE INTO `feedback` (`comment_id`, `name`, `email`, `comment`) VALUES " + my_str)
        elif (table == "nfts.csv"):
            nft_id = str(columns[0])
            description = str(columns[1])
            owner = str(columns[2])
            token = str(columns[3])
            my_str = 'flask_app/static/main/images/' + str(columns[4])
            with open(my_str, 'rb') as file:
                image_data = file.read()
            data = base64.b64encode(image_data)
            data = data.decode('utf-8')
            onMarket = str(columns[5])
            q = self.query("INSERT IGNORE INTO `nfts` (`nft_id`, `description`, `owner`, `token`, `image`, `onMarket`) VALUES (%s, %s, %s, %s, %s, %s)", (nft_id, description, owner, token, data, onMarket))

    """
    Get Resume's data
    :return: entire resume data
    """
    def getResumeData(self):
        data = {}
        institutions = self.query("SELECT * FROM institutions")
        positions = self.query("SELECT * FROM positions")
        experiences = self.query("SELECT * FROM experiences")
        skills = self.query("SELECT * FROM skills")
        for row in range(len(institutions)):
            my_dict = {}
            inst_id = institutions[row]["inst_id"]
            type = institutions[row]["type"]
            name = institutions[row]["name"]
            if institutions[row]["department"] == "NULL":
                department = ""
            else:
                department = institutions[row]["department"]
            if institutions[row]["address"] == "NULL":
                address = ""
            else:
                address = institutions[row]["address"]
            city = institutions[row]["city"]
            state = institutions[row]["state"] 
            zip = institutions[row]["zip"] 
            my_dict["type"] = type
            my_dict["name"] = name
            my_dict["department"] = department
            my_dict["address"] = address
            my_dict["city"] = city
            my_dict["state"] = state
            my_dict["zip"] = zip
            my_dict["positions"] = {}
            data[inst_id] = my_dict
            row += 1
        previous_id = 1
        new_dict = {}
        position_to_inst = {}
        exp_to_pos = {}
        for row in range(len(positions)):
            my_dict = {}
            position_id_pos = positions[row]["position_id"]
            inst_id = positions[row]["inst_id"]
            position_to_inst[position_id_pos] = inst_id

            title = positions[row]["title"]
            responsobilities = positions[row]["responsibilities"]
            start_date = positions[row]["start_date"]
            if positions[row]["end_date"] is None:
                end_date = "Current"
            else:
                end_date = positions[row]["end_date"]
            my_dict["title"] = title
            my_dict["responsobilities"] = responsobilities
            my_dict["start_date"] = start_date
            my_dict["end_date"] = end_date
            if previous_id != inst_id:
                data[previous_id]["positions"] = new_dict
                new_dict = {}
            if (row+1) >= len(positions):
                new_dict[position_id_pos] = my_dict
                data[inst_id]["positions"] = new_dict
            new_dict[position_id_pos] = my_dict
            previous_id = inst_id
            row += 1
        for row_2 in range(len(experiences)):
            my_dict_2 = {}
            experience_id = experiences[row_2]["experience_id"]
            position_id_exp = experiences[row_2]["position_id"]
            exp_to_pos[experience_id] = position_id_exp
            name = experiences[row_2]["name"]
            description = experiences[row_2]["description"]
            hyperlink = experiences[row_2]["hyperlink"]
            start_date = experiences[row_2]["start_date"]
            end_date = experiences[row_2]["end_date"]
            my_dict_2["position_id"] = position_id_exp
            my_dict_2["name"] = name
            my_dict_2["description"] = description
            my_dict_2["hyperlink"] = hyperlink
            my_dict_2["start_date"] = start_date
            my_dict_2["end_date"] = end_date
            new_dict_2 = {}
            new_dict_2[experience_id] = my_dict_2
            current_inst_id = position_to_inst[position_id_exp]
            if 'experiences' not in data[current_inst_id]["positions"][position_id_exp]:
                data[current_inst_id]["positions"][position_id_exp]["experiences"] = new_dict_2
            else:
                current_dict_val = data[current_inst_id]["positions"][position_id_exp]["experiences"]
                current_dict_val[experience_id] = my_dict_2
                data[current_inst_id]["positions"][position_id_exp]["experiences"] = current_dict_val 
            row_2 += 1


        for row in range(len(skills)):
            my_dict = {}
            skill_id = skills[row]["skill_id"]
            experience_id = skills[row]["experience_id"]
            name = skills[row]["name"]
            skill_level = skills[row]["skill_level"]
            my_dict["skill_id"] = skill_id
            my_dict["experience_id"] = experience_id
            my_dict["name"] = name
            my_dict["skill_level"] = skill_level
            new_dict = {}
            new_dict[skill_id] = my_dict

            position_id = exp_to_pos[experience_id]
            current_inst_id = position_to_inst[position_id]
            if 'skills' not in data[current_inst_id]["positions"][position_id]["experiences"][experience_id]:
                data[current_inst_id]["positions"][position_id]["experiences"][experience_id]['skills'] = new_dict
            else:
                current_dict_val = data[current_inst_id]["positions"][position_id]["experiences"][experience_id]['skills']
                current_dict_val[skill_id] = my_dict
                data[current_inst_id]["positions"][position_id]["experiences"][experience_id]['skills'] = current_dict_val 
            row+=1


        return data
    """
    Gets feedback data from databse
    :return: data from feedback table
        """
    def getFeedbackData(self):
        comments = self.query("SELECT * FROM feedback")
        data = {}
        for row in range(len(comments)):
            my_dict = {}
            name = comments[row]['name']
            email = comments[row]['email']
            comment = comments[row]['comment']
            comment_id = comments[row]['comment_id']
            my_dict['name'] = name
            my_dict['email'] = email
            my_dict['comment'] = comment
            data[comment_id] = my_dict
        return data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################

    """
    Creates a user in the database
    :param email: email of user
    :param password: password of user
    :param role: role of user
    :param balance: balance of user
    :return: None
    """
    def createUser(self, email='me@email.com', password='password', role='user', balance=100):
        #self.query("DELETE FROM users;")
        count = self.query("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        usersss = self.query("SELECT email FROM users;")
        if int(count[0]['COUNT(*)']) >= 1:
            return {"success" : 0}
        last_user_id = self.query("SELECT COUNT(*) FROM users")
        biggest_id = int(last_user_id[0]['COUNT(*)'])+1
        user_id = str(biggest_id)
        role = str(role)
        email = str(email)
        encrypted_password = self.onewayEncrypt(password)
        password = str(encrypted_password)
        balance = str(balance)
        q = self.query("INSERT IGNORE INTO `users` (`user_id`, `role`, `email`, `password`, `balance`) VALUES (%s, %s, %s, %s, %s)", (user_id, role, email, password, balance))


    """
    Authenticates a user in the database
    :param email: email of user
    :param password: password of user
    :return: 1 if user exists, 0 if user does not exist
    """
    def authenticate(self, email='me@email.com', password='password'):
        email_1 = self.query("SELECT COUNT(*) FROM users WHERE email = %s and password= %s", (email, self.onewayEncrypt(password)))
        users = self.query("SELECT * FROM users")
        if email_1[0]["COUNT(*)"]:
            return {"success" : 1}
        else:
            return {"success" : 0}


    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message
    """
    Updates instituiton data in database
    :param inst_id: id of institution
    :param name: name of institution
    :param department: department of institution
    :param address: address of institution
    :param city: city of institution
    :return: None
    """
    def update_institution(self, inst_id ,name, department, address, city):#, position_id, start_date, end_date, title):
        self.query("UPDATE institutions SET name = '" + name + "' WHERE inst_id = " + inst_id +";")
        self.query("UPDATE institutions SET department = '" + department + "' WHERE inst_id = " + inst_id +";")
        self.query("UPDATE institutions SET address = '" + address + "' WHERE inst_id = " + inst_id +";")
        self.query("UPDATE institutions SET city = '" + city + "' WHERE inst_id = " + inst_id +";")


    """
    Updates name data in database
    :param inst_id: id of institution
    :param name: name of institution
    :return: None
    """
    def update_name(self, inst_id ,name):
        self.query("UPDATE institutions SET name = '" + name + "' WHERE inst_id = " + inst_id +";")


    """
    Updates department data in database
    :param inst_id: id of institution
    :param department: department of institution
    :return: None
    """
    def update_department(self, inst_id ,department):
        self.query("UPDATE institutions SET department = '" + department + "' WHERE inst_id = " + inst_id +";")


    """
    Updates address data in database
    :param inst_id: id of institution
    :param address: adress of institution
    :return: None
    """
    def update_address(self, inst_id ,address):
        self.query("UPDATE institutions SET address = '" + address + "' WHERE inst_id = " + inst_id +";")


    """
    Updates name data in database
    :param inst_id: id of institution
    :param name: name of institution
    :return: None
    """
    def update_city(self, inst_id ,city):
        self.query("UPDATE institutions SET city = '" + city + "' WHERE inst_id = " + inst_id +";")


    """
    Updates name data in database
    :param inst_id: id of institution
    :param name: name of institution
    :return: None
    """
    def update_title(self, pos_id ,title):
        self.query("UPDATE positions SET title = '" + title + "' WHERE position_id = " + pos_id +";")



    """
    Updates start_date data in database
    :param pos_id: id of position
    :param start_date: start date of position
    :return: None
    """
    def update_start_date(self, pos_id ,start_date):
        self.query("UPDATE positions SET start_date = '" + start_date + "' WHERE position_id = " + pos_id +";")


    """
    Updates end_date data in database
    :param pos_id: id of position
    :param end_date: end_date of position
    :return: None
    """
    def update_end_date(self, pos_id ,end_date):
        if end_date == "Current":
            self.query("UPDATE positions SET end_date = NULL WHERE position_id = " + pos_id +";")
        else:
            self.query("UPDATE positions SET end_date = '" + end_date + "' WHERE position_id = " + pos_id +";")


    """
    Updates skill data in database
    :param inst_id: id of skill
    :param name: name of skill
    :return: None
    """
    def update_skills(self, skill_id ,name):
        self.query("UPDATE skills SET name = '" + name + "' WHERE skill_id = " + skill_id +";")



    """
    Updates name of the xpreiencedata in database
    :param exp_id: id of experience
    :param expname: name of experience
    :return: None
    """
    def update_expname(self, exp_id ,expname):
        self.query("UPDATE experiences SET name = '" + expname + "' WHERE experience_id = " + exp_id +";")


    """
    Updates description of an experience data in database
    :param exp_id: id of experience
    :param description: description of experience
    :return: None
    """
    def update_description(self, exp_id ,description):
        self.query("UPDATE experiences SET description = '" + description + "' WHERE experience_id = " + exp_id +";")


    """
    Adds entry to database
    :param instituion: name of institution
    :param department: department of institution
    :param address: address of institution
    :param city: city of institution
    :param position: position of institution
    :param start_date: start date of position
    :param end_date: end date of position
    :param position_name: name of position
    :param position_description: description of position
    :param skill: skill of position
    :return: None
    """
    def add_entry(self, institution, department, address, city, position, start_date, end_date, position_name, position_description, skill):
        last_inst_id = self.query("SELECT COUNT(*) FROM institutions")
        inst_id = int(last_inst_id[0]['COUNT(*)'])+1 
        type = state = zip = "NULL"
        my_str = "('"+str(inst_id)+"', '"+type+"', '"+institution+"', '"+department+"', '"+address+"', '"+city+"', '"+state+"', '"+zip+"')"
        self.query("INSERT IGNORE INTO `institutions` (`inst_id`, `type`, `name`, `department`, `address`, `city`, `state`, `zip`) VALUES " + my_str)

        last_inst_id = self.query("SELECT COUNT(*) FROM positions")
        pos_id = int(last_inst_id[0]['COUNT(*)'])+1 
        title = responsibilities = "NULL"
        my_str = "('"+str(pos_id)+"', '"+str(inst_id)+"', '"+position+"', '"+responsibilities+"', '"+start_date+"', '"+end_date+"')"
        self.query("INSERT IGNORE INTO `positions` (`position_id`, `inst_id`, `title`, `responsibilities`, `start_date`, `end_date`) VALUES " + my_str)

        last_exp_id = self.query("SELECT COUNT(*) FROM experiences")
        exp_id = int(last_exp_id[0]['COUNT(*)'])+1 
        hyperlink = start_date = end_date = ""
        my_str = "('"+str(exp_id)+"', '"+str(pos_id)+"', '"+position_name+"', '"+position_description+"', '"+hyperlink+"', '"+start_date+"', '"+end_date+"')"
        self.query("INSERT IGNORE INTO `experiences` (`experience_id`, `position_id`, `name`, `description`, `hyperlink`, `start_date`, `end_date`) VALUES " + my_str)


        last_skill_id = self.query("SELECT COUNT(*) FROM skills")
        skill_id = int(last_skill_id[0]['COUNT(*)'])+1 
        skill_level = "NULL"
        my_str = "('"+str(skill_id)+"', '"+str(exp_id)+"', '"+skill+"', '"+skill_level+"')"
        self.query("INSERT IGNORE INTO `skills` (`skill_id`, `experience_id`, `name`, `skill_level`) VALUES " + my_str)






#######################################################################################
# NFT RELATED
#######################################################################################
    """
    Creates NFT in database
    :param description: description of an NFT
    :param owner: owner of an NFT
    :param token: token of an NFT
    :param image: image of an NFT
    :param onMarket: whther NFT is on market or not
    :return: None
    """
    def createNFT(self, description="very nice NFT", owner='me@email.com', token=100, image=None, onMarket=1):
        #self.query("DELETE FROM nfts;")
        last_nft_id = self.query("SELECT COUNT(*) FROM nfts")
        biggest_id = int(last_nft_id[0]['COUNT(*)'])+1
        description = str(description)
        owner = str(owner)
        token = str(token)
        onMarket = str(onMarket)
        self.query("INSERT IGNORE INTO `nfts` (`nft_id`, `description`, `owner`, `token`, `image`, `onMarket`) VALUES (%s, %s, %s, %s, %s, %s)", (biggest_id, description, owner, token, image, onMarket))


    """
    Gets NFT data from database
    :return: Data about NFT
    """
    def getNFT(self):
        nfts = self.query("SELECT * FROM nfts")
        my_dict = {}
        for row in range(len(nfts)):
            new_dict = {}
            nft_id = nfts[row]['nft_id']
            description = nfts[row]['description']
            owner = nfts[row]['owner']
            token = nfts[row]['token']
            image = nfts[row]['image']
            onMarket = nfts[row]['onMarket']
            new_dict['description'] = description
            new_dict['owner'] = owner
            new_dict['token'] = token
            new_dict['image'] = image
            new_dict['onMarket'] = onMarket
            my_dict[nft_id] = new_dict
        return my_dict
    
    """
    Updates nft description in database
    :param nft_id: id of nft
    :param description: new description of nft
    :return: None
    """
    def update_nft_description(self, nft_id ,description):
        self.query("UPDATE nfts SET description = '" + description + "' WHERE nft_id = " + nft_id +";")


    """
    Updates nft token in database
    :param nft_id: id of nft
    :param token: new token of nft
    :return: None
    """
    def update_nft_token(self, nft_id ,token):
        self.query("UPDATE nfts SET token = '" + token + "' WHERE nft_id = " + nft_id +";")


    """
    Get balance of user
    :param email: email of user
    :return: balance of user
    """
    def getBalance(self, email):
        balance = self.query("SELECT balance FROM users WHERE email = '" + email + "';")
        print(self.query("SELECT * FROM users;"))
        print(balance)
        print(email)
        return balance[0]['balance']
    

    """
    Makes the transaction
    :param nft_id: id of nft
    :param buyer: email of buyer
    :param token: token of nft
    :return: None
    """
    def completeTransaction(self, nft_id, buyer, token):
        seller = self.query("SELECT owner FROM nfts WHERE nft_id = " + nft_id +";") #finds seller
        token = self.query("SELECT token FROM nfts WHERE nft_id = " + nft_id +";")
        seller = str(seller[0]['owner'])
        token = str(token[0]['token'])
        self.query("UPDATE users SET balance = balance - '" + token  +"' WHERE email = '" + buyer + "';")   #updates buyer balance
        self.query("UPDATE users SET balance = balance + '" + token  +"' WHERE email = '" + seller + "';") #updates seller balance
        self.query("UPDATE nfts SET owner = '" + buyer + "' WHERE nft_id = " + nft_id +";")
        self.addTransaction(token, seller, buyer, buyer, nft_id)
        return
    


    """
    Adds transaction to database
    :param nft_id: id of nft
    :param buyer: email of buyer
    :param cost: cost of nft
    :param seller: email of seller
    :param owner: email of owner
    :return: None
    """
    def addTransaction(self, cost, seller, buyer, owner, nft_id ):
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        last_inst_id = self.query("SELECT COUNT(*) FROM transactions")
        trans_id = int(last_inst_id[0]['COUNT(*)'])+1 
        my_str = "('"+str(trans_id)+"', '"+str(cost)+"', '"+str(seller)+"', '"+str(buyer)+"', '"+str(owner)+"', '"+str(nft_id)+"', '"+str(date)+"')"
        self.query("INSERT IGNORE INTO `transactions` (`transaction_id`, `cost`, `seller`, `buyer`, `owner`, `nft_id`, `date`) VALUES " + my_str)
        print(self.query("SELECT * FROM transactions"))
        # self.query("DELETE FROM transactions;")


    """
    Gets NFT's transactions from database
    :param nft_id: id of nft
    :return: All NFT's transactions from database
    """
    def getTransactions(self, nft_id):
        transactions = self.query("SELECT * FROM transactions WHERE nft_id = " + nft_id +";")
        my_dict = {}
        for row in range(len(transactions)):
            new_dict = {}
            transaction_id = transactions[row]['transaction_id']
            cost = transactions[row]['cost']
            seller = transactions[row]['seller']
            buyer = transactions[row]['buyer']
            owner = transactions[row]['owner']
            nft_id = transactions[row]['nft_id']
            date = transactions[row]['date']
            new_dict['cost'] = cost
            new_dict['seller'] = seller
            new_dict['buyer'] = buyer
            new_dict['owner'] = owner
            new_dict['nft_id'] = nft_id
            new_dict['date'] = date
            my_dict[transaction_id] = new_dict
        return my_dict