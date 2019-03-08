from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

class ErrorLogic():


    def error_404(error):
        return render_template("error_screens/404.html"), 404

    def error_403(error):
        return render_template("error_screens/403.html"), 403

    def error_500(error):
        return render_template("error_screens/500.html"), 500

    def error_503(error):
        return render_template("error_screens/503.html"), 503

    def error_504(error):
        return render_template("error_screens/504.html"), 504
