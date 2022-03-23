import sqlite3


class Project:
    # initialization
    def __init__(self):
        self.db_name = "main.db"
        self.db_connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connection.cursor()
        self.create_tables()

    def create_tables(self):
        task_table = '''
                        CREATE TABLE  IF NOT EXISTS tasks 
                        (
                        task_id INTEGER primary key autoincrement,
                        task_content varchar(255),
                        complete INTEGER
                        );
                        '''

        hashtag_table = '''
                            CREATE TABLE IF NOT EXISTS hashtags
                            (
                            hashtag_id INTEGER primary key autoincrement,
                            hashtag_name varchar(255) unique
                            );
                        '''

        hash_tasks = '''
                        CREATE TABLE IF NOT EXISTS hashtasks
                        (
                        hashtag_id INTEGER,
                        task_id INTEGER,
                        primary key (hashtag_id, task_id),
                        foreign key (hashtag_id) references hashtags(hashtag_id),
                        foreign key (task_id) references tasks(task_id)
                        );
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
        # remove all entries from hashtask table
        remove_from_hashtask = "DELETE FROM HASHTASKS WHERE task_id=?"
        self.db_cursor.execute(remove_from_hashtask, [task_id])

        # edit from tasks table
        edit_task_query = "UPDATE TASKS SET content=? WHERE task_id=?"
        self.db_cursor.execute(edit_task_query, [new_content, task_id])

        # add mapping to hashtask table
        tag_name = self.find_hashtag(new_content)
        if tag_name:
            for hashtag in tag_name:
                hashtag_query = "INSERT OR IGNORE INTO hashtags (hashtag_name) value(?)"
                self.db_cursor.execute(hashtag_query, [hashtag])

                hashtag_id = self.db_cursor.execute("select hashtag_id from hashtags order by desc limit 1")
                hashtasks_query = "INSERT INTO HASHTASKS (task_id, hashtag_id) value (?,?)"
                self.db_cursor.execute(hashtasks_query, [task_id, hashtag_id])
        else:
            print("No new hashtags found")
        print("modified..")

    def delete_task(self, task_id):
        task_query = "DELETE FROM TASKS WHERE task_id=?"
        self.db_cursor.execute(task_query, [task_id])

        hashtask_query = "DELETE FROM HASHTASKS WHERE TASK_ID=?"
        self.db_cursor.execute(hashtask_query, [task_id])

    def fetch_tagged_tasks(self):
        query = "SELECT * FROM TASKS WHERE TASK_ID IN (SELECT task_id from hashtasks)"
        self.db_cursor.execute(query)

    def fetch_tag_by_task(self, hashtag_name):
        query = '''
                SELECT * FROM TASKS t
                JOIN HASHTASKS ht ON ht.task_id = t.task_id
                JOIN HASHTAGS h on h.hashtag_id = ht.hashtag_id
                where hashtag_name=?
                '''
        self.db_cursor.execute(query, [hashtag_name])

