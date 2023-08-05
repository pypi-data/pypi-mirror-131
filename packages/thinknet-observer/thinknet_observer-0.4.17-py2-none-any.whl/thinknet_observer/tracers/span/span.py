from ..agents.jaeger import init_tracer
from opentracing import tags
import opentracing

class Span:
    
    def __init__(self,name,parent_span = None, tracer = None , active = None):
        if tracer == None:
            tracer = opentracing.tracer
        self.tracer = tracer
        if parent_span is None:
            if active:
                self.scope = self.tracer.start_active_span(name)
                self.span = self.scope.span
            else:
                self.span = self.tracer.start_span(name)
                
        else:
            if active:
                self.scope = self.tracer.start_active_span(name,child_of=parent_span)
                self.span = self.scope.span
            else:
                self.span = self.tracer.start_span(name,child_of=parent_span)
  

    def tracers(self):
        return self.tracer

    def tag(self,key, value):
        return self.span.set_tag(key,value)
    
    def log(self,name, payload = None):
        data = {"event" : name}
        if payload:
            data["payload"] = payload
        return self.span.log_kv(data)
    
    def finish(self):
        return self.span.finish()

    def close(self):
        return self.tracer.close()
    
    def getTracId(self):
        return self.span.trace_id
    
    def markError(self , name , payload = None):
        self.tag(tags.SAMPLING_PRIORITY, 1)
        self.tag(tags.ERROR, True)
        return self.log(name , payload )