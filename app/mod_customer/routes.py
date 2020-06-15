import json
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .exceptions import InvalidSSNId, CustomerDoesNotExist, InvalidId
from .forms import CustomerForm
from .models import Customer
from .service import create_customer, get_all_customers, get_customer_by_id, delete_customer, get_all_active_accounts, search_customer

bp_customer = Blueprint(
    'customer', __name__, template_folder='templates', static_folder='static'
)


@bp_customer.route('/signup', methods=['POST', 'GET'])
def signup():
    form = CustomerForm()
    if request.method == 'POST':
        try:
            create_customer(request.form)
            flash("Customer successfully registered!", "success")
        except InvalidSSNId as invalid_ssn_id:
            flash("Customer already exists or invalid SSN ID", "error")
        return redirect(url_for("customer.signup"))
    return render_template("create_customer.html", title="Create Customer Account", form=form)


@bp_customer.route('/status')
def status():
    return render_template("customer_status.html", entries=get_all_customers())


@bp_customer.route('customer/status/<string:customer_id>', methods=['GET'])
def details(customer_id):
    return render_template("customer_details.html", detail=get_customer_by_id(customer_id))


@bp_customer.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        try:
            delete_customer(request.form)
            flash('Customer account deactivated successfully', 'success')
        except CustomerDoesNotExist as customer_does_not_exist:
            flash(customer_does_not_exist.message, 'error')

    customers_mappings = get_all_active_accounts()
    return render_template('delete_customer.html', customers=customers_mappings, json_customers=json.dumps(customers_mappings))

@bp_customer.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        try:
            search_customer(request.form)
            flash('Customer is active','success')
        except InvalidSSNId as invalid_ssn_id:
            flash(invalid_ssn_id.message, 'error')
        except InvalidId as invalid_id:
            flash(invalid_id.message,'error')
    return render_template("customer_search.html")
