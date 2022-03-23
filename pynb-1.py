import json
import pprint
import sqlite3


class Project:
    # initialization
    def __init__(self):
        self.db_name = "main.db"
        self.db_connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connection.cursor()

    def create_tables(self):
        task_table = '''CREATE TABLE tasks IF NOT EXISTS (
                        task_id int primary key auto increment,
                        task_content varchar(255),
                        complete int
                        )
                        '''
        hashtag_table = '''CREATE TABLE hashtags IF NOT EXISTS(
                            hashtag_id int primary key auto increment,
                            hashtag_name varchar(255) unique
                            )
                        '''
        hash_tasks = '''CREATE TABLE hashtasks IF NOT EXISTS(
                            rel_id int,
                            hashtag_id int,
                            task_id int,
                            removed int,
                            primary key (hashtag_id, task_id)
                            )
                            '''
        self.db_cursor.execute(task_table)
        self.db_cursor.execute(hashtag_table)
        self.db_cursor.execute(hash_tasks)

    def find_hashtag(self, task_content):
        tags = []
        for word in task_content.split():
            if word[0] == "#":
                if word not in tags:
                    tags.append(word[1:])
        if len(tags) != 0:
            return tags
        return False

#######################################################################################################################
    def add_task(self, task_content):  # NOT COMPLETELY DONE TEST PENDING
        # add to tasks table
        task_query = "INSERT INTO tasks (task_content, complete) value(?,0)"
        self.db_cursor.execute(task_query, [task_content])
        # get task_id # TODO TEST
        task_id = self.db_cursor.execute("SELECT task_id FROM TASK ORDER BY ID DESC LIMIT 1").fetchone()
        # add to hashtag table
        hashtag_query = "INSERT OR IGNORE INTO hashtags (hashtag_name) value(?)"  # TODO TEST
        tags_list = self.find_hashtag(task_content)
        if tags_list:
            for hashtag in tags_list:
                self.db_cursor.execute(hashtag_query, [hashtag])
        # TODO ADD TO HASHTASK TABLE,
        print("Task added successfully..")

    def mark_task_complete(self, task_id):  # COMPLETELY DONE TEST PENDING
        query = "UPDATE TASKS SET complete=1 WHERE task_id=?"
        self.db_cursor.execute(query, [task_id])

    def edit_task(self, task_id, new_content):
        # remove all entries from hashtask table where task_id
        remove_from_hashtask = "DELETE FROM HASHTASKS WHERE task_id=?"
        self.db_cursor.execute(remove_from_hashtask, [task_id])
        # edit from tasks table
        edit_task_query = "UPDATE TASKS SET content=? WHERE task_id=?"
        self.db_cursor.execute(edit_task_query, [new_content, task_id])

        tag_name = self.find_hashtag(new_content)
        if tag_name:
            for hashtag in tag_name:
                hashtag_query = "INSERT OR IGNORE INTO hashtags (hashtag_name) value(?)"
                self.db_cursor.execute(hashtag_query, [hashtag])
                # TODO ADD FUNCTIONALITY TO REMOVE TASK FROM HASHTAG MAPPING TABLE
        else:
            print("No new hashtags found")
        print("modified..")

    def delete_task(self, task_id):
        query = "DELETE FROM TASKS WHERE task_id=?"
        self.db_cursor.execute(query, [task_id])

        # TODO ADD FUNCTIONALITY TO REMOVE FROM HASHTAGS MAPPING TABLE

    def fetch_tagged_tasks(self):
        query = '''SELECT task_content FROM TASKS
                    W'''
        # TODO COMPLETE THIS

    def fetch_tag_by_task(self, hashtag_name):
        query = '''select '''
        query = '''SELECT task_content from tasks
                    where task_id in (select task_id from hashtask where hashtag_id=(select hashtag_id from '''


