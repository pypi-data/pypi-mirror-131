'''JUQCS exceptions module.'''

class JuqcsError(Exception):
    '''Base class for errors raised by JuqcsProvider.'''
    pass

class MissingTokenError(JuqcsError):
    '''No access token could be found in the system.'''

class AuthenticationError(JuqcsError):
    '''User credentials were refused by the server.'''

class AllocationError(JuqcsError):
    '''Errors related to the resource allocation process.'''
    pass

class JobSubmitError(JuqcsError):
    '''Errors raised when a job submission failed.'''
    pass

class JobFailureError(JuqcsError):
    '''Errors raised when a job execution failed.'''
    pass

class DeallocationError(JuqcsError):
    '''Errors related to the resource deallocation process.'''
    pass

