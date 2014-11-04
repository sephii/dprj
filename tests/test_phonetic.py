# -*- coding: utf-8 -*-
from dprj import say


def test_ch():
    assert say(u'chanson') == u'xnsn'
    assert say(u'chrysanthème') == u'krsntm'
    assert say(u'archange') == u'rknj'
    assert say(u'archive') == u'rxv'


def test_sch():
    assert say(u'schizophrène') == u'skzfrn'
    assert say(u'schiste') == u'xst'


def test_ill():
    assert say(u'aiguille') == u'g'


def test_cc():
    assert say(u'accident') == u'ksdn'
    assert say(u'accès') == u'ks'
    assert say(u'accélération') == u'kslrsn'
    assert say(u'accord') == u'kr'
    assert say(u'accapare') == u'kpr'
    assert say(u'accueil') == u'k'


def test_final_il():
    assert say(u'accueil') == u'k'
    assert say(u'poil') == u'pl'


def test_final_x():
    assert say(u'couteaux') == u'kt'


def test_middle_x():
    assert say(u'exagère') == u'gzjr'
    assert say(u'axiome') == u'ksm'


def test_xc():
    assert say(u'exception') == u'kspsn'


def test_gn():
    assert say(u'araignée') == u'rn'


def test_final_s():
    assert say(u'sons') == u'sn'
    assert say(u'anis') == u'ns'
    assert say(u'flûtes') == u'flt'
    assert say(u'fluets') == u'fl'


def test_sc():
    assert say(u'scaphandre') == u'skfndr'
    assert say(u'science') == u'sns'


def test_final_f():
    assert say(u'aéronef') == u'rnf'
    assert say(u'clef') == u'kl'
    assert say(u'bref') == u'brf'
    assert say(u'nerf') == u'nr'


def test_double_letters():
    assert say(u'allée') == u'l'
    assert say(u'femme') == u'fm'
    assert say(u'attablé') == u'tbl'
