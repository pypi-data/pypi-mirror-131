from flask import Flask


class HaltException(Exception):

    def __init__(self, *args):
        super().__init__("modern-flask halted")
        self.args = args


def halt(*args):
    raise HaltException(*args)


def modern_flask(*args, **kwargs) -> Flask:
    app = Flask(*args, **kwargs)

    @app.errorhandler(404)
    def handle_404(_):
        return {"message": "not found"}, 404

    @app.errorhandler(HaltException)
    def handle_halt_exception(e: HaltException):
        if len(e.args) == 1:
            return e.args[0]
        return tuple(e.args)

    return app
