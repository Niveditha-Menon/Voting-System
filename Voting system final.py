from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import mysql.connector as mycon
import matplotlib.pyplot as plt
conn = mycon.connect(host="localhost", user="root",password="mypass", database="votes")  # main database
cursor = conn.cursor()  # main cursor


def pollpage(name):  # page for polling
    def proceed():
        pd = mycon.connect(host="localhost", user="root",password="mypass", database="votes")  # poll database
        pcursor = pd.cursor()
        chose = choose.get()
        print(chose)
        command = 'update polling set votes=votes+1 where name=%s'
        pcursor.execute(command, (chose,))
        pd.commit()
        messagebox.showinfo('Success!', 'VOTE CASTED!')
    choose = StringVar()
    names = []
    pd = mycon.connect(host="localhost", user="root",password="mypass", database="votes")  # poll database
    pcursor = pd.cursor()  # poll cursor

    pcursor.execute('select name from polling where pollname="'+name+'"')
    data = pcursor.fetchall()
    for i in range(len(data)):
        data1 = data[i]
        ndata = data1[0]
        names.append(ndata)
    print(names)
    ppage = Toplevel()
    ppage.geometry('300x300')
    ppage.title('Poll')

    Label(ppage, text='Vote for any one person!').grid(row=1, column=3)
    for i in range(len(names)):
        Radiobutton(ppage, text=names[i], value=names[i], variable=choose).grid(row=2+i, column=1)
    Button(ppage, text='Vote',command=proceed).grid(row=2+i+1, column=2)


def polls(age):  # mypolls
    def proceed(name):
        global plname
        plname = psel.get()
        if plname == '-select-':
            return messagebox.showerror('Error', 'select poll')
        else:
            mpolls.destroy()
            pollpage(name)
    age = int(age)
    if age < 18:
        messagebox.showerror('Error', 'YOU ARE NOT ELIGIBLE TO VOTE')
    else:
        cursor.execute('select name from poll')
        data = cursor.fetchall()
        pollnames = ['-select-']
        for i in range(len(data)):
            data1 = data[i]
            ndata = data1[0]
            pollnames.append(ndata)
        psel = StringVar()
        mpolls = Toplevel()
        mpolls.geometry('270x200')
        mpolls.title('Voting page')
        Label(mpolls, text='Select Poll',font='Centaur 12 bold',bg='pink').grid(row=1, column=3)
        select = ttk.Combobox(mpolls, values=pollnames,state='readonly', textvariable=psel)
        select.grid(row=2, column=3)
        select.current(0)
        Button(mpolls, text='Proceed', command=lambda: proceed(select.get())).grid(row=2, column=4)


def checkAge():
    agepoll = Toplevel()
    agepoll.geometry('270x200')
    Label(agepoll, text="Please enter your age to proceed:").grid(row=1, column=1)
    t1 = Entry(agepoll)
    t1.grid(row=1, column=2)
    Button(agepoll, text="check", command=lambda: polls(t1.get())).grid(row=2, column=1)


def create():
    def proceed():
        global pcursor
        pname = name.get()  # pollname
        can = cname.get()
        print(pname, can)  # candidatename
        if pname == '':
            return messagebox.showerror('Error', 'Enter poll name')
        elif can == '':
            return messagebox.showerror('Error', 'Enter candidates')
        else:
            candidates = can.split(',')  # candidate list
            command = "insert into poll values (%s)"
            cursor.execute(command, (pname,))
            conn.commit()
            pd = mycon.connect(host="localhost", user="root",password="mypass", database="votes")  # poll database
            pcursor = pd.cursor()  # poll cursor
            for i in range(len(candidates)):
                command = "insert into polling (name,votes,pollname) values (%s, %s, '"+pname+"')"
                data = (candidates[i], 0)
                pcursor.execute(command, data)
                pd.commit()
            pd.close()
            messagebox.showinfo('Success!', 'Poll Created')
            cr.destroy()

    name = StringVar()
    cname = StringVar()
    cr = Toplevel()
    cr.geometry('500x400')
    cr.title('Create a new poll')
    Label(cr, text='Enter Details', font='Centaur 12 bold',bg='pink').grid(row=1, column=2)
    Label(cr, text='Enter Poll name: ').grid(row=2, column=1)
    Entry(cr, width=45, textvariable=name).grid(row=2, column=2)  # poll name
    Label(cr, text='(eg: Panchayat election)').place(x=354, y=25)
    Label(cr, text='ENTER CANDIDATE NAMES: ').grid(row=3, column=1)
    Entry(cr, width=45, textvariable=cname).grid(row=3, column=2)  # candidate name
    Label(cr, text='Note: Enter the candidate names one by one by putting commas').grid(row=4, column=2)
    Label(cr, text='eg: candidate1,candate2,candidate3....').grid(row=6, column=2)
    Button(cr, width=50, text='Proceed', command=proceed).grid(row=7, column=2)


def selpl():  # pollresults
    def results():
        sel = sele.get()  # selected option
        if sel == '-select-':
            return messagebox.showerror('Error', 'Select Poll')
        else:
            pl.destroy()

            def project():
                names = []
                votes = []
                for i in range(len(r)):
                    data = r[i]
                    names.append(data[0])
                    votes.append(data[1])
                    plt.title('Poll Result')
                plt.pie(votes, labels=names, autopct='%1.1f%%',shadow=True, startangle=140)
                plt.axis('equal')
                plt.show()

            res = Toplevel()  # result-page
            res.geometry('300x300')
            res.title('Results!')
            Label(res, text='Here is the Result!',font='Centaur 12 bold').grid(row=1, column=2)
            con = mycon.connect(host="localhost", user="root",passwd="mypass", database="votes")
            pcursor = con.cursor()
            pcursor.execute('select name,votes from polling where pollname="'+sel+'"')
            r = pcursor.fetchall()  # data-raw
            for i in range(len(r)):
                data = r[i]
                Label(res, text=data[0]+': '+str(data[1]) +' votes').grid(row=2+i, column=1)
            Button(res, text='Project Results',command=project).grid(row=2+i+2, column=2)

    cursor.execute('select name from poll')
    data = cursor.fetchall()
    pollnames = ['-select-']
    for i in range(len(data)):
        data1 = data[i]
        ndata = data1[0]
        pollnames.append(ndata)
    sele = StringVar()
    pl = Toplevel()
    pl.geometry('350x100')
    pl.title('Voting System')
    Label(pl, text='Select Poll', font='Centaur 12 bold',bg='Pink').grid(row=1, column=1)
    sel = ttk.Combobox(pl, values=pollnames,state='readonly', textvariable=sele)
    sel.grid(row=2, column=1)
    sel.current(0)
    Button(pl, text='GET RESULTS', command=results).grid(row=2, column=2)


home = Tk()
home.geometry('300x300')
home.title('VOTING SYSTEM')
home['bg'] = '#49A'
Button(home, width=30, text='REGISTER NEW ELECTION',command=create).grid(row=3, column=4, padx=20, pady=10)
Button(home, width=30, text='YOUR VOTES', command=checkAge).grid(row=4, column=4, padx=20, pady=10)
Button(home, width=30, text='VOTE RESULTS', command=selpl).grid(row=5, column=4, padx=20, pady=10)
Label(home, text='WELCOME TO VOTING SYSTEM',font='Centaur 12 bold', bg='#49A').grid(row=6, column=4)

home.mainloop()
