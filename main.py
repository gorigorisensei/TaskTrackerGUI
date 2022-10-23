import tkinter
from tkinter import *
from tkinter import messagebox
import csv
from functools import partial
import pandas as pd
import customtkinter
import re
from datetime import date, timedelta

GREEN_HOVER = "#023020"
GREEN = "#008000"
BACKGROUND_COLOR = "#696969"
icon_font = ('roboto', 28)
large_font = ('roboto', 22)
medium_font = ('Verdana', 19)
small_font = ('Verdana', 10)
entry = ""
CENTER_X = 180
CENTER_Y = 280
SECOND_Y = 400
BUTTON_X = 620
EXAM_TXT_Y = 520
EXAM_BUTTON_X = 660
EXAM_BUTTON_Y = 700
BACK_BUTTON_X = 450
NEXT_BUTTON_X = 900
config_x = 350
button_y = 330
MAIN_MENU_GEO = "1000x650"
WIN_DEF_GEO = "1400x850"
example_text = ""
quarter_value = ""
GO = "Goal_Oriented"
COLLAB = "Collaboration"
INNO = "Innovation"
JK = "Job_Knowledge"
PAGE_NUM = 1
customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


### MAIN INTERFACE ###
def main_menu():
    global switch_var
    global card_title
    global card_word, feedback
    global screen_canvas
    global window
    global pf_button, config_button

    window = customtkinter.CTk()
    window.title("Task Tracker App")
    window.geometry(WIN_DEF_GEO)

    screen_canvas = Canvas(width=1400, height=850)
    card_title = screen_canvas.create_text(700, 100, text="Welcome to the Task Tracker App!",font=("roboto", 40),fill=('white'))
    card_word = screen_canvas.create_text(700, 200,
                                          text="First, press Goals button to add/edit goals",
                                          font=("roboto", 22, "bold"), fill='white')
    screen_canvas.pack()
    config_button = customtkinter.CTkButton(text="Goals", command=store_semester_ideas, text_font=icon_font, fg_color="orange", hover_color="#FFC000")
    config_button.place(x=config_x, y=button_y + 100)

    pf_button = customtkinter.CTkButton(text="Edit a Weekly Task List", command=edit_tasks,fg_color="#10AEB6", hover_color="#3610B6",text_font=icon_font )
    pf_button.place(x=config_x + 400, y=button_y + 100)

    window.mainloop()
def task_to_csv(categ,input):
    global INDEX_NUM
    df = pd.read_csv("data/tasks_list.csv")
    df.dropna(axis=0, how='all', inplace=True)
    thirty_days_after = (date.today()+timedelta(days=30)).isoformat()
    half_a_year = (date.today()+timedelta(days=183)).isoformat()
    try:
        entry_data = df.loc[INDEX_NUM, categ]

        #if the input is the same as the one in the list, skip
        if bool(re.search(f"{input}", str(entry_data))) == True:
            pass
        #go to the next index if the current line is not empty
        elif bool(re.search(f"\w+", str(entry_data))) == True:
            INDEX_NUM += 1
            task_to_csv(categ,input)
        else:
            if categ == "short_term":
                input = f"{input} due by {thirty_days_after}"
            else:
                input = f"{input} due by {half_a_year}"
            df.loc[INDEX_NUM, categ] = input
            df.to_csv("data/tasks_list.csv", index=False)

    except KeyError:
        if categ == "short_term":
            input = f"{input} due by {thirty_days_after}"
        else:
            input = f"{input} due by {half_a_year}"
        df.loc[INDEX_NUM, categ] = input
        df.to_csv("data/tasks_list.csv", index=False)


def read_task_data():
    global task_data
    with open('data/tasks_list.csv', 'r') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        task_data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    task_data[header].append(value)

                except KeyError:
                    task_data[header] = [value]

