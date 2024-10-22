from flask import Blueprint , render_template 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')



@main.route('/register')
def register():
    # Direct rendering of the choose_role.html when the REGISTER button is clicked
    return render_template('role.html')

