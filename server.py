from flask import Flask, render_template
from db_operations import output_for_flask


app = Flask(__name__)


@app.route('/')
def score():
    return render_template('score.html', order_info=output_for_flask())

if __name__ == "__main__":
    app.run()
