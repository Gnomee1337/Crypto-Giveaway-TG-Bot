import logging
import mysql.connector
from mysql.connector import errorcode

# import sqlite3
# import keyboards.markups as nav
# import re

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT


# TODO: USE ORM dumbass -_-
class Database:
    def __init__(self):
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_DATABASE
        self.port = DB_PORT

        try:
            logging.info("DB starting Test-Connection")
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your DB user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.connection.cursor()
            logging.info("DB Test-Connection established!")
            self.__disconnect__()

    # # For SQLite3
    # def __init__(self, db_file):
    #     self.connection = sqlite3.connect(db_file)
    #     self.cursor = self.connection.cursor()
    #     if(self.connection):
    #         print("DB Connected!")

    def __connect__(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        logging.debug("DB connection established!")

    def __disconnect__(self):
        self.cursor.close()
        self.connection.close()
        logging.debug("DB cursor and connection closed!")

    def add_user(self, user_id, nickname, referral_id=None):
        self.__connect__()
        if referral_id != None:
            sql = "INSERT INTO `users_bot` (`tg_id`,`tg_nickname`,`referral_id`) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (user_id, nickname, referral_id,), )
            self.connection.commit()
            # result = self.cursor.fetchall()
        else:
            sql = "INSERT INTO `users_bot` (`tg_id`,`tg_nickname`) VALUES (%s, %s)"
            self.cursor.execute(sql, (user_id, nickname,), )
            self.connection.commit()
            # result = self.cursor.fetchall()
        self.__disconnect__()
        # if result is None:
        #     return 0
        # else:
        #     return bool(len(result))
        return True

    def user_exists(self, user_id):
        self.__connect__()
        sql = "SELECT * FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchall()
        self.__disconnect__()
        if result is None:
            return 0
        else:
            return bool(len(result))

    def set_wallet(self, user_id, wallet):
        self.__connect__()
        sql = "UPDATE `users_bot` SET `wallet` = %s WHERE `tg_id` = %s"
        self.cursor.execute(sql, (wallet, user_id,))
        self.connection.commit()
        # result = self.cursor.fetchall()
        self.__disconnect__()
        # if result is None:
        #     return 0
        # else:
        #     return bool(len(result))
        return True

    def get_wallet(self, user_id):
        self.__connect__()
        sql = "SELECT `wallet` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        # for row in result:
        # wallet = str(row[0])
        # return wallet
        if result is None:
            return 0
        else:
            return result[0]

    def get_nickname(self, user_id):
        self.__connect__()
        sql = "SELECT `tg_nickname` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        # for row in result:
        # nickname = str(row[0])
        # return nickname
        if result is None:
            return 0
        else:
            return result[0]

    def set_signup(self, user_id, signup):
        self.__connect__()
        sql = "UPDATE `users_bot` SET `signup` = %s WHERE `tg_id` = %s"
        self.cursor.execute(sql, (signup, user_id,))
        self.connection.commit()
        # result = self.cursor.fetchall()
        self.__disconnect__()
        # if result is None:
        #     return 0
        # else:
        #     return bool(len(result))
        return True

    def get_signup(self, user_id):
        self.__connect__()
        sql = "SELECT `signup` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        ## for row in result:
        ## signup = str(row[0])
        ## return signup
        print(result[0])
        if result is None:
            return 0
        else:
            return result[0]
        # return True

    def count_referrals(self, user_id):
        self.__connect__()
        sql = "SELECT COUNT(`id_users`) as count FROM `users_bot` WHERE `referral_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        # return result[0]
        if result is None:
            return 0
        else:
            return result[0]

    def get_invite_fails(self, user_id):
        self.__connect__()
        sql = "SELECT `invite_fails` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        # return result[0]
        if result is None:
            return 0
        else:
            return result[0]

    def increase_invite_fails(self, user_id):
        current_invite_fails = self.get_invite_fails(user_id)
        new_invite_fails = current_invite_fails + 1
        self.__connect__()
        sql = "UPDATE `users_bot` SET `invite_fails` = %s WHERE `tg_id` = %s"
        self.cursor.execute(sql, (new_invite_fails, user_id,))
        self.connection.commit()
        # result = self.cursor.fetchone()
        # if result is None:
        #     return 0
        # else:
        #     return result
        return True

    def create_task(self, user_id, task_text, task_counter=1, task_reward=0):
        self.__connect__()
        sql = "INSERT INTO `tasks_bot` (`task_author`,`task`,`task_complete_counter`,`points_reward`) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(
            sql, (user_id, task_text, task_counter, task_reward,))
        self.connection.commit()
        last_task_id = self.cursor.lastrowid
        print("###DEBUG### Last Created Task ID: " + str(last_task_id))
        logging.debug("###DEBUG### Last Created Task ID: " + str(last_task_id))
        sql = "INSERT INTO `task_tracker_2` (`task_id_tracker`,`assigned_user`) SELECT `id_tasks`, `id_users` FROM `tasks_bot` CROSS JOIN `users_bot` WHERE `id_tasks` = %s"
        self.cursor.execute(sql, (last_task_id,))
        self.connection.commit()
        self.__disconnect__()
        return True

    def assign_new_user_to_all_tasks(self, user_id):
        self.__connect__()
        sql = "SELECT `id_users` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        db_user_id = self.cursor.fetchone()
        # tasks = self.cursor.execute("SELECT `id_tasks` from `tasks_bot`").fetchall()
        sql = "INSERT INTO `task_tracker_2` (`task_id_tracker`,`assigned_user`) SELECT `id_tasks`, `id_users` FROM `tasks_bot` CROSS JOIN `users_bot` WHERE `id_users` = %s"
        # self.cursor.execute("INSERT INTO `task_tracker_2` (`task_id_tracker`,`assigned_user`) SELECT `id_tasks`, `id_users` FROM `tasks_bot` CROSS JOIN `users_bot` WHERE `id_users` = ?",(db_user_id[0],))
        self.cursor.execute(sql, (db_user_id[0],))
        self.connection.commit()
        self.__disconnect__()
        return True

    # def get_task(self, user_id):
    #     self.__connect__()
    #     sql = "SELECT `task` FROM `tasks_bot`"
    #     self.cursor.execute(sql, ())
    #     result = self.cursor.fetchall()
    #     self.__disconnect__()
    #     # for row in result:
    #     # task_text = str(row[0])
    #     if result is None:
    #         return 0
    #     else:
    #         return result[0]

    def get_task_by_id(self, task_id):
        self.__connect__()
        logging.debug("###DEBUG### task_id in get_task_by_id=")
        print("###DEBUG### task_id in get_task_by_id=")
        print(task_id)
        logging.debug(task_id)
        sql = "SELECT `task` FROM `tasks_bot` WHERE `id_tasks` = %s"
        self.cursor.execute(sql, (task_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        logging.debug("###DEBUG### Task_Name from get_task_by_id =")
        logging.debug(result)
        print("###DEBUG### Task_Name from get_task_by_id =")
        print(result)
        # task_name = []
        # for tup in result:
        # task_name = tup
        # return task_name
        if result is None:
            return 0
        else:
            return result[0]

    def get_tgnickname_by_id(self, assigned_user):
        self.__connect__()
        logging.debug("###DEBUG### assigned_user in get_tgnickname_by_id=")
        logging.debug(assigned_user)
        print("###DEBUG### assigned_user in get_tgnickname_by_id=")
        print(assigned_user)
        sql = "SELECT `tg_nickname` FROM `users_bot` WHERE `id_users` = %s"
        self.cursor.execute(sql, (assigned_user,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        # result = self.cursor.execute("SELECT `tg_nickname` FROM `users_bot` WHERE `id_users` = ?",(assigned_user,)).fetchone()
        logging.debug("###DEBUG### tg_nickname from get_tgnickname_by_id =")
        logging.debug(result)
        print("###DEBUG### tg_nickname from get_tgnickname_by_id =")
        print(result)
        # tgnickname = []
        # for tup in result:
        # tgnickname = tup
        # return tgnickname
        if result is None:
            return 0
        else:
            return result[0]

    def get_user_language(self, user_id):
        self.__connect__()
        sql = "SELECT `language` FROM `users_bot` WHERE `tg_id` = %s"
        # return self.cursor.execute("SELECT `language` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()[0]
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        if result is None:
            return 0
        else:
            return result[0]

    def change_user_language(self, user_id, new_language):
        self.__connect__()
        sql = "UPDATE `users_bot` set `language` = %s WHERE `tg_id` = %s"
        # self.cursor.execute("UPDATE `users_bot` set `language` = ? WHERE `tg_id` = ?",(new_language, user_id,))
        self.cursor.execute(sql, (new_language, user_id,))
        self.connection.commit()
        self.__disconnect__()
        return True

    def get_user_points(self, user_id):
        self.__connect__()
        logging.debug("###DEBUG### user_points in get_user_points=")
        print("###DEBUG### user_points in get_user_points=")
        sql = "SELECT `user_points` FROM `users_bot` WHERE `tg_id` = %s"
        # result = self.cursor.execute("SELECT `user_points` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        logging.debug(result)
        print(result)
        return result[0]

    def increase_user_points(self, user_id, amount):
        logging.debug(
            "###DEBUG### current_user_points in increase_user_points=")
        print("###DEBUG### current_user_points in increase_user_points=")
        current_user_points = self.get_user_points(user_id)
        logging.debug(current_user_points)
        print(current_user_points)
        self.__connect__()
        new_user_points = current_user_points + amount
        sql = "UPDATE `users_bot` SET `user_points` = %s WHERE `tg_id` = %s"
        # self.cursor.execute("UPDATE `users_bot` SET `user_points` = ? WHERE `tg_id` = ?",(new_user_points, user_id,))
        self.cursor.execute(sql, (new_user_points, user_id,))
        self.connection.commit()
        self.__disconnect__()
        logging.debug(
            "###DEBUG### new_user_points from increase_user_points =")
        print("###DEBUG### new_user_points from increase_user_points =")
        logging.debug(new_user_points)
        print(new_user_points)
        return True

    def decrease_user_points(self, user_id, amount):
        logging.debug(
            "###DEBUG### current_user_points in decrease_user_points=")
        print("###DEBUG### current_user_points in decrease_user_points=")
        current_user_points = self.get_user_points(user_id)
        logging.debug(current_user_points)
        print(current_user_points)
        self.__connect__()
        new_user_points = 0
        if (current_user_points < amount):
            # self.cursor.execute("UPDATE `users_bot` SET `user_points` = ? WHERE `tg_id` = ?",(new_user_points, user_id,))
            sql = "UPDATE `users_bot` SET `user_points` = %s WHERE `tg_id` = %s"
            self.cursor.execute(sql, (new_user_points, user_id,))
            self.connection.commit()
        else:
            new_user_points = current_user_points - amount
            # self.cursor.execute("UPDATE `users_bot` SET `user_points` = ? WHERE `tg_id` = ?",(new_user_points, user_id,))
            sql = "UPDATE `users_bot` SET `user_points` = %s WHERE `tg_id` = %s"
            self.cursor.execute(sql, (new_user_points, user_id,))
            self.connection.commit()
        self.__disconnect__()
        logging.debug(
            "###DEBUG### new_user_points from decrease_user_points =")
        print("###DEBUG### new_user_points from decrease_user_points =")
        logging.debug(new_user_points)
        print(new_user_points)
        return True

    def get_users_status(self, to_verify=None):
        self.__connect__()
        if (to_verify == None):
            # dirty_users_status = self.cursor.execute("SELECT * FROM `task_tracker_2` ORDER BY `assigned_user`").fetchall()
            sql = "SELECT * FROM `task_tracker_2` ORDER BY `assigned_user`"
            self.cursor.execute(sql, ())
            dirty_users_status = self.cursor.fetchall()
        else:
            # dirty_users_status = self.cursor.execute("SELECT * FROM `task_tracker_2` WHERE `completed` = 1 AND `verified` = 0 ORDER BY `assigned_user`").fetchall()
            sql = "SELECT * FROM `task_tracker_2` WHERE `completed` = 1 AND `verified` = 0 ORDER BY `assigned_user`"
            self.cursor.execute(sql, ())
            dirty_users_status = self.cursor.fetchall()
            ## dirty_all_users = self.cursor.execute("SELECT `id_users`,`tg_nickname` FROM `users_bot`").fetchall()
            ## dirty_all_tasks = self.cursor.execute("SELECT `id_tasks`,`task` FROM `tasks_bot`").fetchall()
        self.__disconnect__()
        # Replace Task_id_tracker to Task Name
        for i in range(len(dirty_users_status)):
            dirty_users_status_list = list(dirty_users_status[i])
            dirty_users_status_list[1] = self.get_task_by_id(
                str(dirty_users_status_list[1]))
            dirty_users_status[i] = tuple(dirty_users_status_list)
        # Replace assigned_user to tg Nickname
        for i in range(len(dirty_users_status)):
            dirty_users_status_list = list(dirty_users_status[i])
            dirty_users_status_list[2] = self.get_tgnickname_by_id(
                str(dirty_users_status_list[2]))
            dirty_users_status[i] = tuple(dirty_users_status_list)
        # Replace Status to True/False
        for i in range(len(dirty_users_status)):
            dirty_users_status_list = list(dirty_users_status[i])
            # temp = self.get_tgnickname_by_id(str(dirty_users_status_list[1]))
            # for tup in temp:
            if (dirty_users_status_list[4] == '0'):
                dirty_users_status_list[4] = "Not Completed"
            else:
                dirty_users_status_list[4] = "Completed"
            dirty_users_status[i] = tuple(dirty_users_status_list)
        logging.debug(dirty_users_status)
        print(dirty_users_status)
        return dirty_users_status

    def get_active_tasks(self, user_id):
        self.__connect__()
        # Get user ID from DB
        # db_user_id = self.cursor.execute("SELECT `id_users` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()
        sql = "SELECT `id_users` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        db_user_id = self.cursor.fetchone()
        logging.debug("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        print("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        # Get active tasks ID assigned to user from DB
        # active_tasks_id = self.cursor.execute("SELECT `task_id_tracker` FROM `task_tracker_2` WHERE `assigned_user` = ? AND `completed` = 0",(str(db_user_id[0]),)).fetchall()
        sql = "SELECT `task_id_tracker` FROM `task_tracker_2` WHERE `assigned_user` = %s AND `completed` = 0"
        self.cursor.execute(sql, (db_user_id[0],))
        active_tasks_id = self.cursor.fetchall()
        logging.debug("###DEBUG### Active_Tasks_ID: " + str(active_tasks_id))
        print("###DEBUG### Active_Tasks_ID: " + str(active_tasks_id))
        if not active_tasks_id:
            return 0
        ## Leave only digits from query
        ## active_task_id_only_digits = []
        ## for task_id in active_tasks_id:
        ## active_task_id_only_digits.append(re.sub("[^\d\.]","",str(task_id)))
        ## print("###DEBUG### Active_Tasks_ID RE.SUB: "+str(active_task_id_only_digits))
        ## Get list of active task names from DB
        ## active_tasks = []
        ## for task_id in active_task_id_only_digits:
        ## active_tasks.append(list(self.cursor.execute("SELECT `task` FROM `tasks_bot` WHERE `id_tasks` = ?",(task_id,)).fetchall()))
        ## print("###DEBUG### Active_TASKS: "+str(active_tasks))
        ## Add task_id to list
        active_tasks = []
        for tup in active_tasks_id:
            for number in tup:
                sql = "SELECT `task`,`points_reward` FROM `tasks_bot` WHERE `id_tasks` = %s"
                self.cursor.execute(sql, (number,))
                active_tasks += self.cursor.fetchall()
                # active_tasks += self.cursor.execute("SELECT `task`,`points_reward` FROM `tasks_bot` WHERE `id_tasks` = ?",(number,)).fetchall()
                # active_tasks.append(list(self.cursor.execute("SELECT `task` FROM `tasks_bot` WHERE `id_tasks` = ?",(number,)).fetchall()))
                logging.debug("###DEBUG### Active_TASKS: " + str(active_tasks))
                print("###DEBUG### Active_TASKS: " + str(active_tasks))
        ## Leave only task names from query
        ## active_tasks_only_text = []
        ## for active_task in list(active_tasks):
        ##    #print("###DEBUG### active_task: "+str(active_task))
        ##    #temp_string = re.sub(r'.$','',str(temp_string),count=3)
        ## print("###DEBUG### active_tasks_only_text RE.SUB: "+str(active_tasks_only_text))
        self.__disconnect__()
        return active_tasks

    def get_task_admin(self, user_id):
        self.__connect__()
        # result = self.cursor.execute("SELECT * FROM `tasks_bot`").fetchall()
        sql = "SELECT * FROM `tasks_bot`"
        self.cursor.execute(sql, ())
        result = self.cursor.fetchall()
        ## for row in result:
        ##    task_text = str(row[0])
        self.__disconnect__()
        return result

    def submit_task(self, user_id, task_name, task_answer):
        self.__connect__()
        # Get DB user ID by tg_id
        # db_user_id = self.cursor.execute("SELECT `id_users` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()
        sql = "SELECT `id_users` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        db_user_id = self.cursor.fetchone()
        logging.debug("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        print("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        # Get DB task id by task_name
        # db_task_id = self.cursor.execute("SELECT `id_tasks` FROM `tasks_bot` WHERE `task` = ?",(task_name,)).fetchone()
        sql = "SELECT `id_tasks` FROM `tasks_bot` WHERE `task` = %s"
        self.cursor.execute(sql, (task_name,))
        db_task_id = self.cursor.fetchone()
        logging.debug("###DEBUG### DB_TASK_ID: " + str(db_task_id[0]))
        print("###DEBUG### DB_TASK_ID: " + str(db_task_id[0]))
        ## IN DEV for Multiple answers in DB
        ## Get old answers
        ## old_user_answers = self.cursor.execute("SELECT `answer_field` FROM `task_tracker_2` WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],)).fetchone()
        ## print("###DEBUG### DB_ANSWER_FIELD: "+str(old_user_answers[0]))
        ## Concatenate new answer with old
        ## new_user_answer = str(old_user_answers[0]) +", "+ task_answer
        ## print("###DEBUG### new_user_answer: "+str(new_user_answer))
        ## Update task status to TRUE
        ## self.cursor.execute("UPDATE `task_tracker_2` SET `completed` = 1, `answer_field` = ? WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(task_answer, db_task_id[0], db_user_id[0],))
        sql = "UPDATE `task_tracker_2` SET `completed` = 1, `answer_field` = %s WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
        self.cursor.execute(sql, (task_answer, db_task_id[0], db_user_id[0],))
        self.connection.commit()
        self.__disconnect__()
        return True

    def verify_task(self, user_id, task_name, verify_status):
        self.__connect__()
        # Get DB user ID by tg_id
        # db_user_id = self.cursor.execute("SELECT `id_users` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()
        sql = "SELECT `id_users` FROM `users_bot` WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        db_user_id = self.cursor.fetchone()
        print("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        logging.debug("###DEBUG### DB_USER_ID: " + str(db_user_id[0]))
        # Get DB task id by task_name
        # db_task_id = self.cursor.execute("SELECT `id_tasks` FROM `tasks_bot` WHERE `task` = ?",(task_name,)).fetchone()
        sql = "SELECT `id_tasks` FROM `tasks_bot` WHERE `task` = %s"
        self.cursor.execute(sql, (task_name,))
        db_task_id = self.cursor.fetchone()
        print("###DEBUG### DB_TASK_ID: " + str(db_task_id[0]))
        logging.debug("###DEBUG### DB_TASK_ID: " + str(db_task_id[0]))
        # If "verify_status" parameter True, then verify task
        if (verify_status == True):
            # Get DB "task_completed_times" for current task
            # db_task_completed_times = self.cursor.execute("SELECT `task_completed_times` FROM `task_tracker_2` WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],)).fetchone()
            sql = "SELECT `task_completed_times` FROM `task_tracker_2` WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
            self.cursor.execute(sql, (db_task_id[0], db_user_id[0],))
            db_task_completed_times = self.cursor.fetchone()
            # Get DB max "task_complete_counter" for task
            # db_task_complete_counter = self.cursor.execute("SELECT `task_complete_counter` FROM `tasks_bot` WHERE `id_tasks` = ?",(db_task_id[0],)).fetchone()
            sql = "SELECT `task_complete_counter` FROM `tasks_bot` WHERE `id_tasks` = %s"
            self.cursor.execute(sql, (db_task_id[0],))
            db_task_complete_counter = self.cursor.fetchone()
            # Take reward value
            # db_task_reward = self.cursor.execute("SELECT `points_reward` FROM `tasks_bot` WHERE `id_tasks` = ?",(db_task_id[0],)).fetchone()
            sql = "SELECT `points_reward` FROM `tasks_bot` WHERE `id_tasks` = %s"
            self.cursor.execute(sql, (db_task_id[0],))
            db_task_reward = self.cursor.fetchone()
            # If current completed status for task less than max complete counter from task
            if (db_task_completed_times[0] < db_task_complete_counter[0]):
                # Increase completed counter
                new_counter = db_task_completed_times[0] + 1
                # Update counter
                # self.cursor.execute("UPDATE `task_tracker_2` SET `verified` = 0, `completed` = 0, `task_completed_times` = ? WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(new_counter, db_task_id[0], db_user_id[0],))
                sql = "UPDATE `task_tracker_2` SET `verified` = 0, `completed` = 0, `task_completed_times` = %s WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
                self.cursor.execute(
                    sql, (new_counter, db_task_id[0], db_user_id[0],))
                self.connection.commit()
                # Give points
                self.increase_user_points(user_id, db_task_reward[0])
                self.__connect__()
                # self.cursor.execute("UPDATE `task_tracker_2` SET `verified` = 1 WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],))
                if (new_counter >= db_task_complete_counter[0]):
                    # if current complete counter more/equal to max complete counter
                    # self.cursor.execute("UPDATE `task_tracker_2` SET `verified` = 1, `completed` = 1 WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],))
                    sql = "UPDATE `task_tracker_2` SET `verified` = 1, `completed` = 1 WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
                    self.cursor.execute(sql, (db_task_id[0], db_user_id[0],))
                    self.connection.commit()
            else:
                # if current complete counter more/equal to max complete counter
                # self.cursor.execute("UPDATE `task_tracker_2` SET `verified` = 1 WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],))
                sql = "UPDATE `task_tracker_2` SET `verified` = 1 WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
                self.cursor.execute(sql, (db_task_id[0], db_user_id[0],))
                self.connection.commit()
                # Give points
                self.increase_user_points(user_id, db_task_reward[0])
                self.__connect__()
        else:
            # If "verify_status" parameter False, then decomplete task
            # self.cursor.execute("UPDATE `task_tracker_2` SET `completed` = 0 WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],))
            sql = "UPDATE `task_tracker_2` SET `completed` = 0 WHERE `task_id_tracker` = %s AND `assigned_user` = %s"
            self.cursor.execute(sql, (db_task_id[0], db_user_id[0],))
            self.connection.commit()
        # self.connection.commit()
        self.__disconnect__()
        return True

    def log_payment(self, user_id, payment_sum, points_bought):
        self.__connect__()
        # self.cursor.execute("INSERT INTO `payment_logs` (`id_payment_user`,`payment_sum`,`points_bought`) VALUES (?, ?, ?)", (user_id, payment_sum, points_bought,))
        sql = "INSERT INTO `payment_logs` (`id_payment_user`,`payment_sum`,`points_bought`) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (user_id, payment_sum, points_bought,))
        self.connection.commit()
        self.__disconnect__()
        print("###DEBUG### Payment log: " +
              str(user_id) + " spent " + str(payment_sum))
        logging.debug("###DEBUG### Payment log: " +
                      str(user_id) + " spent " + str(payment_sum))
        return True

    def get_bundles(self):
        self.__connect__()
        # result = self.cursor.execute("SELECT `tokens_amount`,`price_amount`,`bundle_name` FROM `bundle_shop` WHERE `bundle_status` = 1").fetchall()
        sql = "SELECT `tokens_amount`,`price_amount`,`bundle_name` FROM `bundle_shop` WHERE `bundle_status` = 1"
        self.cursor.execute(sql, ())
        result = self.cursor.fetchall()
        ## for row in result:
        ## task_text = str(row[0])
        self.__disconnect__()
        return result

    # IN DEV
    # def remove_last_task_answer(self, user_id, task_name):
    #     with self.connection:
    #         print("###DEBUG### remove_last_task_answer")

    #         #Get DB user ID by tg_id
    #         db_user_id = self.cursor.execute("SELECT `id_users` FROM `users_bot` WHERE `tg_id` = ?",(user_id,)).fetchone()
    #         print("###DEBUG### DB_USER_ID: "+str(db_user_id[0]))

    #         #Get DB task id by task_name
    #         db_task_id = self.cursor.execute("SELECT `id_tasks` FROM `tasks_bot` WHERE `task` = ?",(task_name,)).fetchone()
    #         print("###DEBUG### DB_TASK_ID: "+str(db_task_id[0]))

    #         #Get old answers
    #         old_user_answers = self.cursor.execute("SELECT `answer_field` FROM `task_tracker_2` WHERE `task_id_tracker` = ? AND `assigned_user` = ?",(db_task_id[0], db_user_id[0],)).fetchone()
    #         print("###DEBUG### DB_ANSWER_FIELD: "+str(old_user_answers[0]))

    #         new_answer = old_user_answers[0].split()

    #         self.cursor.execute("UPDATE `task_tracker_2` SET `answer_field` = ? WHERE `task_id_tracker` = ? AND `assigned_user` = ?")

    #     return True

    # FOR DEBUG, list tasks in buttons
    # def tasks_markup(self, user_id, page):
    #     markup_tasks = nav.InlineKeyboardMarkup(row_width=2)
    #     items = page * 10
    #     count = 0
    #     check = self.cursor.execute("SELECT `task` FROM `tasks_bot` WHERE `task_author` = ?", (user_id,)).fetchall()
    #     print("###DEBUG### (tasks_markup) check: "+str(check))
    #     x = 0
    #     for j in check:
    #         x += 1
    #         for item in range(items-10, items):
    #             for i in self.cursor.execute("SELECT `task` FROM `tasks_bot` WHERE `task_author` = ? AND `id_tasks` = ?",(user_id, item,)).fetchall():
    #                 count += 1
    #                 markup_tasks.insert(nav.InlineKeyboardButton(i[0], callback_data=str(item)))
    #         if count == 10 and page == 1 and x > 10:
    #             markup_tasks.add(nav.btnNext_adm)
    #         elif count % 10 == 0 and page != 1:
    #             markup_tasks.add(nav.btnBack_adm)
    #             markup_tasks.insert(nav.btnNext_adm)
    #         elif count % 10 != 0 and page != 1:
    #             markup_tasks.add(nav.btnBack_adm)

    #     # elif page == 1 and last_page == False and count == 10:
    #     # 	markup_tasks.add(next_btn)
    #     # elif last_page == False and page != 1:
    #     # 	markup_tasks.insert(back_btn)
    #     # 	markup_tasks.insert(next_btn)
    #     # elif last_page == True:
    #     # 	markup_tasks.add(back_btn)
    #     return markup_tasks
