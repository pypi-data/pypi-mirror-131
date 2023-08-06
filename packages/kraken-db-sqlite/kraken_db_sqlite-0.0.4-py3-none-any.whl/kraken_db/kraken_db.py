from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import over
from sqlalchemy import inspect

from sqlalchemy import Column, Boolean, Date, DateTime, Float, Integer, Text, String

from sqlalchemy.orm import aliased
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

import json
import datetime



"""
Init db engine
"""
#engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///test.db''check_same_thread=true&timeout=10&mode=ro&nolock=1&uri=true', echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


"""
Class declaration
"""


class Observation(Base):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    observation_id = Column(String)
    ref_id = Column(String)
    datasource = Column(String)
    agent = Column(String)
    instrument = Column(String)
    object = Column(String)
    result = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    valid = Column(Boolean)

    record_type = Column(String)
    record_id = Column(String)
    key = Column(String)
    value = Column(String)
    credibility = Column(Float)
    created_date = Column(DateTime)    



    def _asdict(self):
        record = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        record.pop('id')
        record.pop('ref_id')

        return record

Base.metadata.create_all(engine)


"""
API
"""

def get(record_type = None, record_id = None, key = None, value = None):
    # Get observations matching conditions
    query = _get_observations(record_type, record_id, key, value)

    return _to_dict(query)


def get_max(record_type = None, record_id = None, key = None, value = None):
    """Return max observation
    """
    query = _get_max_observations(record_type, record_id, key, value)


    return _to_dict(query)


def get_summary(record_type = None, record_id = None, key = None, value = None):
    """Return object with max observation for each key
    """

    query = _get_summary(record_type, record_id, key, value)

    return _to_dict(query)


def get_summary_by_value(record_type = None, record_id = None):
    """Return object with max observation for each key value combination
    """

    query = _get_summaries_by_value(record_type, record_id)

    return _to_dict(query)


def search(params, order_by = None, order_direction = None, limit = None, offset = None):

    query = _search(params, order_by, order_direction, limit, offset)

    return _to_dict(query)


def search_first(params, order_by = None, order_direction = None, limit = None, skip = None):

    query = _search(params, order_by, order_direction, 1, 0)

    return _to_dict(query)



def post(record):
    """Post an observation. Need ot be committed
    """
    result = _post_observation_from_record(record)
    result = commit()

    return


def update(old_record_type, old_record_id, new_record_type, new_record_id):
    """Changes record_id and related references
    """

    _update(old_record_type, old_record_id, new_record_type, new_record_id)

    commit()

    return


def commit():
    """Commmit posting of observations
    """
    _commit()

    return




"""
Methods
"""

def list_record_types():
    """Return list of dict with record_types and number for each
    """
    query = session.query(func.count(Observation.record_type), Observation.record_type).group_by(Observation.record_type).all()

    records = []
    for n, t in query:

        record = {
            'record_type': t,
            'n': n
        }
        records.append(record)

    return records


def _get_observations(record_type, record_id, key, value):
    """ Return observations matching condition
    """
    query = session.query(Observation)

    if record_type:
        query = query.filter(Observation.record_type == record_type)

    if record_id:
        query = query.filter(Observation.record_id == record_id)
        
    if key:
        query = query.filter(Observation.key == key)

    if value:
        query = query.filter(Observation.value == value)


    return query



def _get_max_observations(record_type, record_id, key, value):

    query = _get_observations(record_type, record_id, key, value)

    query.order_by(Observation.credibility.desc()).order_by(Observation.credibility.created_date())

    # Limit
    query = query.limit(1)

    return query

def _get_summary(record_type = None, record_id = None, key = None, value = None):

    query1 = _get_observations(record_type, record_id, key, value)
    
    query = _get_summaries(query1)


    return query

def _get_summaries(query):
    """Returns best observation for each keys of records in scope of query
    """

    subquery1 = query

    if 1 == 0:
        # Get max cred for each key
        obs1 = aliased(Observation)
        subquery1 = session.query(obs1)

        # Filter 
        if record_type:
            subquery1 = subquery1.filter(obs1.record_type == record_type)
        
        if record_id:
            subquery1 = subquery1.filter(obs1.record_id == record_id)
    subquery1 = subquery1.subquery()

    # Filter for top credibility
    subquery2 = session.query(subquery1)
    subquery2 = subquery2.group_by(subquery1.c.record_type)
    subquery2 = subquery2.group_by(subquery1.c.record_id)
    subquery2 = subquery2.group_by(subquery1.c.key)
    subquery2 = subquery2.having(func.max(subquery1.c.credibility) == subquery1.c.credibility)
    subquery2 = subquery2.subquery()
    
    # Filter for top created date
    subquery3 = session.query(subquery2)
    subquery3 = subquery3.group_by(subquery2.c.record_type)
    subquery3 = subquery3.group_by(subquery2.c.record_id)
    subquery3 = subquery3.group_by(subquery2.c.key)
    subquery3 = subquery3.having(func.max(subquery2.c.created_date) == subquery2.c.created_date)

    return subquery3


