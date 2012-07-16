from utils.ordereddict import OrderedDict
import const

# ==== Errors ====
#
# Errors usually come with a number and human readable text. Generally the text should be followed whenever possible,
# but a brief description of the numeric error codes are as follows:
#
#     -7  Use secure.gravatar.com
#     -8  Internal error
#     -9  Authentication error
#     -10 Method parameter missing
#     -11 Method parameter incorrect
#     -100  Misc error (see text)
#
const.ERRORS={7:'Use secure.gravatar.com',
        8:'Internal error',
        9:'Authentication error',
        10:'Method parameter missing',
        11:'Method parameter incorrect',
        100:'Misc error (see text)'}

#Rating
RATING=OrderedDict({-1:'unknown',0:'g',1:'pg',2:'r',3:'x'})
RATING.merge(RATING.reverse_dictionary())
const.rating=RATING

if __name__ == '__main__':
    print const.ERRORS
    print const.rating