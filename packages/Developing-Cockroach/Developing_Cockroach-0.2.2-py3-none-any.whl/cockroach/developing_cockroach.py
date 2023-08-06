"""
Debug. Custom log for Python3 apps.

You have a registration option for your app. Which is to use log. This is usually done using the print() statement:
The option for application logging is to use the developer.log() function. This allows you to include a little more granularity and information in the log output. Here is an example:

import developer
developer.log(message= "Hello World!")

OUTPUT: \033[33;2m[Log]:\033[0m\033[33m Hello World!\033[0m

Note: You will see logs in yellow color on your system console. In the next update you will be able to choose the colors.
"""
log = lambda message: print("\033[33;2m[Log]:\033[0m" + " " + "\033[33m{}\033[0m".format(message))
log.__doc__ = """Returns the result printing in yellow color.

     Parameters:
         log (message): The message that will be converted to log.

     The "message" parameter can take any type whether int or string, boolean or float.
"""
if __name__ == "__main__":
    log(message="Hello World!")