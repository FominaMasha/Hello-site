from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Company,
    Member,
    Order,
    Event,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound)

from pyramid.view import (
    view_config,
    forbidden_view_config)

from pyramid.security import (
    remember,
    forget)  

from .security import USERS   

@view_config(route_name = 'home', renderer = 'templates/index.jinja2')
def my_view(request):   	
    events = DBSession.query(Event).all()
    if 'form.submitted' in request.params:
        name = request.params['name']
        email = request.params['email']
        phone = request.params['phone']
        companyName = request.params['companyName']
        siteCompany = request.params['companySite']

        company = Company(name = companyName, site = siteCompany)
        DBSession.add(company)

        member = Member(name = name, phone = phone, e_mail = email, company = company)
        DBSession.add(member)

        order = Order(member = member, payment_status = True, obtain_status = False)
        DBSession.add(order)

    return {'events': events, 'username': request.authenticated_userid,}

@view_config(route_name = 'login', renderer = 'templates/login.jinja2')
@forbidden_view_config(renderer = 'templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' 
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = "Incorrect login or password"            

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)

