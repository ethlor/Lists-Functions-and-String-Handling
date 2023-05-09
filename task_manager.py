#=====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date
import datetime

#====Login Section====

username = input("Enter username: ")
password = input("Enter password: ")
generate = False

# opening file
with open('user.txt','r') as user_file:
    user_names = []
    pass_words = []

    # readinga  lines of the file and seperating inforamtion and stroing them in appropriate variables
    for line in user_file:
        # removing \n commands
        temp = line.strip()
        # spliting the line into differente information 
        temp = temp.split(", ")
        # adding information to a appropriate list. 
        # first item on list which is the username goes into the username list 
        user_names.append(temp[0])
        pass_words.append(temp[1])
    
    # setting a boolean to true
    check = True
    # while the check has to be done the loop continues
    while check:
        # checking if the username is in the txt file(username list)
        if username in user_names:
            if password in pass_words:
                # boolean gets set to false. check does not need to be done to loop wont continue
                check = False
            else:
                password= input("\nIncorrect password entered please try again: ")
        else:
            # re-asks for username and password
            username = input("\nIncorrect username entered.\nEnter username:  ")
            password = input("Enter password: ")

#===add user to database====
def reg_user(username1):
    with open('user.txt','r') as user_file:
        user_names = []
        for line in user_file:
            temp = line.strip()
            temp = temp.split(", ")
            user_names.append(temp[0])
    if username1 == "admin":
        # asking for informatio not update users.txt
        new_username=input("\nEnter new username: ")
        check = True
        while check:
            if new_username in user_names:
                new_username = input("Username already exists please enter new username: ")
            else:
                check = False

        new_password = input("Enter new password: ")
        confirm_password = input("confirm password: ")
        # making sure that confiramtion password enterd match new password enterd
        while new_password != confirm_password:
            new_password = input("\nInvalid confirmation password\nEnter password: ")
            confirm_password = input("Confirm password: ")          
            
        # open txt file and insert information in correct format
        with open('user.txt','a') as user_file:
            user_file.write(f"\n{new_username}, {new_password}")
        
    else:
        print("\nYou cannot perform that option!")


def add_task():
    # asking for information
    username_task = input("\nEnter username: ")
    title = input("Enter title: ")
    description = input("Enter task description: ")
    due_date = input("Enter task due date(write in this format:01 jan 1999): ")
    # method to get current date 
    today_date = date.today()
    # stroring in correct format
    month = today_date.strftime("%B")
    month = month[0:3]
    year = today_date.strftime("%Y")
    day = today_date.strftime("%d")
    today = day+" "+month+" " +year 

    # open txt file tasks and write inforamtion in correct format
    with open('tasks.txt','a') as task_file:
        task_file.write(f"\n{username_task}, {title}, {description}, {today}, {due_date}, No")#\n for new line


def view_all():
    # open txt tasks to only read from it
    with open('tasks.txt','r') as task_file:
        for line in task_file:
            temp = line.strip()
            temp = temp.split(", ")
            print("------------------------------------------------------")
            # display in correct format
            print(f"Task:\t\t\t{temp[1]}\nAssigned to:\t\t {temp[0]}\nDate assigned:\t\t{temp[3]}\nDue date:\t\t{temp[4]}\nTask complete?\t\t{temp[5]}\nTask description:\t{temp[2]}")
            print("------------------------------------------------------")


def view_mine():
    with open('tasks.txt','r') as task_file:
        num_tasks = 0
        for line in task_file:
            temp= line.strip()
            temp = temp.split(", ")
             # count which task iteration of loop is on
            # check if username on task is same as username of logged in person
            if temp[0] == username:
                num_tasks += 1
                print("------------------------------------------------------")
                # display in correct format
                print(f"No:{num_tasks}\nTask:\t\t\t{temp[1]}\nAssigned to:\t\t {temp[0]}\nDate assigned:\t\t{temp[3]}\nDue date:\t\t{temp[4]}\nTask complete?\t\t{temp[5]}\nTask description:\t{temp[2]}")
                print("------------------------------------------------------") 
    
