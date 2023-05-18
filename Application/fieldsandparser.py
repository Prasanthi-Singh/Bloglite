from flask_restful import reqparse, fields

list_parse=reqparse.RequestParser()
list_parse.add_argument("l_name")
list_parse.add_argument("l_description")


card_parse=reqparse.RequestParser()
card_parse.add_argument("c_name")
card_parse.add_argument("c_description")
card_parse.add_argument("deadline")

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')


# deck_fields={
#     "deck_id": fields.Integer(attribute="id"),
#     "deck_name":fields.String(attribute="name"),
#     "deck_cards": fields.List(fields.Nested(card_fields),attribute="cards")
# }

# deck_lite={
#     "deck_id": fields.Integer(attribute="id"),
#     "deck_name":fields.String(attribute="name"),
    
# }

# user_decks={
#     "deck_id": fields.Integer(attribute="id"),
#     "deck_name":fields.String(attribute="name"),
# }
# follower_fields={
#     "follower_id" : fields.Integer,   
# }
# following_fields={
#     "follower_id" : fields.Integer,   
# }




post_fields={
    "post_name": fields.String,
    "post_id" : fields.Integer,
    "post_time" : fields.DateTime,
    "post_descr" : fields.String,
    "image" : fields.String,
    
}
user_fields={
    "user_name": fields.String,
    "user_id" : fields.Integer,
    "email" : fields.String,
    "password" : fields.String,
    "image" : fields.String,
    "bio" : fields.String,
    "post" : fields.List(fields.Nested(post_fields)),
}

