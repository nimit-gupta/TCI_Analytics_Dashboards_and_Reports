from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app1 import app as app1
from app2 import app as app2
from app3 import app as app3
from app4 import app as app4
from app5 import app as app5
from app6 import app as app6
from app7 import app as app7
from app8 import app as app8
from app9 import app as app9
from app10 import app as app10
from app11 import app as app11
from app12 import app as app12
from flask_app import flask_app

application = DispatcherMiddleware(flask_app, {
                                                '/app1': app1.server,
                                                '/app2': app2.server,
                                                '/app3': app3.server,
                                                '/app4': app4.server,
                                                '/app5': app5.server,
                                                '/app6': app6.server,
                                                '/app7': app7.server,
                                                '/app8': app8.server,
                                                '/app9': app9.server,
                                                '/app10': app10.server,
                                                '/app11': app11.server,
                                                '/app12': app12.server,
                                              }
                                  )

if __name__ == '__main__':
    run_simple('127.0.0.1', 8050, application)