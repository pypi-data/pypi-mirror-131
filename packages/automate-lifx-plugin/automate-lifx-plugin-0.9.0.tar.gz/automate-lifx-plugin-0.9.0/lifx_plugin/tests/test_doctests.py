import doctest
import lifx_plugin


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(lifx_plugin.gateway))
    tests.addTests(doctest.DocTestSuite(lifx_plugin.message))
    tests.addTests(doctest.DocTestSuite(lifx_plugin.trigger))
    tests.addTests(doctest.DocTestSuite(lifx_plugin.command))

    return tests
