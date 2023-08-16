# certifi-system-store-wrapper
A certifi hack to use system trust store and use's own CA.


## References
- https://gitlab.com/alelec/python-certifi-win32
  - This is a Windows-only library that hooks certifi and modifies it
    to return a list of certification authorities installed on the
    system. Although it no longer seems to be maintained, the code to
    retrieve Windows Certificate Authority information was
    particularly helpful.

- https://gitlab.com/alelec/pip-system-certs
  - It extends the requests library to use the certificate authority
    information from the ssl library, which is a successor to
    python-certifi-win32, but it is a bit harder to use because it is
    limited to requests.

- https://github.com/tiran/certifi-system-store
  - It is designed for almost the same purpose as this library, but
    unfortunately it is for Linux/FreeBSD only. The information about
    the location of the certificate authority for each Linux
    distribution is very helpful.
  
  







