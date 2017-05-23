==============
The Suite File
==============

The suite file specifies the set of commands to execute and the results of said executions. The suite format is defined in `json-schema <http://json-schema.org>`_:

.. raw:: html

    <script src="http://lbovet.github.io/docson/widget.js"
        data-schema="https://raw.githubusercontent.com/bh107/benchpress/master/benchpress/suite_schema.json">
    </script>

A example of a suite file that contains two commands; one finished and one pending::

    {
        "creation_date_utc": "2017-05-23T09:02:25.373696",
        "cmd_list": [
            {
                "cmd": "python xraysim.py --size=10*10*1",
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
                "cmd": "python xraysim.py --size=20*10*1",
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
