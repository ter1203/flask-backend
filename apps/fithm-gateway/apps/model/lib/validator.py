from flask import abort


class ModelValidator:

    def validate_update_positions(self, param: dict) -> dict:

        if 'positions' not in param:
            return

        positions = param['positions']
        if not isinstance(positions, list):
            abort(400, 'Positions must be an array')

        for position in positions:
            if 'symbol' not in position or 'weight' not in position:
                abort(400, 'Position must have symbol and weight attributes')

        symbol_list = [pos['symbol'] for pos in positions]
        if len(symbol_list) != len(set(symbol_list)):
            abort(400, 'Symbols can not be duplicated')
