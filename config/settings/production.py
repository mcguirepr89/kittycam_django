from .base import *                                          
import os
from dotenv import load_dotenv

load_dotenv("/etc/kittycam/.env")
                                                             
DEBUG = False                                                
                                                             
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True                           
SECURE_SSL_REDIRECT = True                                   
SECURE_REFERRER_POLICY = "same-origin"                       
                                                             
USE_X_FORWARDED_HOST = True                                  
                                                             
CSRF_COOKIE_SECURE = True                                    
                                                             
SESSION_COOKIE_SECURE = True                                 

CSRF_TRUSTED_ORIGINS = parse_hosts(
    os.environ.get("CSRF_TRUSTED_ORIGINS", "")
)
