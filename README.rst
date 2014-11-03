What's that?
============

`dprj` is an algorithm that extracts sounds from words. It's similar to
metaphone, except it's targeted at the french language only. While double
metaphone or similar can be ok to regroup content that sound more or less the
same, it becomes unusable when you want to get the real pronunciation of a
word, since it's mainly targeted at english. And we all know french can be
really tricky sometimes.

How to use it?
==============

.. code-block:: python

    >> from dprj import say
    >> say(u'chaussette')
    u'xst'

How reliable is it?
===================

Well, try it and see for yourself! There are still some cases to handle:

* plurals
* silent word endings (eg. ``f`` in ``nerf``, ``d`` in ``accord``, etc)
* french weirdnesses

If you get incorrect results for any word please let me know by filing and
issue.