def show_task_list(category):
    # it will ignore the column that's empty and only shows everything from the list.
    global task_data
    task_list = []
    for data in task_data[category]:
        if data == "":
            pass
        else:
            task_list.append(data)
    return task_list



def clear_text():
    screen_canvas.itemconfig(submitted_text, text="")

def submit_goal_idea(category):
    global submitted_text
    global INDEX_NUM
    INDEX_NUM = 0

    task_submitted = st.get().replace(",", ";").replace("."," ")
    st.delete("0", tkinter.END)
    task_to_csv(categ=category, input=task_submitted)
    submitted_text = screen_canvas.create_text(700, 540, text=f"you have submitted a task!:  {task_submitted}",
                                                       font=("Ariel", 18, "bold"), fill='yellow')
    screen_canvas.after(1000, clear_text)



def not_saved_warning(category):
    user_entry = st.get()

    if user_entry == "":
        if category == "long_term":
            screen_canvas.nametowidget(f'.short_term').destroy()
            screen_canvas.nametowidget(f'.submit').destroy()
            for button in window.winfo_children():
                if type(button) == Button:
                    button.destroy()
                st.destroy()


                # fixes the focus issue
                window.update_idletasks()
                short_term_goals()
        else:
            screen_canvas.nametowidget(f'.submit').destroy()
            screen_canvas.nametowidget(f'.main').destroy()
            for button in window.winfo_children():
                if type(button) == Button:
                    button.destroy()
            read_task_data()
            try:
                task_list = show_task_list("short_term")
                for task in task_list:
                    try:
                        data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                        screen_canvas.nametowidget(f'.{data_name}').destroy()
                    except KeyError:
                        pass
            except KeyError:
                pass

            st.destroy()
            delete_d_buttons()
            # fixes the focus issue
            window.update_idletasks()

            back_to_main()
    # this should be only triggered if the input text was not empty!
    else:
        MsgBox = tkinter.messagebox.askquestion('Save data', 'Would you like to submit the data?',
                                                icon='warning')
        if MsgBox == 'yes':
            submit_goal_idea(category)
        else:
            if category == "long_term":
                short_term_goals()
            else:
                for button in window.winfo_children():
                    if type(button) == Button:
                        button.destroy()
                read_task_data()
                task_list = show_task_list("short_term")
                for task in task_list:
                    try:
                        data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                        screen_canvas.nametowidget(f'.{data_name}').destroy()
                    except KeyError:
                        pass

                st.destroy()
                # fixes the focus issue
                window.update_idletasks()
                delete_d_buttons()
                back_to_main()


def store_semester_ideas():
    global next_button
    global here_are
    global quarter_value
    global submit_button
    global st
    default_y = 130
    remove_x = 400

    config_button.destroy()
    pf_button.destroy()
    # fixes the focus issue
    window.update_idletasks()
    screen_canvas.itemconfig(card_word, text="", fill="white")

    screen_canvas.itemconfig(card_title, text=f"Set some long term goals: \n What do you want to achive in 6 months to a year from now?",
                             fill="white",font=("roboto", 33))
    num = 0

    st = customtkinter.CTkEntry(width=1000,height=100,textvariable=tkinter.StringVar(),text_font=medium_font)
    st.place(x=CENTER_X, y=EXAM_TXT_Y + 50)
    # fixes the focus issue
    window.update_idletasks()
    action_with_arg = partial(submit_goal_idea, "long_term")
    submit_button = customtkinter.CTkButton(text='Submit', command=action_with_arg,name="submit",text_font=large_font)
    submit_button.place(x=EXAM_BUTTON_X, y=EXAM_BUTTON_Y)

    action_with_arg_2 = partial(not_saved_warning, "long_term")
    next_button = customtkinter.CTkButton(text="Short Term Goals", command=action_with_arg_2, name="short_term",text_font=large_font)
    next_button.place(x=NEXT_BUTTON_X + 200, y=EXAM_BUTTON_Y)

    read_task_data()
    try:
        task_list = show_task_list("long_term")
        for task in task_list:
            data_name = str(task.lower().replace(",", "-").replace(".", "-"))
            customtkinter.CTkButton(text=f"{task}",
                                    name=f'{data_name}', fg_color="#2C3E50", text_font=("roboto", 25)).place(x=468,
                                                                                                             y=default_y + 100)
            customtkinter.CTkButton(text='delete',
                                    command=lambda temp=num, temp2=task, temp3="long_term": delete(temp, temp2, temp3),
                                    name=f'd_button{str(num)}', width=50, fg_color="#811331", hover_color="#641E16",
                                    text_font=("roboto", 25)).place(x=remove_x - 20, y=default_y + 100)
            default_y += 30
            num += 1
    except KeyError:
        pass




