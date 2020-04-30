test = {
  'name': 'Question 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> fooLead() #doctest: +NORMALIZE_WHITESPACE
          LeadingSpace
          """,
          'hidden': False,
          'locked': False
        },
          {
          'code': r"""
          >>> fooTrail() #doctest: +NORMALIZE_WHITESPACE
          TrailingSpace
          """,
          'hidden': False,
          'locked': False
        },
          {
          'code': r"""
          >>> fooAll() #doctest: +NORMALIZE_WHITESPACE
          Extra Spaces
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
