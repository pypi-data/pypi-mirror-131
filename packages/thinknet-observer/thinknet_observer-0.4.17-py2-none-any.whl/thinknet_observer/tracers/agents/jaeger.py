import os
from jaeger_client import Config

def init_tracer():
    config = Config(
        config= {
            "sampler" : {"type" : "const" , "param" : 1} ,
                "reporter": {
            "agentHost": os.environ.get("TRACE_AGENT_HOST","127.0.0.1"),
            "agentPort": os.environ.get("TRACE_AGENT_PORT","16686")
        }} ,
        service_name= str(os.environ.get("SERVICE_NAME_PREFIX","example")) + "/" + str(os.environ.get("SERVICE_NAME","test-service")),
    )
    tracer = config.initialize_tracer()
    if tracer is None:
        Config._initialized = False
        tracer = config.initialize_tracer()

    return tracer