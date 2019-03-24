from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user


class ErrorLogic():

    def error_404(error):
        head = "Oops! This page can't be found (404)"
        statement = " The page you're looking for cannot be found or has been removed "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    def error_403(error):
        head = "Sorry you don't have permission to access this (403)"
        statement = " Please check your account for more information "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    def error_500(error):
        head = "Oops. Something went wrong (500)"
        statement = "Our team is working on the problem, please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 500

    def error_503(error):
        head = "Oops! The server is down (503)"
        statement = "It is either currently under maitenance or overloaded so please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 503

    def error_504(error):
        head = "Gateway Timeout (504)"
        statement = "Your browser failed to send the request to the server in time, please try again"
        return render_template("error_screens/error.html", title=head, message=statement), 504