# takes in username and returns dictionary with pos int key as tasks for specific user and negative int keys as other tasks 
def task_list(username2):
    num1 = 0
    num2 =0
    with open('tasks.txt','r') as task_file:
        task = {}
        for line in task_file:
            temp = line.strip()
            temp = temp.split(", ")
            if temp[0]==username2:
                # incrimants pos int for key no.
                num1+=1
                task[num1] = temp
            else:
                num2 = num2 -1
                task[num2] = temp
    # print(task)remover
    return(task)

# overwrites data in file to certain format of data
def save_task(task_dict):
    task_string = ""
    task_temp = []
    task_string_print = ""
    for value in task_dict.values():
        task_string = ", ".join(value)
        task_temp.append(task_string) 
        task_string_print = "\n".join(task_temp)
    with open('tasks.txt','w') as task_file:
        task_file.write(task_string_print)


def date_overdue(due_date):
    due_date = due_date.strip()
    # changing date to a readible format by programme
    date = datetime.datetime.strptime(due_date, '%d %b %Y')
    # comparing todays date to due date
    if date < datetime.datetime.today():
        overdue_time = True
    else:
        overdue_time = False
    # return a boolean value
    return(overdue_time)

def generate_overview():
        tasks = task_list(username)
        num_tasks = len(tasks)
        incomplete=0
        complete=0
        overdue = 0
        task_overview = ""
        for value in tasks.values():# checks all tasks
            if value[5]=="Yes": # check if task is marked yes
                complete += 1 
            else:
                incomplete +=1
                dued_date = value[4]
                if date_overdue(dued_date): # check the due date
                    overdue+=1
        perc_incomplete = (incomplete/num_tasks) *100
        perc_overdue = (overdue / num_tasks) *100
        # foramt(number of tasks,complete tasks,incomplete tasks,percentage incomplete,percentage overdue)
        task_overview = ("{}, {}, {}, {}, {}, {}\n"
                        .format(num_tasks,complete,incomplete,overdue,perc_incomplete,perc_overdue))
        with open('task_overview.txt','w') as task_overview_file:
                task_overview_file.write(task_overview)

        with open('user.txt','r') as user_file:
            user_overview ="" 
            for line in user_file: #  repeats for each user
                num_tasks = 0
                incomplete=0
                complete=0
                overdue = 0
                temp = line.strip()
                temp = temp.split(", ")
                # get dict of task for user in iteration(pos int key:user is assigned to task)
                tasks = task_list(temp[0]) 
                # is 1 is a key means that there is tasks for user
                if 1 in tasks:
                    for i in range(len(tasks.values())):
                        if (i+1) in tasks:   # if number is a key in dict so dont go out of range
                            if tasks[i+1][5]=="Yes":    # completed marked yes
                                complete +=1
                                num_tasks +=1
                            else:
                                num_tasks +=1
                                incomplete +=1
                                dued_date = tasks[i+1][4]
                                if date_overdue(dued_date):
                                   overdue+=1
                    # calulations
                    perc_complete = (complete/num_tasks) *100
                    perc_incomplete = (incomplete/num_tasks) * 100
                    perc_overdue = (overdue/num_tasks) *100
                    perc_assigned = (num_tasks/len(tasks)) * 100
                    # format(username,number of tasks,percentage assigned,percentage complete,percentage overdue) comcatanate each user
                    user_overview = ("{}{}, {}, {}, {}, {}, {}\n"
                                     .format(user_overview,temp[0],num_tasks,perc_assigned,perc_complete,perc_incomplete,perc_overdue))
                else: user_overview = ("{}{}, 0, 0, 0, 0, 0\n"
                                     .format(user_overview,temp[0]))
            # saves all users and their inifomration to txt file
            with open('user_overview.txt','w') as user_overview_file:
                user_overview_file.write(user_overview)


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    if username == "admin":
        menu = menu = input("\nSelect one of the following Options below:\nr - Registering a user\na - Adding a task\nva - View all tasks\nvm - view my task\ngr-generate reports\nds - display statistics\ne - Exit\n: ").lower()
    else:
        menu = input("\nSelect one of the following Options below:\nr - Registering a user\na - Adding a task\nva - View all tasks\nvm - view my task\ne - Exit\n: ").lower()
    

    # checking the option menu
    if menu == 'r':   
        reg_user(username)


    elif menu == 'a':
        add_task()
        

    elif menu == 'va':
        view_all()
                                   
        
    elif menu == 'vm':
        view_mine()
        task_num = int(input("Enter task number to alter or -1 to return to menu: "))
        if task_num == -1:
            pass
        else:
            user_task = task_list(username) #dict of tasks
            option = input("enter 'edit' to edit task or 'mark' to mark task complete: ")
            if option == "mark":
                if task_num in user_task:
                    user_task[task_num][5] = " Yes" # change task number at index 5 of list to yes
                    save_task(user_task) # print edited dict to txt file
            else:
                if task_num in user_task:    
                    if user_task[task_num][5] == "No": # checkis task is complete
                        change = input("enter 'date' to change due date or 'user' to change the person assigned to task")
                        if change == "user": # checking what user wants to change
                            changed_username = input("enter new assigned username for task ")
                            user_task[task_num][0] = changed_username # change username assigned to task
                            save_task(user_task)
                        else:
                            changed_date = input("Enter task new due date(write in this format:01 jan 1999):") 
                            user_task[task_num][4]= changed_date
                            save_task(user_task)
                          
           
    elif menu =="gr" :
        generate = True
        generate_overview()


    elif menu == "ds":
        if generate:# file has beem generated
            with open('task_overview.txt','r') as task_overview_file:
                for line in task_overview_file:
                    temp = line.strip()
                    temp = temp.split(", ")
                    print("------------------------------------------------------")
                    # display in correct format
                    print(f"No. tasks:\t\t{temp[0]}\nNo. complete:\t\t{temp[1]}\nNo. incomplete:\t\t{temp[2]}\nNo. overdue:\t\t{temp[3]}\nPercentage incomplete:\t{temp[4]}\nPercentage overdue:\t{temp[5]}")
                    print("------------------------------------------------------")
            with open('user_overview.txt','r') as user_overview_file:
                for line in user_overview_file:
                    temp = line.strip()
                    temp = temp.split(", ")
                    print("------------------------------------------------------")
                    # display in correct format
                    print(f"user:\t{temp[0]}\nNo. tasks assigned:\t{temp[1]}\nPercentage assigned:\t{temp[2]}\nPercentage complete:\t{temp[3]}\nPercentage incomplete:\t{temp[4]}\nPercentage overdue:\t{temp[5]}")
                    print("------------------------------------------------------")
        else:
            generate_overview()
            with open('task_overview.txt','r') as task_overview_file:
                for line in task_overview_file:
                    temp = line.strip()
                    temp = temp.split(", ")
                    print("------------------------------------------------------")
                    # display in correct format
                    print(f"No. tasks\t{temp[0]}\nNo. complete tasks\t{temp[1]}\nNo. incomplete\t{temp[2]}\nNo. overdue:\t{temp[3]}\nPercentage incomplete:\t{temp[4]}\nPercentage overdue:\t{temp[5]}")
                    print("------------------------------------------------------")
            with open('user_overview.txt','r') as user_overview_file:
                for line in user_overview_file:
                    temp = line.strip()
                    temp = temp.strip(", ")
                    print("------------------------------------------------------")
                    # display in correct format
                    print(f"user:\t{temp[0]}\nNo. tasks assigned:\t{temp[1]}\nPercentage assigned:\t{temp[2]}\nPercentage complete:\t{temp[3]}\nPercentage incomplete:\t{temp[4]}\nPercentage overdue:\t{temp[5]}")
                    print("------------------------------------------------------")


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")