def _get_summaries_by_value(record_type, record_id):
    """Returns best observation for each keys/values of records in scope of query
    """

    # Get max cred for each key
    obs1 = aliased(Observation)

    subquery1 = session.query(obs1)
    subquery1 = subquery1.filter(obs1.record_type == record_type)
    subquery1 = subquery1.filter(obs1.record_id == record_id)
    subquery1 = subquery1.subquery()
    
    # Filter for top credibility
    subquery2 = session.query(subquery1)
    subquery2 = subquery2.group_by(subquery1.c.key)
    subquery2 = subquery2.group_by(subquery1.c.value)
    subquery2 = subquery2.having(func.max(subquery1.c.credibility) == subquery1.c.credibility)
    subquery2 = subquery2.subquery()
    
    # Filter for top created date
    subquery3 = session.query(subquery2)
    subquery3 = subquery3.group_by(subquery2.c.key)
    subquery3 = subquery3.group_by(subquery2.c.value)
    subquery3 = subquery3.having(func.max(subquery2.c.created_date) == subquery2.c.created_date)

    # Order
    subquery3 = subquery3.order_by(subquery2.c.key)
    subquery3 = subquery3.order_by(subquery2.c.credibility.desc())
    subquery3 = subquery3.order_by(subquery2.c.created_date.desc())

    return subquery3




def _post_observation_from_record(record):
    
    if type(record) is list:
        for i in record:
            _post_observation_from_record(i)
        return


    if not record.get('created_date', None):
        record['created_date'] = datetime.datetime.now()

    record_ref_id = str(record.get('record_type', None)) + '/' + str(record.get('record_id', None))

    obs = Observation(
        observation_id = record.get('observation_id', None),
        ref_id = record_ref_id,
        datasource = record.get('datasource', None),
        agent = record.get('agent', None),
        instrument = record.get('instrument', None),
        object = record.get('object', None),
        result = record.get('result', None),
        start_time = record.get('start_time', None),
        end_time = record.get('end_time', None),
        valid = record.get('valid', None),

        record_type = record.get('record_type', None),
        record_id = record.get('record_id', None),
        key = record.get('key', None),
        value = record.get('value', None),
        credibility = record.get('credibility', None),
        created_date = record.get('created_date', None)    
        )

    session.add(obs)


def _update(old_record_type, old_record_id, new_record_type, new_record_id):

    # Step 1. Update record_ids
    query = session.query(Observation)
    query = query.filter(Observation.record_type == old_record_type)
    query = query.filter(Observation.record_id == old_record_id)

    query = query.update(
        {
            Observation.record_type: new_record_type, 
            Observation.record_id: new_record_id
            })


    # Step 2. Update references to record_ids
    old_record = {
        '@type': old_record_type,
        '@id': old_record_id
    }
    old_record = json.dumps(old_record, default=str)

    new_record = {
        '@type': new_record_type,
        '@id': new_record_id
    }
    new_record = json.dumps(new_record, default=str)

    query = session.query(Observation)
    query = query.filter(Observation.value == old_record)

    query = query.update(
        {
            Observation.value: new_record }
            )


def _commit():

    session.commit()



def _search(params, order_by = None, order_direction = None, limit = None, offset = None):
    """ Return entities matching multiple conditions
    """

    query = None

    obs0 = aliased(Observation)


    # Step 1. Find observations meeting conditions
    for key, operator, value in params:

        sub_query = session.query(obs0)

        if key == 'record_type':
            sub_query = sub_query.filter(obs0.record_type.like(value))
        elif key == 'record_id':
            sub_query = sub_query.filter(obs0.record_id.like(value))
        else:
            sub_query = sub_query.filter(obs0.key.like(key))
            sub_query = sub_query.filter(obs0.value.like(value))

        if query:
            query = query.intersect(sub_query)
        else:
            query = sub_query


    # Step 2. Retrieve all observations with same ref_id
    obs1 = aliased(Observation)
    query = query.join(obs1, obs0.ref_id == obs1.ref_id)


    # apply order_by
    if order_by:
        query = query.order_by("record_type")


    # apply limit and offset
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)



    return query


def _to_dict_single(record):


    if type(record) is dict:

        result = {}
        for c in record.keys():
            result[c] = getattr(record, c)


        result.pop('id')
        result.pop('ref_id')

        return result

    else:
        result = record._asdict()
        return result



def _to_dict(querys):
    # COnvert sqlalchemy classes to dicts
    records = []
    for r in querys:
        record = _to_dict_single(r)
        records.append(record)

    return records


