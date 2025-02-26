import json
import logging
import os
from inspect import stack


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        caller_stack = self._get_caller_stack()
        
        record.lineno = caller_stack.lineno
        record.filename = os.path.splitext(
            os.path.basename(caller_stack.filename)
        )[0]
        record.funcName = caller_stack.function
        return True
    
    @staticmethod
    def _get_caller_stack():
        stacks = stack()
        
        index = [
            index for index, item in enumerate(stacks)
            if item.function == "_do_log"
        ][0]
        index = index + 2
        
        return stacks[index]
    
def _build_format():
    fmt = """
    {
        "code_line": "%(filename)s:%(lineno)d - %(funcName)s()",
        "log_code": "%(log_code)s",
        "log_message": "%(message)s",
        "payload": %(payload)s,
        "severity": "%(levelname)s"
    }
    """
    
    fmt = fmt.replace("\n", "")
    fmt = " ".join(fmt.split())
    
    return fmt

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

logging.basicConfig(format=_build_format(), level=logging.INFO)

logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

LOGGER = logging.getLogger("api_contas")
LOGGER.addFilter(LogFilter())

class Logger:
    @staticmethod
    def info(log_code:str, log_message: str, payload: object = ""):
        _do_log(logging.INFO, log_code, log_message, payload)
        
    @staticmethod
    def warn(log_code:str, log_message: str, payload: object = ""):
        _do_log(logging.WARN, log_code, log_message, payload)
        
    @staticmethod
    def error(log_code:str, log_message: str, payload: object = ""):
        _do_log(logging.ERROR, log_code, log_message, payload)
        
        
def _do_log(level: int, log_code: str, log_message: str, payload: object):
    LOGGER.log(
        level=level,
        msg=log_message,
        extra={
            "log_code": log_code,
            "payload": json.dumps(payload)
        }
    )
