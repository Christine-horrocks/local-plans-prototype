import csv
import click
import requests

from flask.cli import with_appcontext
from contextlib import closing
from application.extensions import db
from application.models import PlanningAuthority, LocalPlan, PlanDocument, EmergingPlanDocument


def create_other_data(pa, row):
    plan_id = row['local-plan'].strip()
    plan = LocalPlan.query.get(plan_id)
    if plan is not None:
        status = [row['status'].strip(), row['date'].strip()]
        if status not in plan.states:
            plan.states.append(status)
            print('updated local plan', plan_id)
        if pa not in plan.planning_authorities:
            pa.local_plans.append(plan)
    else:
        plan = LocalPlan()
        plan.local_plan = plan_id
        plan.url = row['plan-policy-url'].strip()
        plan.states = [[row['status'].strip(), row['date'].strip()]]
        pa.local_plans.append(plan)
        plan.title = row['title'].strip()
        print('created local plan', plan_id)

    db.session.add(pa)
    db.session.commit()
    print('loaded local plan', plan_id)

    if row['status'].strip() == 'adopted' and row.get('plan-document-url') and row.get('plan-document-url') != '?':
        pd = PlanDocument(url=row.get('plan-document-url'))
        plan.plan_documents.append(pd)
        db.session.add(pa)
        db.session.commit()
        print('loaded plan document for plan', plan, 'document', row.get('plan-document-url'))


@click.command()
@with_appcontext
def load():
    websites = 'https://raw.githubusercontent.com/digital-land/alpha-data/master/local-authority-websites.csv'
    mapping = {}
    print('Loading', websites)
    with closing(requests.get(websites, stream=True)) as r:
        reader = csv.DictReader(r.iter_lines(decode_unicode=True), delimiter=',')
        for row in reader:
            mapping[row['local-authority'].strip()] = row['website'].strip()

    register = 'https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/local-plan-register.csv'
    print('Loading', register)
    with closing(requests.get(register, stream=True)) as r:
        reader = csv.DictReader(r.iter_lines(decode_unicode=True), delimiter=',')
        for row in reader:
            id = row['organisation'].strip()
            name = row['name'].strip()
            if id != '':
                pa = PlanningAuthority.query.get(id)
                if pa is None:
                    pa = PlanningAuthority(id=id, name=name)
                    if mapping.get(id) is not None:
                        pa.website = mapping.get(id)
                    db.session.add(pa)
                    db.session.commit()
                    print(row['organisation'], row['name'])
                else:
                    print(id, 'already in db')

                create_other_data(pa, row)


@click.command()
@with_appcontext
def clear():
    db.session.execute('DELETE FROM planning_authority_plan');
    db.session.query(EmergingPlanDocument).delete()
    db.session.query(PlanDocument).delete()
    db.session.query(LocalPlan).delete()
    db.session.query(PlanningAuthority).delete()
    db.session.commit()

