import opentracing
import http.client
from ..agents.jaeger import init_tracer
from opentracing import tags ,Tracer
from opentracing.propagation import Format
from flask import _request_ctx_stack as stack
from flask import Flask
from fastapi import FastAPI
from ..span.span import Span

class traceMiddleware(Tracer):

    """
    Tracer that can trace certain requests to a Flask app.
    @param tracer the OpenTracing tracer implementation to trace requests with
    """
    def __init__(self, app=None, tracer=None, trace_all_requests=True,
                    traced_attributes=[], start_span_cb=None):

        if start_span_cb is not None and not callable(start_span_cb):
            raise ValueError('start_span_cb is not callable')

        if trace_all_requests is True and app is None:
            raise ValueError('trace_all_requests=True requires an app object')

        if trace_all_requests is None:
            trace_all_requests = False if app is None else True

        if not callable(tracer):
            self.__tracer = None
            self.__tracer_getter = init_tracer
        else:
            self.__tracer = None
            self.__tracer_getter = tracer

        self._trace_all_requests = trace_all_requests
        self._start_span_cb = start_span_cb
        self._current_scopes = {}
        self._app = app
        self.fastapi_request = None
        if self._trace_all_requests:
            if isinstance(app, Flask):
                @app.before_request
                def start_trace():
                    request = stack.top.request
                    self.before_request(request)

                @app.after_request
                def end_trace(response):
                    request = stack.top.request
                    self.after_request(request,response)
                    return response
                    
            elif isinstance(app, FastAPI):
                @app.middleware("http")
                async def start_end_trace(request, call_next):
                    response = await self.before_fast_api(request,call_next)
                    self.fastapi_request = request
                    response = await call_next(request)
                    self.after_request(request, response)
                    return response
            else:
                raise TypeError("app type have to be etiher 'Flask' or 'fastapi'.")
  

    @property
    def _tracer(self):
        """DEPRECATED"""
        return self.tracer

    @property
    def tracer(self):
        if not self.__tracer:
            if self.__tracer_getter is None:
                return opentracing.tracer

            self.__tracer = self.__tracer_getter()
        return self.__tracer

    def trace(self, *attributes):
        """
        Function decorator that traces functions
        NOTE: Must be placed after the @app.route decorator
        @param attributes any number of flask.Request attributes
        (strings) to be set as tags on the created span
        """
        def decorator(f):
            def wrapper(*args, **kwargs):
                if self._trace_all_requests:
                    return f(*args, **kwargs)

                self.before_request(list(attributes))
                try:
                    r = f(*args, **kwargs)
                    self.after_request()
                except Exception as e:
                    self.after_request(error=e)
                    raise

                self.after_request()
                return r

            wrapper.__name__ = f.__name__
            return wrapper
        return decorator

    def before_request(self, request ):
        """
        Gather various info about the request and start new span with the data.
        """
        headers = dict(request.headers)
        method = request.method
        url = request.url
        body = request.data.decode("utf-8") 
        hostname = request.host
        ip = request.remote_addr
        query = request.query_string.decode("utf-8") 
        referer = request.referrer
        
        span_context = self.tracer.extract(
            format=Format.HTTP_HEADERS, carrier=headers
        )
        self.span = Span(f"{request.path}" ,span_context,self.tracer,True)
        scope = self.span.scope
        self._current_scopes[request] = scope
        self.span.log("req",{
            "body": body,
            "headers": headers,
            "hostname": hostname,
            "ip": ip,
            "query":query,
            "referer": referer,
            })

        self.span.tag(tags.HTTP_METHOD, method)
        self.span.tag(tags.COMPONENT, 'Flask')
        self.span.tag(tags.HTTP_URL, url)
        self.span.tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
        self._call_start_span_cb(self.span, request)

    def after_request(self,request, response=None, error=None):

        # the pop call can fail if the request is interrupted by a
        # `before_request` method so we need a default
        scope = self._current_scopes.pop(request, None)

        if scope is None:
            return
        
        
        if response is not None:
            response.headers["Trace-Id"] = format(self.span.getTracId(),"x")
            status_code = int(response.status_code)
            self.span.tag(tags.HTTP_STATUS_CODE,status_code)
            if ((status_code < 200) | (status_code >= 400)) : 
                self.span.markError("error" , {
                'error.kind': http.client.responses[status_code],
                })

        if error is not None:
            self.span.tag(tags.ERROR, True)
            self.span.log(tags.ERROR, {'error.object': error})

        scope.close()
    
    async def before_fast_api(self, request , call_next):
        """
        Gather various info about the request and start new span with the data.
        """
        
        headers = dict(request.headers)
        method = request.method
        url = request.url
        body = await request.body()
        body = body.decode("utf-8") 
        hostname = headers["host"]
        ip = request.client.host
        query = request.query_params
        referer = ""

        span_context = self.tracer.extract(
            format=Format.HTTP_HEADERS, carrier=headers
        )
        
        self.span = Span(f"{request.url.path}" ,span_context,self.tracer,True)
        scope = self.span.scope
        self._current_scopes[request] = scope
        self.span.log("req",{
            "body": body,
            "headers": headers,
            "hostname": hostname,
            "ip": ip,
            "query":query,
            "referer": referer,
            })
        self.span.tag(tags.HTTP_METHOD, method)
        self.span.tag(tags.COMPONENT, 'FastAPI')
        self.span.tag(tags.HTTP_URL, url)
        self.span.tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
        self._call_start_span_cb(self.span, request)


    def _call_start_span_cb(self, span, request):
        if self._start_span_cb is None:
            return

        try:
            self._start_span_cb(span, request)
        except Exception:
            pass
    
    def get_span(self, request=None):
        """
        Returns the span tracing `request`, or the current request if
        `request==None`.
        If there is no such span, get_span returns None.
        @param request the request to get the span from
        """
        if isinstance(self._app, Flask):
            if request is None and stack.top:
                request = stack.top.request
        elif isinstance(self._app, FastAPI):
            if request is None:
                request = self.fastapi_request

        scope = self._current_scopes.get(request, None)
        return None if scope is None else scope.span