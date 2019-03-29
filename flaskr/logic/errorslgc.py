from flask import render_template

"""
This class holds all the functions for the error logic. It catches an error and generates the error template with the
corresponding error message and description.
"""
class ErrorLogic:

    @staticmethod
    def error_404():
        """
        Catches a 404 error and displays the corresponding error messages on the rendered template
        :return: error.html
        """
        head = "Oops! This page can't be found (404)"
        statement = " The page you're looking for cannot be found or has been removed "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    @staticmethod
    def error_403():
        """
        Catches a 403 error and displays the corresponding error messages on the rendered template
        :return: error.html
        """
        head = "Sorry you don't have permission to access this (403)"
        statement = " Please check your account for more information "
        return render_template("error_screens/error.html", title=head, message=statement), 404

    @staticmethod
    def error_500():
        """
        Catches a 500 error and displays the corresponding error messages on the rendered template
        :return: error.html
        """
        head = "Oops. Something went wrong (500)"
        statement = "Our team is working on the problem, please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 500

    @staticmethod
    def error_503():
        """
        Catches a 503 error and displays the corresponding error messages on the rendered template
        :return: error.html
        """
        head = "Oops! The server is down (503)"
        statement = "It is either currently under maitenance or overloaded so please try again later"
        return render_template("error_screens/error.html", title=head, message=statement), 503

    @staticmethod
    def error_504():
        """
        Catches a 504 error and displays the corresponding error messages on the rendered template
        :return: error.html
        """
        head = "Gateway Timeout (504)"
        statement = "Your browser failed to send the request to the server in time, please try again"
        return render_template("error_screens/error.html", title=head, message=statement), 504
