from .base import *                                          
                                                             
DEBUG = False                                                
                                                             
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True                           
SECURE_SSL_REDIRECT = True                                   
SECURE_REFERRER_POLICY = "same-origin"                       
                                                             
USE_X_FORWARDED_HOST = True                                  
                                                             
CSRF_COOKIE_SECURE = True                                    
                                                             
SESSION_COOKIE_SECURE = True                                 

