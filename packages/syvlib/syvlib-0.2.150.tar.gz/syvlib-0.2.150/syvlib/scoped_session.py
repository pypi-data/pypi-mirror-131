from contextlib import contextmanager

from .session import Session


@contextmanager
def scoped_session(url, username, password):
    session = Session(url, username, password)
    try:
        yield session
    finally:
        session.exit()

