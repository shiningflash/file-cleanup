import os, requests, json
import tkinter as tk

root = tk.Tk()
title = 'File Clean-Up'
root.title(title)

count = 0
deleted_files = []

root.geometry("650x250")

dir_path_var = tk.StringVar()
extensions_var = tk.StringVar()
email_var = tk.StringVar()


def send_mail(dir_path, extensions, email):
    try:
        url = "https://api.sendinblue.com/v3/smtp/email"
        ACCRESS_KEY = "SENDINBLUE ACCESS KEY HERE"

        payload = {
            "sender":{
                "name": "FILE-CLEANUP",
                "email": "file-cleanup@gmail.com"
            },
            "to":[
                {
                    "email": email
                }
            ],
            "subject": title,
            "htmlContent": f'From FILE-CLEANUP, <br> <br> <strong> Parent Directory Path: {dir_path} <br> Extensions: {extensions} <br> Total deleted file: {count} </strong> <br> <br> All deleted files: {deleted_files}'
        }
        headers = {
            "api-key": ACCRESS_KEY,
            "content-type": "application/json",
            "accept": "application/json"
        }
        result = requests.post(url, data=json.dumps(payload), headers=headers)
        result_text = "Email sent" if str(result.status_code) in ['200', '201'] else "Email failed to send"
        mail_msg_label = tk.Label(root, text=f'{result_text}', fg='red')
        mail_msg_label.grid(row=6, column=1)
    except:
        mail_msg_label = tk.Label(root, text="Email failed to send", fg='red')
        mail_msg_label.grid(row=6, column=1)


def delete_files(file_path, extensions):
    try:
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.endswith(tuple(extensions)):
                    global count, deleted_files
                    count += 1
                    deleted_files.append(file)
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        # permission issues
                        pass
    except:
        root.title('Error!')
        this_label = tk.Label(root, text=f'Please, fill up correctly.', fg='red')
        this_label.grid(row=5, column=1)
        return


def submit():
    root.title('Running...')

    this_label = tk.Label(root, text=f'', fg='red')
    this_label.grid(row=5, column=1)

    dir_path = dir_path_var.get()
    extensions = extensions_var.get().split(' ')
    extensions = [extension for extension in extensions if len(extension) > 1]
    email = email_var.get()

    if not dir_path:
        root.title('Error!')
        this_label = tk.Label(root, text=f'Please, enter directory path.', fg='red')
        this_label.grid(row=5, column=1)
        return
    
    if not extensions:
        root.title('Error!')
        this_label = tk.Label(root, text=f'Please, enter file extensions that you want to remove.', fg='red')
        this_label.grid(row=5, column=1)
        return

    delete_files(dir_path, extensions)

    this_label = tk.Label(root, text=f'All including files has deleted successfully! Total {count}.', fg='green')
    this_label.grid(row=5, column=1)

    send_mail(dir_path, extensions, email)

    root.title('DONE!')

    dir_path_entry.delete(0, tk.END)
    extensions_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


if __name__=='__main__':
    dir_path_label = tk.Label(root, text='Directory Path:*', width = 30)
    dir_path_entry = tk.Entry(root, textvariable=dir_path_var, width = 40)

    extensions_label = tk.Label(root, text='Extensions (space separated)*:', width = 30)
    extensions_entry = tk.Entry(root, textvariable=extensions_var, width = 40)

    email_label = tk.Label(root, text='Email Id:', width = 30)
    email_entry = tk.Entry(root, textvariable=email_var, width = 40)

    sub_btn = tk.Button(root, text='Submit', command=submit, bg='brown', fg='white')

    dir_path_label.grid(row=0, column=0, pady=(15, 5))
    dir_path_entry.grid(row=0, column=1, pady=(15, 5))
    extensions_label.grid(row=1, column=0, pady=5)
    extensions_entry.grid(row=1, column=1, pady=5)
    email_label.grid(row=3, column=0, pady=5)
    email_entry.grid(row=3, column=1, pady=5)
    sub_btn.grid(row=4, column=1, pady=5)

    root.mainloop()