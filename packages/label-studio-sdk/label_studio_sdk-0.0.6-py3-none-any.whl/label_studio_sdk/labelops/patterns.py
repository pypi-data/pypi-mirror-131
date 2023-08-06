from pydantic import BaseModel
from typing import Dict


class Pattern(object):

    def __init__(self, query=None, parameters=None):
        self.query = query
        self.parameters = parameters


class Regex(Pattern):

    def __init__(self, **kwargs):
        expr = ''
        for key, pattern in kwargs.items():
            if expr:
                expr += ' AND '
            expr += f'r.{key} =~ {pattern}'
        super(Regex, self).__init__(query=f'MATCH (r:Region) WHERE {expr}')


class Entity(Pattern):
    pass


class EntitySequence(Pattern):
    pass


class LabelOp(BaseModel):
    label: str
    pattern: Pattern

    class Config:
        arbitrary_types_allowed = True

    def get_query(self):
        if self.pattern.query:
            return self.pattern.query + '\nCREATE (l:Label {label:$label})-[:to]->(r)'

    def get_parameters(self):
        return dict(label=self.label, **self.pattern.parameters)
