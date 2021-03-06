__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.json import merge_json

data_a = {
  "date": 20210101,
  "brands": {
    "new": [
      "toothpaste",
      "floss"
    ],
    "old": [
      "face cream",
      "skin cream"
    ]
  },
  "campaigns": [
    {
      "name": "west coast",
      "places": [
        {
          "city": "Seattle",
          "state": "WA"
        },
        {
          "city": "Portland",
          "state": "OR"
        }
      ]
    },
    {
      "name": "midwest",
      "places": [
        {
          "city": "Chicago",
          "state": "IL"
        },
        {
          "city": "Cincinnati",
          "state": "OH"
        }
      ]
    }
  ]
}
data_b = {
  "date": 20210102,
  "topic": "branding",
  "brands": {
    "protential": [
      "vitamins"
    ],
    "new": [
      "floss",
      "toothbrushes"
    ],
    "old": [
      "face cream"
    ]
  },
  "campaigns": [
    {
      "name": "midwest",
      "season": "winter",
      "places": [
        {
          "city": "Cincinnati",
          "neighborhood": "suburbs"
        }
      ]
    },
    {
      "name": "east coast",
      "places": [
        {
          "city": "Charleston"
        },
        {
          "city": "Philadelphia"
        }
      ]
    }
  ]
}

if __name__ == '__main__':

    output = 'test20210325c.json'
    sources = ['test20210325a.json', 'test20210325b.json']
    combined = merge_json(*sources, output=output)
    assert 'topic' in combined.keys()
    assert len(combined['brands']) > 2
    assert 'season' in combined['campaigns'][1].keys()
    assert 'neighborhood' in combined['campaigns'][1]['places'][1].keys()
    assert combined['date'] < 20210102
    
        
