from library.extension import ma


class Total_priceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'chessBoard', 'turn',  'codeGame',
                  'player1', 'player2', 'winner', 'time_player1', 'time_player2', 'total_time1', 'total_time2')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'score', 'numMatch')


class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class SeedSchema(ma.Schema):
    teams = ma.Nested(TeamSchema, many=True)  # Nested relationship

    class Meta:
        fields = ('id', 'matchID', 'result', 'teams')


class RoundSchema(ma.Schema):
    seeds = ma.Nested(SeedSchema, many=True)  # Nested relationship

    class Meta:
        fields = ('id', 'title', 'seeds')
