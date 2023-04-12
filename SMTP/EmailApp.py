#!/usr/bin/python3

# Student name and No.: Tsang Edmund Chiu Yat 3035667261
# Development platform: VScode
# Python version: 3.10.11

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import re
import os
import pathlib
import sys
import base64
import socket

#
# Global variables
#

# Replace this variable with your CS email address
YOUREMAIL = "edmundcy@cs.hku.hk"
# Replace this variable with your student number
MARKER = '3035667261'

# The Email SMTP Server
SERVER = "testmail.cs.hku.hk"   #SMTP Email Server
SPORT = 25                      #SMTP listening port

# For storing the attachment file information
fileobj = None                  #For pointing to the opened file
filename = ''                   #For keeping the filename


#
# For the SMTP communication
#
def do_Send():
  # Get the user's inputs
  to, cc, bcc, subject, msg = get_TO(), get_CC(), get_BCC(), get_Subject(), get_Msg()
  to_list, cc_list, bcc_list = [], [], []
  composed_msg = ''
  # Check the "To" input
  if not to:
    alertbox('Must enter the recipient\'s email address')
    return
  else :
    #Split the input into a list of emails and remove the spaces
    to_list = to.replace(" ", "").split(',')
    for i in to_list:
      if not echeck(i):
        alertbox('Invalid To: Email - ' + i)
        return
  
  # Check the "Subject" input
  if not subject:
    alertbox('Must enter the enter the subject')
    return
  
  # Check the "Message" input
  if len(msg) <= 1:
    alertbox('Must enter the the message')
    return
    
  # Check the "CC" input
  if cc:
    cc_list = cc.replace(" ", "").split(',')
    for i in cc_list:
      if not echeck(i):
        alertbox('Invalid CC: Email - ' + i)
        return
    
  # Check the "BCC" input
  if bcc:
    bcc_list = bcc.replace(" ", "").split(',')
    for i in bcc_list:
      if not echeck(i):
        alertbox('Invalid BCC: Email - ' + i)
        return
  
  # message with no attachment
  # Compose the email message following RFC2822 standard
  if not filename:
    # No cc and bcc
    if not cc_list and not bcc_list:
      format_to = ', '.join(to_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\n\r\n{msg}\r\n'
    #No bcc
    elif not bcc_list and cc_list:
      format_to = ', '.join(to_list)
      format_cc = ', '.join(cc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nCc: {format_cc}\r\n\r\n{msg}\r\n'
    #No cc
    elif not cc_list and bcc_list:
      format_to = ', '.join(to_list)
      format_bcc = ', '.join(bcc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nBcc: {format_bcc}\r\n\r\n{msg}\r\n'
    #Both cc and bcc
    else:
      format_to = ', '.join(to_list)
      format_cc = ', '.join(cc_list)
      format_bcc = ', '.join(bcc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nCc: {format_cc}\r\nBcc: {format_bcc}\r\n\r\n{msg}\r\n'
  
  # message with attachment
  # Compose the email message following RFC2045 standard with two MIME header
  else:
    encoded_file = base64.encodebytes(fileobj.read()).decode('utf-8')
    # No cc and bcc
    if not cc_list and not bcc_list:
      format_to = ', '.join(to_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary={MARKER}\r\n\r\n--{MARKER}\r\nContent-Type: text/plain\r\nContent-Transfer-Encoding: 7bit\r\n\r\n{msg}\r\n--{MARKER}\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename={filename}\r\n\r\n{encoded_file}\r\n--{MARKER}--\r\n'
    #No bcc
    elif not bcc_list and cc_list:
      format_to = ', '.join(to_list)
      format_cc = ', '.join(cc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nCc: {format_cc}\r\nContent-Type: multipart/mixed; boundary={MARKER}\r\n\r\n--{MARKER}\r\nContent-Type: text/plain\r\nContent-Transfer-Encoding: 7bit\r\n\r\n{msg}\r\n--{MARKER}\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename={filename}\r\n\r\n{encoded_file}\r\n--{MARKER}--\r\n'
    #No cc
    elif not cc_list and bcc_list:
      format_to = ', '.join(to_list)
      format_bcc = ', '.join(bcc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nBcc: {format_bcc}\r\nContent-Type: multipart/mixed; boundary={MARKER}\r\n\r\n--{MARKER}\r\nContent-Type: text/plain\r\nContent-Transfer-Encoding: 7bit\r\n\r\n{msg}\r\n--{MARKER}\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename={filename}\r\n\r\n{encoded_file}\r\n--{MARKER}--\r\n'
    #Both cc and bcc
    else:
      format_to = ', '.join(to_list)
      format_cc = ', '.join(cc_list)
      format_bcc = ', '.join(bcc_list)
      composed_msg = f'From: {YOUREMAIL}\r\nSubject: {subject}\r\nTo: {format_to}\r\nCc: {format_cc}\r\nBcc: {format_bcc}\r\nContent-Type: multipart/mixed; boundary={MARKER}\r\n\r\n--{MARKER}\r\nContent-Type: text/plain\r\nContent-Transfer-Encoding: 7bit\r\n\r\n{msg}\r\n--{MARKER}\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename={filename}\r\n\r\n{encoded_file}\r\n--{MARKER}--\r\n'

  # Implement the SMTP communication using the low-level socket interface TCP
  # Create a socket object
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the server and receive the server response
  # If no response within 10 seconds, alert a message and close the TCP connection
  try:
    s.connect((SERVER, SPORT))
    s.settimeout(10)
    recv = s.recv(1024).decode('utf-8')
    if recv[0:3] == '220':
      print(f'{recv[0:3]} {SERVER} at port:{SPORT} {s.getpeername()}')
    else:
      alertbox('Fail in connecting to server\n' + recv)
      return
  except socket.timeout:
    alertbox('SMTP server is not available')
    #close the socket
    s.close()
    return

  # Send HELO command and print server response with extra info replies by the server to indicate which parameters this server supports
  heloCommand = f'EHLO {s.getpeername()[0]}\r\n'
  print(heloCommand)
  s.send(heloCommand.encode('utf-8'))
  recv1 = s.recv(1024).decode('utf-8')
  if recv1[0:3] != '250':
    alertbox('Fail in sending EHLO\n' + recv1)
    return
  print(recv1)

  # Send MAIL FROM command and print server response
  mailFrom = f'MAIL FROM: <{YOUREMAIL}>\r\n'
  print(mailFrom)
  s.send(mailFrom.encode('utf-8'))
  recv2 = s.recv(1024).decode('utf-8')
  if recv2[0:3] != '250':
    alertbox('Fail in sending MAIL FROM\n' + recv2)
    return
  print(recv2)

  # Send RCPT TO command and print server response
  # combine the to_list, cc_list and bcc_list into one list
  rcpt_list = to_list + cc_list + bcc_list
  for i in rcpt_list:
    rcptTo = f'RCPT TO: <{i}>\r\n'
    print(rcptTo)
    s.send(rcptTo.encode('utf-8'))
    recv3 = s.recv(1024).decode('utf-8')
    if recv3[0:3] != '250':
      alertbox('Fail in sending RCPT TO\n' + recv3)
      return
    print(recv3)

  # Send DATA command and print server response
  data = 'DATA\r\n'
  print(data)
  s.send(data.encode('utf-8'))
  recv4 = s.recv(1024).decode('utf-8')
  if recv4[0:3] != '354':
    alertbox('Fail in sending DATA\n' + recv4)
    return
  print(recv4)

  # Send message data (ends with a . on a line by itself)
  end_msg = composed_msg + '.\r\n'
  # print(end_msg)
  s.send(end_msg.encode('utf-8'))
  recv5 = s.recv(1024).decode('utf-8')
  if recv5[0:3] != '250':
    alertbox('Fail in sending message data\n' + recv5)
    return
  print(recv5)
  alertbox('successfully')

  # Quit the SMTP connection
  quit = 'QUIT\r\n'
  print(quit)
  s.send(quit.encode('utf-8'))
  recv6 = s.recv(1024).decode('utf-8')
  if recv6[0:3] != '221':
    alertbox('Fail in sending QUIT\n' + recv6)
    return
  print(recv6)


#
# Utility functions
#

#This set of functions is for getting the user's inputs
def get_TO():
  return tofield.get()

def get_CC():
  return ccfield.get()

def get_BCC():
  return bccfield.get()

def get_Subject():
  return subjfield.get()

def get_Msg():
  return SendMsg.get(1.0, END)

#This function checks whether the input is a valid email
def echeck(email):   
  regex = '^([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'  
  if(re.fullmatch(regex,email)):   
    return True  
  else:   
    return False

#This function displays an alert box with the provided message
def alertbox(msg):
  messagebox.showwarning(message=msg, icon='warning', title='Alert', parent=win)

#This function calls the file dialog for selecting the attachment file.
#If successful, it stores the opened file object to the global
#variable fileobj and the filename (without the path) to the global
#variable filename. It displays the filename below the Attach button.
def do_Select():
  global fileobj, filename
  if fileobj:
    fileobj.close()
  fileobj = None
  filename = ''
  filepath = filedialog.askopenfilename(parent=win)
  if (not filepath):
    return
  print(filepath)
  if sys.platform.startswith('win32'):
    filename = pathlib.PureWindowsPath(filepath).name
  else:
    filename = pathlib.PurePosixPath(filepath).name
  try:
    fileobj = open(filepath,'rb')
  except OSError as emsg:
    print('Error in open the file: %s' % str(emsg))
    fileobj = None
    filename = ''
  if (filename):
    showfile.set(filename)
  else:
    alertbox('Cannot open the selected file')

#################################################################################
#Do not make changes to the following code. They are for the UI                 #
#################################################################################

#
# Set up of Basic UI
#
win = Tk()
win.title("EmailApp")

#Special font settings
boldfont = font.Font(weight="bold")

#Frame for displaying connection parameters
frame1 = ttk.Frame(win, borderwidth=1)
frame1.grid(column=0,row=0,sticky="w")
ttk.Label(frame1, text="SERVER", padding="5" ).grid(column=0, row=0)
ttk.Label(frame1, text=SERVER, foreground="green", padding="5", font=boldfont).grid(column=1,row=0)
ttk.Label(frame1, text="PORT", padding="5" ).grid(column=2, row=0)
ttk.Label(frame1, text=str(SPORT), foreground="green", padding="5", font=boldfont).grid(column=3,row=0)

#Frame for From:, To:, CC:, Bcc:, Subject: fields
frame2 = ttk.Frame(win, borderwidth=0)
frame2.grid(column=0,row=2,padx=8,sticky="ew")
frame2.grid_columnconfigure(1,weight=1)
#From 
ttk.Label(frame2, text="From: ", padding='1', font=boldfont).grid(column=0,row=0,padx=5,pady=3,sticky="w")
fromfield = StringVar(value=YOUREMAIL)
ttk.Entry(frame2, textvariable=fromfield, state=DISABLED).grid(column=1,row=0,sticky="ew")
#To
ttk.Label(frame2, text="To: ", padding='1', font=boldfont).grid(column=0,row=1,padx=5,pady=3,sticky="w")
tofield = StringVar()
ttk.Entry(frame2, textvariable=tofield).grid(column=1,row=1,sticky="ew")
#Cc
ttk.Label(frame2, text="Cc: ", padding='1', font=boldfont).grid(column=0,row=2,padx=5,pady=3,sticky="w")
ccfield = StringVar()
ttk.Entry(frame2, textvariable=ccfield).grid(column=1,row=2,sticky="ew")
#Bcc
ttk.Label(frame2, text="Bcc: ", padding='1', font=boldfont).grid(column=0,row=3,padx=5,pady=3,sticky="w")
bccfield = StringVar()
ttk.Entry(frame2, textvariable=bccfield).grid(column=1,row=3,sticky="ew")
#Subject
ttk.Label(frame2, text="Subject: ", padding='1', font=boldfont).grid(column=0,row=4,padx=5,pady=3,sticky="w")
subjfield = StringVar()
ttk.Entry(frame2, textvariable=subjfield).grid(column=1,row=4,sticky="ew")

#frame for user to enter the outgoing message
frame3 = ttk.Frame(win, borderwidth=0)
frame3.grid(column=0,row=4,sticky="ew")
frame3.grid_columnconfigure(0,weight=1)
scrollbar = ttk.Scrollbar(frame3)
scrollbar.grid(column=1,row=1,sticky="ns")
ttk.Label(frame3, text="Message:", padding='1', font=boldfont).grid(column=0, row=0,padx=5,pady=3,sticky="w")
SendMsg = Text(frame3, height='10', padx=5, pady=5)
SendMsg.grid(column=0,row=1,padx=5,sticky="ew")
SendMsg.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=SendMsg.yview)

#frame for the button
frame4 = ttk.Frame(win,borderwidth=0)
frame4.grid(column=0,row=6,sticky="ew")
frame4.grid_columnconfigure(1,weight=1)
Sbutt = Button(frame4, width=5,relief=RAISED,text="SEND",command=do_Send).grid(column=0,row=0,pady=8,padx=5,sticky="w")
Atbutt = Button(frame4, width=5,relief=RAISED,text="Attach",command=do_Select).grid(column=1,row=0,pady=8,padx=10,sticky="e")
showfile = StringVar()
ttk.Label(frame4, textvariable=showfile).grid(column=1, row=1,padx=10,pady=3,sticky="e")

win.mainloop()
