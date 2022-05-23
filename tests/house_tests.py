from factories.user import UserFactory
from house.models import House, City, Country, Job
from factories.house import HouseFactory
from house.helpers import _filter_houses_by_form
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from house.constants import MINE_EXPENSES_TITLE_ROUTE, MINE_HOUSE_TABLE_ROUTE, MINE_HOUSE_TABLE_TITLE_ROUTE
from house.constants import MINE_MINE_PAGE_ROUTE, MINE_SIDEBAR_ROUTE


def test_save_house(generate_house):
    generate_house.save()
    assert generate_house in House.objects.all()


def test_delete_house(generate_house):
    generate_house.save()
    generate_house.delete()
    assert generate_house not in House.objects.all()


def test_filter_parent_profession_1(db):
    pass_filter_house_create()
    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=5000,
        children=1,
        parent_profession_1=Job.OTHER,
        parent_profession_2=Job.OTHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 1


def test_filter_country(db):
    pass_filter_house_create()
    HouseFactory(
        country=Country.objects.get(name='India'),
        city=City.objects.get(name='Tel Aviv'),
        income=5000,
        children=1,
        parent_profession_1=Job.TEACHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 1


def test_filter_city(db):
    pass_filter_house_create()
    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Ramat Gan'),
        income=5000,
        children=1,
        parent_profession_1=Job.TEACHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 1


def test_filter_highest_income(db):
    pass_filter_house_create()
    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=12000,
        children=1,
        parent_profession_1=Job.TEACHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 1


def test_filter_lowest_income(db):
    pass_filter_house_create()
    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=4000,
        children=1,
        parent_profession_1=Job.TEACHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 1


def test_profession_either_parent(db):
    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=5000,
        children=1,
        parent_profession_2=Job.TEACHER,
        parent_profession_1=Job.OTHER,
    ).save()

    HouseFactory(
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=5000,
        children=1,
        parent_profession_1=Job.TEACHER,
        parent_profession_2=Job.OTHER,
    ).save()
    houses = _filter_houses_by_form(form_data_filter_tests(), House.objects.all())
    assert len(houses) == 2
    assert House.objects.get(parent_profession_1=Job.TEACHER) in houses
    assert House.objects.get(parent_profession_2=Job.TEACHER) in houses


def test_no_private_houses_sent(db):
    pass_filter_house_create()
    HouseFactory(
        public=False,
    ).save()
    houses = _filter_houses_by_form({}, House.objects.all())
    assert len(houses) == 1
    assert House.objects.get(public=True) in houses


def pass_filter_house_create():
    HouseFactory(
        user=UserFactory(),
        country=Country.objects.get(name='Israel'),
        city=City.objects.get(name='Tel Aviv'),
        income=5000,
        children=1,
        parent_profession_1=Job.TEACHER,
        public=True,
    ).save()


def form_data_filter_tests():
    return {
        'country': Country.objects.get(name='Israel'),
        'city': City.objects.get(name='Tel Aviv'),
        'parent_profession_1': Job.TEACHER,
        'parent_profession_2': None,
        'highest_income': 10000,
        'lowest_income': 5000,
        'children': 1,
    }


def test_house_view_function_200(db, client, new_user):
    client.force_login(new_user)
    HouseFactory(user=new_user).save()
    response = client.get('/house/')
    assert response.status_code == 200


def test_mine_page_expenses_table_views_templates():
    try:
        get_template(MINE_EXPENSES_TITLE_ROUTE)
    except TemplateDoesNotExist:
        assert False, f'Template {MINE_EXPENSES_TITLE_ROUTE} does not exist'


def test_mine_page_house_table_views_templates():
    try:
        get_template(MINE_HOUSE_TABLE_ROUTE)
    except TemplateDoesNotExist:
        assert False, f'Template {MINE_HOUSE_TABLE_ROUTE} does not exist'


def test_mine_page_house_table_title_views_templates():
    try:
        get_template(MINE_HOUSE_TABLE_TITLE_ROUTE)
    except TemplateDoesNotExist:
        assert False, f'Template {MINE_HOUSE_TABLE_TITLE_ROUTE} does not exist'


def test_mine_page_mine_page_views_templates():
    try:
        get_template(MINE_MINE_PAGE_ROUTE)
    except TemplateDoesNotExist:
        assert False, f'Template {MINE_MINE_PAGE_ROUTE} does not exist'


def test_mine_sidebar_views_templates():
    try:
        get_template(MINE_SIDEBAR_ROUTE)
    except TemplateDoesNotExist:
        assert False, f'Template {MINE_SIDEBAR_ROUTE} does not exist'
