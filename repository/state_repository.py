import json
from data.db_provider import DbProvider
from states_events.states import *
from states_events.events import *
from mapping.state_mapping import *


class StateRepository:

    def __init__(self, db_provider: DbProvider):
        self.db_provider = db_provider
    
    def create(self, state: BotState, user_id: int):
        state_json = json.dumps(state_to_dict(state))
        self.db_provider.execute_query(
            '''INSERT INTO user_bot_states (user_id, state_json) VALUES (%s, %s)''',
            (
                user_id,
                state_json,
            )
        )

    def update(self, state: BotState, user_id: int):
        state_json = json.dumps(state_to_dict(state))
        self.db_provider.execute_query(
            '''UPDATE user_bot_states SET state_json = %s WHERE user_id = %s''',
            (
                state_json,
                user_id,
            )
        )

    def read(self, user_id: int) -> BotState:
        row = self.db_provider.execute_read_query(
            '''SELECT * FROM user_bot_states WHERE user_id = %s''',
            (user_id,)
        )[0]
        dict_json = json.loads(row[1])
        return dict_to_state(dict_json)

    def read_or_create(self, state: BotState, user_id: int) -> BotState:
        try:
            return self.read(user_id=user_id)
        except:
            self.create(state, user_id)
            return state
        