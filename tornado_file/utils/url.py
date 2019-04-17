from handlers.Passpory import IndexHandler,ChatHandler

handlers=[
    (r"/", IndexHandler),
    (r"/chat", ChatHandler),
]