import subprocess
import threading

# Function to copy database from one server to another
def copy_database(source_host, source_user, source_password, source_db, target_host, target_user, target_password, target_db):
    # Command to dump database from source server
    # Remove --single-transaction flag from the dump_cmd
    dump_cmd = [
        'mysqldump',
        '-h', source_host,
        '-u', source_user,
        f'--password={source_password}',
        source_db
    ]

    # Command to import dumped database into target server
    import_cmd = [
        'mysql',
        '-h', target_host,
        '-u', target_user,
        f'--password={target_password}',
        target_db
    ]

    # Execute commands using subprocess
    dump_process = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE)
    import_process = subprocess.Popen(import_cmd, stdin=dump_process.stdout)
    dump_process.stdout.close()  # Close the output stream to allow dump_process to finish
    import_process.communicate()

# Function to start database copy process using threading
def start_copy_process(source_host, source_user, source_password, source_db, target_host, target_user, target_password, target_db):
    thread = threading.Thread(
        target=copy_database,
        args=(source_host, source_user, source_password, source_db, target_host, target_user, target_password, target_db)
    )
    thread.start()
    return thread

if __name__ == "__main__":
    # Source server details
    source_host = ''
    source_user = ''
    source_password = ''
    source_db = ''

    # Target server details
    target_host = ''
    target_user = ''
    target_password = ''
    target_db = ''

    # Start the database copy process using threading
    copy_thread = start_copy_process(source_host, source_user, source_password, source_db, target_host, target_user, target_password, target_db)
    copy_thread.join()

    print("Database copy process completed.")
