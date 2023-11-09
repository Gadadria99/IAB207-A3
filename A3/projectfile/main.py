from qutickets import create_app
from flask import render_template


if __name__ == '__main__':
    app = create_app()
    app.run()
    @app.errorhandler(404) 
# inbuilt function which takes error as parameter 
    def not_found(e): 
        return render_template("404.html", error=e)

    @app.errorhandler(500) 
# inbuilt function which takes error as parameter 
    def not_found(e): 
        return render_template("500.html", error=e)
