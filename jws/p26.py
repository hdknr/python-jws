import unittest
class _AssertRaisesContext(object):
    """A context manager used to implement TestCase.assertRaises* methods."""

    def __init__(self, expected, test_case, expected_regexp=None):
        self.expected = expected
        self.failureException = test_case.failureException
        self.expected_regexp = expected_regexp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise self.failureException(
                "{0} not raised".format(exc_name))
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True


def assertIn(self, test_value, expected_set):
    msg = "%s did not occur in %s" % (test_value, expected_set)
    self.assert_(test_value in expected_set, msg)

def assertRaises(self, excClass, callableObj=None, *args, **kwargs):
    ''' copied from Python2.7 unitttest'''
    context = _AssertRaisesContext(excClass, self)
    if callableObj is None:
        return context
    with context:
        callableObj(*args, **kwargs)

unittest.TestCase.assertIn= assertIn
unittest.TestCase.assertRaises= assertRaises
