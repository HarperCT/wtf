import threading
import time

def task_one():
    print("Task One: Starting...")
    time.sleep(2)  # Simulate some work
    print("Task One: Finished.")

def task_two():
    print("Task Two: Starting...")
    time.sleep(1)  # Simulate some work
    print("Task Two: Finished.")

if __name__ == "__main__":
    print("Main program: Starting threads.")
    
    t1 = threading.Thread(target=task_one)
    t2 = threading.Thread(target=task_two)
        
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    # dump_output_to_zip
    print("Main program: All threads completed.")