from flask import render_template


class ErrorLogic:

    @staticmethod
    def error_404():
        head = "Oops! This page can't be found (404)"
        statement = " The page you're looking for cannot be found or has been removed "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    @staticmethod
    def error_403():
        head = "Sorry you don't have permission to access this (403)"
        statement = " Please check your account for more information "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    @staticmethod
    def error_500():
        head = "Oops. Something went wrong (500)"
        statement = "Our team is working on the problem, please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 500

    @staticmethod
    def error_503():
        head = "Oops! The server is down (503)"
        statement = "It is either currently under maitenance or overloaded so please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 503

    @staticmethod
    def error_504():
        head = "Gateway Timeout (504)"
        statement = "Your browser failed to send the request to the server in time, please try again"
        return render_template("error_screens/error.html", title=head, message=statement), 504