def short_term_goals():
    global submit_button
    global st
    delete_d_buttons()
    default_y = 130
    remove_x = 400
    num = 0
    try:
        goal_task_list = show_task_list("long_term")
        for task in goal_task_list:
            try:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass

    for button in window.winfo_children():
        if type(button) == Button:
            button.destroy()

    screen_canvas.itemconfig(card_title, text=f"Set some short term goals: \n What do you want to achieve in a month?",
                             fill="white", font=("roboto", 33))
    st = customtkinter.CTkEntry(width=1000, height=100, textvariable=tkinter.StringVar(), text_font=medium_font)
    st.place(x=CENTER_X, y=EXAM_TXT_Y + 50)
    # fixes the focus issue
    window.update_idletasks()
    action_with_arg = partial(submit_goal_idea, "short_term")
    submit_button = customtkinter.CTkButton(text='Submit', command=action_with_arg, name="submit", text_font=large_font)
    submit_button.place(x=EXAM_BUTTON_X, y=EXAM_BUTTON_Y)

    action_with_arg_2 = partial(not_saved_warning, "short_term")
    main_manu_button = customtkinter.CTkButton(text="Back to Main Manu", command=action_with_arg_2, name="main",
                                          text_font=large_font)
    main_manu_button.place(x=NEXT_BUTTON_X + 200, y=EXAM_BUTTON_Y)
    read_task_data()
    try:
        task_list = show_task_list("short_term")
        for task in task_list:
            data_name = str(task.lower().replace(",", "-").replace(".", "-"))
            customtkinter.CTkButton(text=f"{task}",
                                    name=f'{data_name}', fg_color="#2C3E50", text_font=("roboto", 20)).place(x=468,
                                                                                                             y=default_y + 100)
            customtkinter.CTkButton(text='delete',
                                    command=lambda temp=num, temp2=task, temp3="long_term": delete(temp, temp2, temp3),
                                    name=f'd_button{str(num)}', width=50, fg_color="#811331", hover_color="#641E16",
                                    text_font=("roboto", 20)).place(x=remove_x, y=default_y + 100)
            default_y += 30
            num += 1
    except KeyError:
        pass






def back_to_main():
    global config_button
    global edit_progress_button, pf_button, generate_html_button
    global config_img, edit_p_img, task_image, generate_image
    try:
        screen_canvas.nametowidget(f'.main').destroy()
    except KeyError:
        pass

    screen_canvas.itemconfig(card_title, text="Welcome to the Task Tracker App!",
                             fill="white")
    screen_canvas.itemconfig(card_word, text="Press the config button to edit some settings (if this is the first time opening the app, do this)",
                             fill="white")
    config_button = customtkinter.CTkButton(text="Goals", command=store_semester_ideas, text_font=icon_font,
                                            fg_color="orange", hover_color="#FFC000")
    config_button.place(x=config_x, y=button_y + 100)

    pf_button = customtkinter.CTkButton(text="Edit a Weekly Task List", command=edit_tasks, fg_color="#10AEB6",
                                        hover_color="#3610B6", text_font=icon_font)
    pf_button.place(x=config_x + 400, y=button_y + 100)


