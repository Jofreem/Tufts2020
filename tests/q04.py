test = {
  'name': 'Question 4',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> fooWorld() #doctest: +ELLIPSIS
          Hello ...
          """,
          'hidden': False,
          'locked': False
        },
                  {
          'code': r"""
          >>> str(obj) #doctest: +ELLIPSIS
          <__main__.sample object at ...>
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}