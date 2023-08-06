##########
Abyssinica
##########

Locale functions for the countries of Eritrea and Ethiopia.

See also `HornMT <https://github.com/gebre/HornMT/>`_: a machine-learning corpus for the Horn of Africa region.

*************
Functionality
*************

Numerals
========
Convert between Arabic and Ge'ez numerals::

    >>> from abyssinica.numerals import arabic_to_geez
    >>> arabic_to_geez(42)
    '፵፪'

    >>> from abyssinica.numerals import geez_to_arabic
    >>> geez_to_arabic('፵፪')
    42

Romanization
============
Transliterate Ge'ez characters::

    >>> from abyssinica.romanization import romanize
    >>> print(f"{romanize('ሰላም እንደምን አለህ?').capitalize()}")
    Salām ʼendamn ʼalah?

**********************
Upcoming Functionality
**********************

Date & Time
===========
Convert between Ge'ez and Gregorian dates and times.
