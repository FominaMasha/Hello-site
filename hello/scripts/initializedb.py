import os
import sys

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from ..models import (
    DBSession,
    Company,
    Member,
    Order,
    Event,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:        
        event1 = Event(
            name = 'Иннопром 2016', 
            date = 'с 11 по 14 июля',
            #address = 'г. Екатеринбург, ЭКСПО-бульвар, дом 2',
            description = 'Главная тема ИННОПРОМ-2016 - «Промышленные сети». Страна-партнер ИННОПРОМ-2016 – Индия. Темы, которые действительно волнуют промышленников. Более 500 спикеров и экспертов на уровне СЕО. 150 мероприятий, открытых для посещения. Более 40 партнеров по организации мероприятий, среди которых: крупнейшие игроки российского и международного промышленного сектора, финансовые институты, институты развития, исследовательские учреждения. Индивидуальные/закрытые встречи лиц, принимающих решения. Прямое общение компаний с заказчиками, партнерами и всеми уровнями власти.',        
        	img = 'innoprom.jpg')
        event2 = Event(
            name = 'Gadget Show 2016', 
            date = 'c 26 по 28 августа',            
            description = 'Концепция выставки и кибер-фестиваля заключается в максимуме интерактива, применению роботов и виртуальной реальности, созданию развлекательного и рабочего пространства для участников и посетителей. Возможности для спонсоров и партнеров в категориях генеральный спонсор, спонсор и партнер включают широкие возможности продвижения как до начала, так во время и после выставки.',
            img = 'gadgetshow.jpg')
        event3 = Event(
            name = 'Международная туристическая выставка Expotravel', 
            date = 'c 7 по 8 октября',            
            description = '«EXPOTRAVEL» - яркое событие в индустрии туризма, направленное на развитие внутреннего, въездного и выездного туризма, а также на укрепление взаимоотношений между региональными и зарубежными представителями туристического бизнеса за счет создания уникальной платформы для их взаимодействия. Участие в выставке позволит Вам рассказать о своих уникальных услугах, установить контакты с потенциальными клиентами, как в Уральском регионе, так и за его пределами, и обменяться опытом с вашими коллегами.',
            img = 'expotravel.jpg')        
        DBSession.add(event1)
        DBSession.add(event2)
        DBSession.add(event3)

        company1 = Company(
            name = 'Госкорпорация "Росатом"',
            site = 'http://www.rosatom.ru/')
        company2 = Company(
            name = 'КУКА РОБОТИКС РУС, ООО',
            site = 'http://www.kuka-robotics.com/russia/ru/')        
        DBSession.add(company1)
        DBSession.add(company2)

        member1 = Member(
            name = 'Сергей Кириенко',            
            phone = '89022134935',
            company = company1)
        member2 = Member(
            name = 'Эйил Грир',
            phone = '89002107823',
            company = company2)
        member3 = Member(
            name = 'Мэтью Уэбб',
            phone = '89002107824',
            company = company2)
        DBSession.add(member1)
        DBSession.add(member2)
        DBSession.add(member3)

        order1 = Order(
            member = member1,
            payment_status = True,
            obtain_status = False)
        order2 = Order(
            member = member2,
            payment_status = True,
            obtain_status = False)
        order3 = Order(
            member = member3,
            payment_status = True,
            obtain_status = False)        
        DBSession.add(order1)
        DBSession.add(order2)
        DBSession.add(order3)