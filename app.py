from flask import Flask, render_template, redirect, url_for
import pygame
import tkinter as tkr
from flask import Flask,render_template,flash,redirect,url_for,request,session
from flask_bcrypt import  generate_password_hash,check_password_hash
from config import User
import os


app = Flask(__name__)
app.secret_key = "@Eshandow254"
"""" if a hacker manges to get your secrete key can decrypt all the passwords"""


os.chdir(r"C:\Users\user\OneDrive\Desktop\ngoma")
print(os.getcwd)
Song_list = os.listdir

Player = tkr.Tk()


songs = Song_list()
@app.route('/home')
def music():  # put application's code here
    return render_template("home.html", songs = Song_list())


pygame.init()
pygame.mixer.init()
Playlist = tkr.Listbox(Player, highlightcolor="blue", selectmode=tkr.SINGLE)


@app.route('/sign up',methods =['GET','POST'])
def register():  # put application's code here
    if request.method == "POST":
        jina= request.form["u_name"]
        arafa =request.form["u_email"]
        siri = request.form["u_password"]
        siri = generate_password_hash(siri)
        User.create(name =jina, email=arafa ,password =siri)
        flash("Registration successful")
    else:
        flash("wrong password or email")
    return render_template('sign up.html')





@app.route('/login',methods =['GET','POST'])
def login():
    if request.method == "POST":
        email= request.form["u_email"]
        password = request.form["u_password"]

        try:
            user =User.get(User.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Login successfully")
                session["logged_in"] = True
                session["name"] = user.name
                return render_template('home.html', songs = Song_list())
            else:
                flash("Wrong username or password")
        except:
            flash("operation not available")

    return render_template('login.html')




@app.route('/')
def welcomepage():
    return render_template('welcome page.html')

"""  if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('welcome page.html')"""


@app.route('/users')
def users():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users =User.select()
    return render_template('users.html',users = users)



@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    User.delete().where(User.id == id).execute()
    flash("user deleted successfully")
    return redirect(url_for("users"))


@app.route('/update/<int:id>',methods =['GET','POST'])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = User.get(User.id == id)
    if request.method == "POST":
        updatedName = request.form["u_name"]
        updatedEmail = request.form["u_email"]
        updatedpassword = request.form["u_password"]
        user.name = updatedName
        user.email = updatedEmail
        user.password = generate_password_hash(updatedpassword)
        user.save()
        flash("User updated successfully")
        return redirect(url_for("users"))
    return render_template("update.html",user = user)




@app.route('/play/<int:id>')
def Play(id):
    pygame.mixer.music.load(songs[id])
    # var.set(Playlist.get(tkr.ACTIVE))
    pygame.mixer.music.play()
    return redirect(url_for("music"))
    # pygame.mixer.music.set_volume(Volume_level.get())
    # print(pygame.mixer.music.get_volume())
    # print(Volume_level.get())


@app.route('/stop')
def ExitPlayer():
    pygame.mixer.music.stop()
    return redirect(url_for("music"))


@app.route('/about')
def about():
    return render_template('about.html')


"""@app.route('/pause')
def Pause():
    pygame.mixer.music.pause()


@app.route('/unpause')
def Unpause():
    pygame.mixer.music.unpause()


@app.route('/rewind')
def Rewind():
    pygame.mixer.music.rewind()"""


if __name__ == '__main__':
    app.run()
