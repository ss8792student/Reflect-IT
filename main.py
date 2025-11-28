from reflect_engine import ReflectEngine
from session_logger import SessionLogger

engine = ReflectEngine()
logger = SessionLogger()

def handle_message(student, subject, msg):
    response, trigger = engine.generate(msg)
    logger.log(student, subject, trigger, msg, response)
    return response
