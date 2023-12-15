from library.extension import ma


class Total_priceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'chessBoard', 'turn',  'codeGame',
                  'player1', 'player2', 'winner', 'time_player1', 'time_player2', 'total_time1', 'total_time2')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'score', 'numMatch')
