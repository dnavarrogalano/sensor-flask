
from flask import render_template, request, redirect, flash
from flask.ext.security import Security, login_required, logout_user, roles_required, current_user, utils
from flask.ext.admin import Admin, expose, AdminIndexView, base
from flask.ext.admin.contrib.sqla import ModelView
from models import *

from forms import *


security = Security(app, user_datastore)
# --------- FLASK Security has a very nice documentation. read more here -> https://pythonhosted.org/Flask-Security/

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    m_tasks = SampleTasksTable()

    list_records = m_tasks.list_all(page, app.config['LISTINGS_PER_PAGE'])

    return render_template("index.html", list_records=list_records)


@app.route('/add_record', methods=['GET', 'POST'])
@login_required
def add_record():
    form = TasksAddForm(request.form)

    if request.method == 'POST':
        if form.validate():
            new_expense = SampleTasksTable()

            title = form.title.data
            description = form.description.data

            logging.info("adding " + title)

            new_expense.add_data(current_user.get_id(), title, description)

            flash("Expense added successfully", category="success")

    return render_template("add_record.html", form=form)



# --------- Secret page example, available only to admin -------------
@app.route('/secret')
@roles_required('admin')
def secret():
    return render_template('secret.html')



@app.route('/logout')
def log_out():
    logout_user()
    return redirect(request.args.get('next') or '/')


@app.route('/sensores')
def get_sensoresDetalle():
    from models import Sensor
    import json
    from time import mktime
    sensors = Sensor.query.all()
    med = Medicion.query.all()
    return render_template('sensores.html', sensores=sensors, meds=med)

#    s = Sensor.query.get(sensor_id)
#    meds =s.medicion.all()
#    valores = [[m.fechautc() ,int(m.valor)] for m in meds]
#    times = [m.timestamp for m in meds]
#    badges = sensoresConValorBadge()
#    return render_template('sensoresDetalle.html', sensores=sensors, meds = valores, times = times, badges = badges, sensor=s)



# Executes before the first request is processed. You might want to delete this after it's done to keep things clean
#@app.before_first_request
#def before_first_request():
#    logging.info("-------------------- initializing everything ---------------------")
#    db.create_all()#

#    user_datastore.find_or_create_role(name='admin', description='Administrator')
#    user_datastore.find_or_create_role(name='end-user', description='End user')#

#    encrypted_password = utils.encrypt_password('123123')
#    if not user_datastore.get_user('me@me.com'):
#        user_datastore.create_user(email='me@me.com', password=encrypted_password, active=True, confirmed_at=datetime.datetime.now())#

#    encrypted_password = utils.encrypt_password('123123')
#    if not user_datastore.get_user('enduser@enduser.com'):
#        user_datastore.create_user(email='enduser@enduser.com', password=encrypted_password, active=True, confirmed_at=datetime.datetime.now())#

#    db.session.commit()#

#    user_datastore.add_role_to_user('me@me.com', 'admin')
#    user_datastore.add_role_to_user('enduser@enduser.com', 'end-user')
#    db.session.commit()


# -------------------------- ADMIN PART ------------------------------------
# --------- FLASK ADMIN has a very nice documentation. read more here -> http://flask-admin.readthedocs.org/en/latest/






class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


# ------- visible only to admin user, else returns "not found" -----------
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.has_role('admin'):
            return render_template('other/404.html'), 404
        return self.render('admin/index.html')


class TasksAdminView(MyModelView):
    can_create = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(TasksAdminView, self).__init__(SampleTasksTable, session, **kwargs)


class UserAdminView(MyModelView):
    column_exclude_list = ('password')

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(UserAdminView, self).__init__(User, session, **kwargs)


class RoleView(MyModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


class SensorAdminView(MyModelView):
    can_create = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(SensorAdminView, self).__init__(Sensor, session, **kwargs)

class CasaAdminView(MyModelView):
    can_create = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(CasaAdminView, self).__init__(Casa, session, **kwargs)



admin = Admin(app, 'Flask-Easy Admin', index_view=MyAdminIndexView())
admin.add_view(TasksAdminView(db.session))
admin.add_view(UserAdminView(db.session))
admin.add_view(RoleView(db.session))
admin.add_view(SensorAdminView(db.session))
admin.add_view(CasaAdminView(db.session))
admin.add_link(base.MenuLink('Web Home', endpoint="index"))
admin.add_link(base.MenuLink('Logout', endpoint="log_out"))

# --------------------------  END ADMIN PART ---------------------------------



# --------------------------- QUICK SEO PART ----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('other/404.html'), 404


@app.errorhandler(403)
def page_forbiden(e):
    return render_template('other/403.html'), 403


# ----------------------------- END QUICK SEO PART ----------------------

#----------------- LLAMADAS PRUEBA

@app.route('/llamadas')
def llamadas():
    return render_template("llamadas.html")