### REMOVE TASKS SECTION ###
def edit_tasks():
    global remove_button
    global add_task_button
    global task_next_button
    read_task_data()
    screen_canvas.itemconfig(card_title, text="Weekly Task List: Monday", fill="white")
    screen_canvas.itemconfig(card_word, text="", fill="white")
    config_button.destroy()
    pf_button.destroy()
    current_day = "Monday"

    task_management(current_day)
def day_task_to_csv(categ, input):
    global INDEX_NUM
    df = pd.read_csv("data/day_task.csv")
    df.dropna(axis=0, how='all', inplace=True)
    df.to_csv("data/day_task.csv", index=False)
    try:
        entry_data = df.loc[INDEX_NUM, categ]

        # if the input is the same as the one in the list, skip
        if bool(re.search(f"{input}", str(entry_data))) == True:
            pass
        # go to the next index if the current line is not empty
        elif bool(re.search(f"\w+", str(entry_data))) == True:
            INDEX_NUM += 1
            day_task_to_csv(categ, input)
        else:
            df.loc[INDEX_NUM, categ] = input
            df.to_csv("data/day_task.csv", index=False)

    except KeyError:

        df.loc[INDEX_NUM, categ] = input
        df.to_csv("data/day_task.csv", index=False)


def submit_day_task(current_day):
    global submitted_text
    global INDEX_NUM
    INDEX_NUM = 0

    task_submitted = st.get().replace(",", ";").replace(".", " ")
    st.delete("0", tkinter.END)
    day_task_to_csv(categ=current_day, input=task_submitted)
    submitted_text = screen_canvas.create_text(700, 540, text=f"you have submitted a task!:  {task_submitted}",
                                               font=("Ariel", 18, "bold"), fill='yellow')
    screen_canvas.after(1000, clear_text)



def read_day_task_data():
    global task_data
    with open('data/day_task.csv', 'r') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        task_data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    task_data[header].append(value)

                except KeyError:
                    task_data[header] = [value]

def delete_both_tasks():
    read_task_data()
    try:
        task_list = show_task_list("long_term")
        for task in task_list:
            try:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
        task_list = show_task_list("short_term")
        for task in task_list:
            try:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass


