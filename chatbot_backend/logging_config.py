import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level=logging.INFO, log_dir="logs"):
    """
    Set up centralized logging for the entire project
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
    
    Returns:
        dict: Dictionary of configured loggers for different components
    """
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Define log format
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Clear any existing handlers to avoid duplicates
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure different loggers for different components
    loggers = {}
    
    # 1. Main application logger
    main_logger = logging.getLogger('chatbot.main')
    main_logger.setLevel(log_level)
    
    # Main app file handler (rotating)
    main_handler = logging.handlers.RotatingFileHandler(
        log_path / 'main.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    main_handler.setLevel(log_level)
    main_handler.setFormatter(detailed_formatter)
    main_logger.addHandler(main_handler)
    
    # 2. API/Services logger
    api_logger = logging.getLogger('chatbot.api')
    api_logger.setLevel(log_level)
    
    api_handler = logging.handlers.RotatingFileHandler(
        log_path / 'api.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    api_handler.setLevel(log_level)
    api_handler.setFormatter(detailed_formatter)
    api_logger.addHandler(api_handler)
    
    # 3. Vector database operations logger
    vector_logger = logging.getLogger('chatbot.vector')
    vector_logger.setLevel(log_level)
    
    vector_handler = logging.handlers.RotatingFileHandler(
        log_path / 'vector_db.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    vector_handler.setLevel(log_level)
    vector_handler.setFormatter(detailed_formatter)
    vector_logger.addHandler(vector_handler)
    
    # 4. Tools logger
    tools_logger = logging.getLogger('chatbot.tools')
    tools_logger.setLevel(log_level)
    
    tools_handler = logging.handlers.RotatingFileHandler(
        log_path / 'tools.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    tools_handler.setLevel(log_level)
    tools_handler.setFormatter(detailed_formatter)
    tools_logger.addHandler(tools_handler)
    
    # 5. Error logger (all errors from all components)
    error_logger = logging.getLogger('chatbot.errors')
    error_logger.setLevel(logging.ERROR)
    
    error_handler = logging.handlers.RotatingFileHandler(
        log_path / 'errors.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Add error handler to all loggers
    main_logger.addHandler(error_handler)
    api_logger.addHandler(error_handler)
    vector_logger.addHandler(error_handler)
    tools_logger.addHandler(error_handler)
    
    # 6. Console handler for development (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add console handler to main logger only (to avoid spam)
    main_logger.addHandler(console_handler)
    
    # Store loggers in dictionary
    loggers = {
        'main': main_logger,
        'api': api_logger,
        'vector': vector_logger,
        'tools': tools_logger,
        'errors': error_logger
    }
    
    # Log the setup completion
    main_logger.info("Logging system initialized successfully")
    main_logger.info(f"Log files will be stored in: {log_path.absolute()}")
    
    return loggers

def get_logger(component_name):
    """
    Get a logger for a specific component
    
    Args:
        component_name: Name of the component ('main', 'api', 'vector', 'tools')
    
    Returns:
        logging.Logger: Configured logger
    """
    logger_map = {
        'main': 'chatbot.main',
        'api': 'chatbot.api', 
        'vector': 'chatbot.vector',
        'tools': 'chatbot.tools',
        'errors': 'chatbot.errors'
    }
    
    logger_name = logger_map.get(component_name, 'chatbot.main')
    return logging.getLogger(logger_name)

def log_function_call(logger):
    """
    Decorator to log function calls and execution time
    
    Usage:
        @log_function_call(get_logger('api'))
        def my_function():
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger.debug(f"Calling {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.debug(f"{func.__name__} completed in {duration:.2f}s")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator

if __name__ == "__main__":
    loggers = setup_logging()
    
    # Test the logging setup
    main_logger = loggers['main']
    api_logger = loggers['api']
    vector_logger = loggers['vector']
    tools_logger = loggers['tools']
    
    main_logger.info("Testing main logger")
    api_logger.info("Testing API logger")
    vector_logger.info("Testing vector logger") 
    tools_logger.info("Testing tools logger")
    
    # Test error logging
    try:
        raise ValueError("Test error")
    except ValueError:
        main_logger.exception("Test exception logging")
    
    print("Logging setup complete! Check the 'logs' directory for log files.")