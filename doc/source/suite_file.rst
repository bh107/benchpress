.. _SuiteFile:

==============
The Suite File
==============

The suite file contains the set of commands to execute and the results of said executions.
In Python, it is easy to create a suite file. You start by creating a list of :py:class:`dict` where each :py:class:`dict` specify a command to execute such as::

    [{
      'label': 'X-ray/10*10*1', # The label of the command
      'cmd': 'python xraysim.py 10*10*1',  # The command to execute
      'env': {}  # The environment variables that will be defined before execution
    }, {
      'label': 'X-ray/20*10*1',
      'cmd': 'python xraysim.py 20*10*1',
      'env': {}
    }]

And then you call :py:func:`benchpress.benchpress.create_suite`, which writes the suite file at the location specified with the command line argument ``--output``.


JSON schema
-----------

The suite format is defined in `json-schema <http://json-schema.org>`_:

.. raw:: html

    <script src="http://lbovet.github.io/docson/widget.js"
        data-schema="https://raw.githubusercontent.com/bh107/benchpress/master/benchpress/suite_schema.json">
    </script>

A example of a suite file that contains two commands; one finished and one pending::

    {
        "creation_date_utc": "2017-05-23T09:02:25.373696",
        "cmd_list": [
            {
                "cmd": "python xraysim.py 10*10*1",
                "jobs": [
                    {
                        "status": "finished",
                        "warmup": true,
                        "results": [
                            {
                                "stderr": "",
                                "success": true,
                                "stdout": "elapsed-time: 0.013244\n"
                            }
                        ],
                        "nruns": 1
                    }
                ],
                "env": {},
                "label": "X-ray/10*10*1"
            },
            {
                "cmd": "python xraysim.py 20*10*1",
                "jobs": [
                    {
                        "status": "pending",
                        "warmup": true,
                        "nruns": 1
                    }
                ],
                "env": {},
                "label": "X-ray/20*10*1"
            }
        ]
    }
