from library.extension import ma 

class Total_priceSchema(ma.Schema):
    class Meta :
        fields = ('id','chessBoard','turn')

