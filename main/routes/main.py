import re
from flask import Blueprint, render_template
from flask import request
from flask_login import current_user

main = Blueprint('main', __name__)

def extract_product_id(url):
    pattern = r"/(\d+)/buy"
    match = re.search(pattern, url)

    if match:
        product_id = match.group(1)
        return product_id
    else:
        return None

@main.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('product')

        if pid := extract_product_id(url):
            print(pid)
            print(current_user.is_authenticated)
            print(current_user.username)
        return {"status": "success"}

    return render_template("index.html")


@main.route("/profile/<string:username>", methods=['GET'])
def profile(username):
    return f"<h1> Profile {username} </h1>"