import rethinkdb as r

class GameDAO:
    def __init__(self, host='localhost', port=28015, db='game'):
        self._conn = r.connect(host=host, port=port, db=db)
    #
    #  get a Component of an Entity
    #  -> document
    def get_component_for_entity(self, component_name, entity_name):
        if isinstance(component_name, str) and isinstance(entity_name, str):
            try:
                result = r.table(component_name).get(entity_name).run(self._conn)
            except:
                return None
            return result
        else:
            raise ValueError('component_name and entity_name must be strings')
    #
    #  set a Component of an Entity
    #  -> bool (success)
    def set_component_for_entity(self, component_name, component_value, entity_name):
        if isinstance(component_name, str) and isinstance(component_value, dict) and component_value['entity']==entity_name:
            try:
                result = r.table(component_name).insert(
                    component_value,
                    conflict = 'replace'
                    ).run(self._conn)
            except:
                return False
            return True
        else:
            raise ValueError('component_name and entity_name must be strings, component_value must be a dict with key "entity" set to entity_name')
    #
    #  update a Component of an Entity
    #  -> bool (success)
    def update_component_for_entity(self, component_name, component_value, entity_name):
        if isinstance(component_name, str) and isinstance(component_value, dict) and component_value['entity']==entity_name:
            try:
                result = r.table(component_name).get(entity_name).update(
                    component_value
                    ).run(self._conn)
            except:
                return False
            return True
        else:
            raise ValueError('component_name and entity_name must be strings, component_value must be a dict with key "entity" set to entity_name')
    #
    #  delete a Component of an Entity
    #  -> bool (success)
    def delete_component_for_entity(self, component_name, entity_name):
        if isinstance(component_name, str) and isinstance(entity_name, str):
            try:
                result = r.table(component_name).get(entity_name).delete().run(self._conn)
            except:
                return False
            return True
        else:
            raise ValueError('component_name and entity_name must be strings')