def task_management(current_day):
    global task_next_button
    global task
    global num
    global st
    try:
        st.destroy()
    except NameError:
        pass
    delete_both_tasks()
    delete_d_buttons()
    screen_canvas.itemconfig(card_title, text=f"Weekly Task List: {current_day}", fill="white")

    if current_day == "Monday":
        next_day = "Tuesday"
    elif current_day == "Tuesday":
        next_day = "Wednesday"
        last_day = "Monday"
    elif current_day == "Wednesday":
        last_day = "Tuesday"
        next_day = "Thursday"
    elif current_day == "Thursday":
        last_day = "Wednesday"
        next_day = "Friday"
    elif current_day == "Friday":
        last_day = "Thursday"
        next_day = "Saturday"
    elif current_day == "Saturday":
        last_day = "Friday"
        next_day = "Sunday"
    else:
        last_day = "Saturday"

    num = 0
    read_day_task_data()


    st = customtkinter.CTkEntry(width=1000, height=100, textvariable=tkinter.StringVar(), text_font=medium_font)
    st.place(x=CENTER_X, y=EXAM_TXT_Y + 50)
    # fixes the focus issue
    window.update_idletasks()
    action_with_arg = partial(submit_day_task, current_day)
    submit_button = customtkinter.CTkButton(text='Submit', command=action_with_arg, name="submit", text_font=large_font)
    submit_button.place(x=EXAM_BUTTON_X, y=EXAM_BUTTON_Y)


    if current_day == "Sunday":
        task_next_button = customtkinter.CTkButton(text="Back to Main", command=back_to_main_from_task, text_font=large_font,
                                                   name="next")
        task_next_button.place(x=NEXT_BUTTON_X + 150, y=EXAM_BUTTON_Y)
        action_with_arg_4 = partial(go_back_day, last_day, current_day)
        note_back_button = customtkinter.CTkButton(text="Go Back", command=action_with_arg_4, name="back",
                                                   text_font=large_font)
        note_back_button.place(x=NEXT_BUTTON_X - 800, y=EXAM_BUTTON_Y)

    else:
        action_with_arg_3 = partial(go_to_next_day, str(next_day), current_day)
        task_next_button = customtkinter.CTkButton(text=next_day, command=action_with_arg_3,text_font=large_font,name="next")
        task_next_button.place(x=NEXT_BUTTON_X + 150, y=EXAM_BUTTON_Y)
        if current_day == "Tuesday" or current_day == "Wednesday" or current_day == "Thursday" or current_day == "Friday" or current_day == "Saturday":
            action_with_arg_4 = partial(go_back_day, last_day, current_day)
            note_back_button = customtkinter.CTkButton(text="Go Back", command=action_with_arg_4, name="back",
                                                       text_font=large_font)
            note_back_button.place(x=NEXT_BUTTON_X - 800, y=EXAM_BUTTON_Y)
        else:
            try:
                screen_canvas.nametowidget(f'.back').destroy()
            except KeyError:
                pass

    action_with_arg_19 = partial(add_goal_tasks_from_day, "long_term", current_day)
    add_tasks = customtkinter.CTkButton(text="Add Goals", command=action_with_arg_19,text_font=large_font, name="add")
    add_tasks.place(x=NEXT_BUTTON_X - 50, y=EXAM_BUTTON_Y)
    action_with_arg_30 = partial(show_long_term_goals, current_day)
    customtkinter.CTkButton(text="Show Long Term Goals", command=action_with_arg_30, text_font=large_font, name="show_l").place(x=NEXT_BUTTON_X - 600, y=EXAM_BUTTON_Y)

    default_y = 130
    remove_x = 370
    num = 0
    try:
        task_list = show_task_list(current_day)
        try:
            for task in task_list:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                customtkinter.CTkButton(text=f"{task}",
                                        name=f'{data_name}', fg_color="#2C3E50", text_font=("roboto", 20)).place(x=468,
                                                                                                                 y=default_y + 100)
                customtkinter.CTkButton(text='Complete',
                                        command=lambda temp=num, temp2=task, temp3=current_day: delete(temp, temp2,
                                                                                                       temp3),
                                        name=f'd_button{str(num)}', width=70, height=33, fg_color=GREEN,
                                        hover_color=GREEN_HOVER, text_font=("roboto", 20)
                                        ).place(x=remove_x, y=default_y + 100)
                default_y += 30
                num += 1
        except KeyError:
            pass
    except KeyError:
        pass




def delete_current_day_tasks(current_day):
    read_day_task_data()
    try:
        goal_task_list = show_task_list(current_day)
        for task in goal_task_list:
            data_name = str(task.lower().replace(",", "-").replace(".", "-"))
            try:

                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass

def go_to_next_day(next_day,last_day):
    st.destroy()

    try:
        delete_current_tasks(last_day)
    except KeyError:
        pass
    task_management(next_day)

def go_back_day(last_day, next_day):
    st.destroy()
    try:
        delete_current_tasks(next_day)
    except KeyError:
        pass
    task_management(last_day)

