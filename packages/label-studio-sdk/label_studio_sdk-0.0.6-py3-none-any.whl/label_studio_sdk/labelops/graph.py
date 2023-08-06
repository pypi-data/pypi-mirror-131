import neo4j
from neo4j import GraphDatabase


class LabelGraphDB1(object):

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, command, parameters=None):
        with self.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
            result = session.run(command, parameters)
            return list(result)

    def clear_graph(self):
        self.run('MATCH (n) DETACH DELETE n')

    # def create_nodes_and_relations(self, pairs):
    #     query = '''
    #         UNWIND $pairs AS row
    #         WITH row.first as prev, row.second as next, row.relation as rel
    #         MERGE (r1:Region {task: prev.task, start: prev.start, end: prev.end, label: prev.label, text: prev.text, type: prev.type})
    #         MERGE (r2:Region {task: next.task, start: next.start, end: next.end, label: next.label, text: next.text, type: next.type})
    #         MERGE (r1)-[:rel]->(r2)
    #         RETURN count(*) as total
    #     '''
    #     return self.run(query, parameters={'pairs': pairs})

    def create_nodes_and_relations(self, pairs):
        query = '''
            UNWIND $pairs as p
            CREATE (x:Region)-[r:p.relation]->(y:Region)
            SET r1 = p.first.values
            SET r2 = p.second.values
            RETURN x,r,y
        '''
        return self.run(query, parameters={'pairs': pairs})

    def close(self):
        self.driver.close()

    def _safe_int(self, i):
        return int(i) if i is not None else -1

    def _convert(self, result, task):
        return {
            "id": result['id'],
            "task": task,
            "label": result["value"][result["type"]][0],
            "start": self._safe_int(result["value"].get("start")),
            "end": self._safe_int(result["value"].get("end")),
            "text": result["value"].get("text", "null"),
            "type": result["from_name"]
        }

    def build_graph(self, predictions):
        # create ID map
        pairs = []
        for prediction in predictions:
            results = prediction['result']
            regions = {r['id']: self._convert(r, prediction["task"]) for r in results if 'id' in r}
            relations = [(r['from_id'], r['to_id']) for r in results if r['type'] == 'relation']
            for from_id, to_id in relations:
                pairs.append({
                    'first': regions[from_id],
                    'second': regions[to_id],
                    'relation': 'next'
                })
        count = self.create_nodes_and_relations(pairs)
        print(f'{count} nodes created.')


# class LabelGraph(object):
#
#     def query(self, command, parameters):
#         db = LabelGraphDB('bolt://localhost:7687', 'neo4j', 'password')
#         print(command, parameters)
#         result = db.run(command, parameters)
#         db.close()
#         return result
#
#     def add_predictions(self, predictions):
#         db = LabelGraphDB('bolt://localhost:7687', 'neo4j', 'password')
#         db.clear_graph()
#         db.build_graph(predictions)
#         db.close()


class LabelGraphDB(object):

    def __init__(self, uri, db_name, password):
        self.uri = uri
        self.db_name = db_name
        self.password = password

        self._driver = GraphDatabase.driver(uri, auth=(db_name, password))

    def run(self, command, parameters=None):
        with self._driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
            result = session.run(command, parameters)
            return list(result)

    def clear_graph(self):
        self.run('MATCH (n) DETACH DELETE n')

    def create_nodes_and_relations(self, pairs):
        query = '''
            UNWIND $pairs as p
            CREATE (x:Region)-[r:p.relation]->(y:Region)
            SET r1 = p.first.values
            SET r2 = p.second.values
            RETURN x,r,y
        '''
        return self.run(query, parameters={'pairs': pairs})

    def add_nodes_from_tasks(self, tasks):
        query = '''
            UNWIND $tasks as task
            CREATE (x:Region)-[:from]->(t:Task)
            SET x = task.data
            SET t.id = task.id
            RETURN count(x)
        '''
        return self.run(query, parameters={'tasks': tasks})

    def add_nodes_from_predictions(self, predictions):
        raise NotImplementedError

    def match_regex(self, regex):
        query = '''
            MATCH (r:Region)
            WHERE r.text =~ $regex
            RETURN r
        '''
        return self.run(query, parameters={'regex': regex})

    def match_regex_and_label(self, regex, label):
        query = '''
            MATCH (r:Region)
            WHERE r.text =~ $regex
            CREATE (l:Label {label:$label})-[:to]->(r)
            RETURN r
        '''
        return self.run(query, parameters={'regex': regex, 'label': label})

    def apply(self, label_ops):
        full_query = ''
        full_parameters = {}
        for label_op in label_ops:
            query = label_op.get_query()
            if query:
                full_query += query + '\n'
        full_query += 'RETURN r'
        return self.run(full_query, parameters=label_ops[0].get_parameters())

    def add_predictor(self):
        pass

    def add_predictions(self):
        pass

    def commit(self, project):
        query = '''
            MATCH (l:Label)-->(r:Region)-->(t:Task)
            return l.label as label, r as region, t.id as task
        '''
        results = self.run(query)
        predictions = []
        for result in results:
            print(result['task'])
            predictions.append({
                'task': result['task'],
                'result': result['label'],
                'score': 1.0
            })
        project.create_predictions(predictions)

