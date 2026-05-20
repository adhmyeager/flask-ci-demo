from flask import Blueprint, render_template


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html', title='Flask CI/CD Demo')


@main_bp.route('/health')
def health():
    return {'status': 'ok'}, 200


@main_bp.route('/greet/<name>')
def greet(name):
    return {'message': f'Hello, {name}!'}, 200