def show_short_term_goals(current_day):
    delete_d_buttons()
    read_task_data()
    try:
        task_list = show_task_list("long_term")
        for task in task_list:
            try:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.next').destroy()
        screen_canvas.nametowidget(f'.back').destroy()
    except KeyError:
        pass

    action_with_arg_30 = partial(show_long_term_goals, current_day)
    customtkinter.CTkButton(text="Show Long Term Goals", command=action_with_arg_30, text_font=large_font,
                            name="show_l").place(x=NEXT_BUTTON_X - 600, y=EXAM_BUTTON_Y)
    try:
        screen_canvas.nametowidget(f'.show_s').destroy()
    except KeyError:
        pass

    try:
        action_with_arg_31 = partial(task_management, current_day)
        customtkinter.CTkButton(text="Show Tasks", command=action_with_arg_31, name="back",
                                text_font=large_font).place(x=NEXT_BUTTON_X - 800, y=EXAM_BUTTON_Y)
        goal_task_list = show_task_list("short_term")
        default_y = 130
        remove_x = 400
        num = 0

        for task in goal_task_list:
            data_name = str(task.lower().replace(",", "-").replace(".", "-"))
            customtkinter.CTkButton(text=f"{task}",
                                        name=f'{data_name}',fg_color="#2C3E50", text_font=("roboto",20)).place(x=468, y=default_y + 100)
            customtkinter.CTkButton(text='delete', command=lambda temp=num, temp2=task, temp3="short_term": delete(temp, temp2, temp3),
                               name=f'd_button{str(num)}',width=70, height=33,fg_color="#811331", hover_color="#641E16",text_font=("roboto",20)
                                        ).place(x=remove_x, y=default_y+ 100)
            default_y += 30
            num += 1

    except KeyError:
        pass


def show_long_term_goals(current_day):
    delete_d_buttons()
    delete_current_day_tasks(current_day)
    read_task_data()
    try:
        screen_canvas.nametowidget(f'.next').destroy()
        screen_canvas.nametowidget(f'.back').destroy()
    except KeyError:
        pass
    try:
        task_list = show_task_list("short_term")
        for task in task_list:
            try:
                data_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{data_name}').destroy()
            except KeyError:
                pass
    except KeyError: pass


    try:
        screen_canvas.nametowidget(f'.show_l').destroy()
    except KeyError:
        pass
    action_with_arg_30 = partial(show_short_term_goals, current_day)

    customtkinter.CTkButton(text="Show Short Term Goals", command=action_with_arg_30, text_font=large_font,
                            name="show_s").place(x=NEXT_BUTTON_X - 600, y=EXAM_BUTTON_Y)
    action_with_arg_31 = partial(task_management, current_day)
    customtkinter.CTkButton(text="Show Tasks", command=action_with_arg_31, name="back",
                            text_font=large_font).place(x=NEXT_BUTTON_X - 800, y=EXAM_BUTTON_Y)

    try:
        goal_task_list = show_task_list("long_term")
        default_y = 130
        remove_x = 400
        num = 0

        for task in goal_task_list:
            data_name = str(task.lower().replace(",", "-").replace(".", "-"))
            customtkinter.CTkButton(text=f"{task}",
                                        name=f'{data_name}',fg_color="#2C3E50", text_font=("roboto",20)).place(x=468, y=default_y + 100)
            customtkinter.CTkButton(text='delete', command=lambda temp=num, temp2=task, temp3="long_term": delete(temp, temp2, temp3),
                               name=f'd_button{str(num)}',width=70, height=33,fg_color="#811331", hover_color="#641E16",text_font=("roboto",20)
                                        ).place(x=remove_x, y=default_y+ 100)
            default_y += 30
            num += 1
    except KeyError:
        pass

def delete(num,task, current_category):
    MsgBox = tkinter.messagebox.askquestion('Save data', f'Do you really want to remove the task: {task}?',
                                            icon='warning')
    if MsgBox == 'yes':
        screen_canvas.nametowidget(f'.d_button{num}').destroy()
        task_name = str(task.lower().replace(",", "-").replace(".", "-"))
        screen_canvas.nametowidget(f'.{task_name}').destroy()
        remove_task(current_category, task)

    else:
        pass


def add_goal_tasks_from_day(category, current_day):
    global here_are
    global example_text_display
    global st
    global submit_button_2
    global next_button_2

    delete_both_tasks()
    read_day_task_data()

    try:
        goal_task_list = show_task_list(current_day)
        for task in goal_task_list:
            try:
                task_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{task_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass

    try:
        st.destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.show_l').destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.show_s').destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.next').destroy()
    except KeyError:
        pass


    for label in window.winfo_children():
        if type(label) == Label:  # just Label since you used a wildcard import to import tkinter
            label.destroy()
    for button in window.winfo_children():
        if type(button) == Button:
            button.destroy()
    read_task_data()
    try:
        goal_task_list = show_task_list(category)
        for task in goal_task_list:
            try:
                task_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{task_name}').destroy()
            except KeyError:
                pass
    except KeyError:
        pass

    screen_canvas.nametowidget(f'.add').destroy()


    delete_d_buttons()
    try:
        screen_canvas.nametowidget(f'.back').destroy()
    except KeyError:
        pass

    store_semester_ideas()

def add_goal_tasks(category):
    global here_are
    global example_text_display
    global st
    global submit_button_2
    global next_button_2

    try:
        st.destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.show_l').destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.show_s').destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.next').destroy()
    except KeyError:
        pass


    for label in window.winfo_children():
        if type(label) == Label:  # just Label since you used a wildcard import to import tkinter
            label.destroy()
    for button in window.winfo_children():
        if type(button) == Button:
            button.destroy()
    read_task_data()
    goal_task_list = show_task_list(category)
    for task in goal_task_list:
        try:
            task_name = str(task.lower().replace(",", "-").replace(".", "-"))
            screen_canvas.nametowidget(f'.{task_name}').destroy()
        except KeyError:
            pass
    screen_canvas.nametowidget(f'.add').destroy()


    delete_d_buttons()
    try:
        screen_canvas.nametowidget(f'.back').destroy()
    except KeyError:
        pass

    store_semester_ideas()

def back_to_main_from_task():
    st.destroy()

    for label in window.winfo_children():
        if type(label) == Label:  # just Label since you used a wildcard import to import tkinter
            label.destroy()
    for button in window.winfo_children():
        if type(button) == Button:
            button.destroy()
    try:
        screen_canvas.nametowidget(f'.show_l').destroy()
    except KeyError:
        pass
    try:
        screen_canvas.nametowidget(f'.show_s').destroy()
    except KeyError:
        pass
    screen_canvas.nametowidget(f'.submit').destroy()
    read_day_task_data()
    try:
        goal_task_list = show_task_list("Sunday")
        for task in goal_task_list:
            try:
                task_name = str(task.lower().replace(",", "-").replace(".", "-"))
                screen_canvas.nametowidget(f'.{task_name}').destroy()
            except KeyError:
                pass

    except KeyError:
        pass

    delete_d_buttons()
    screen_canvas.nametowidget(f'.add').destroy()
    screen_canvas.nametowidget(f'.back').destroy()
    screen_canvas.nametowidget(f'.next').destroy()
    window.update_idletasks()
    back_to_main()



def remove_task(category, task):
    df = pd.read_csv("data/day_task.csv")
    task_value = task
    for num in range(0,200):

        try:

            if df.loc[num, category] == task_value:
                df.loc[num, category] = ""
            df.to_csv("data/day_task.csv", index=False)
        except KeyError:
            pass


def entry_pop_up(entry):
    tkinter.messagebox.showinfo(title="Entry", message=f"{entry}")

def delete_current_tasks(category):

    goal_task_list = show_task_list(category)
    for task in goal_task_list:
        data_name = str(task.lower().replace(",", "-").replace(".", "-"))
        try:

            screen_canvas.nametowidget(f'.{data_name}').destroy()
        except KeyError:
            pass

def destroy_labels():
    for label in window.winfo_children():
        if type(label) == Label:  # just Label since you used a wildcard import to import tkinter
            label.destroy()


def delete_d_buttons():

    for num in range(0,100):
        try:
            screen_canvas.nametowidget(f'.d_button{num}').destroy()


        except KeyError:
            pass


main_menu()

