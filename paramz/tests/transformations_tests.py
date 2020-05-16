#===============================================================================
# Copyright (c) 2020, CentraleSupélec
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of paramax nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================

import unittest
from paramz import transformations as transf
from paramz import domains as dom


class TransformationsTest(unittest.TestCase):

    # Generic construction test for "simple" transformation classes
    # (i.e., transformation classes that behave like singletons)
    def _test_construct_simple(self, cls):
        cls._instance = None
        t = cls()
        self.assertIsInstance(t, transf.Transformation)
        self.assertIsInstance(t, cls)
        self.assertEqual(cls(), t)
        self.assertEqual(cls._instance, t)

    def test_construct_Logexp(self):
        self._test_construct_simple(transf.Logexp)

    def test_construct_Exponent(self):
        self._test_construct_simple(transf.Exponent)

    def test_construct_NegativeLogexp(self):
        self._test_construct_simple(transf.NegativeLogexp)

    def test_construct_NegativeExponent(self):
        self._test_construct_simple(transf.NegativeExponent)

    def test_construct_Square(self):
        self._test_construct_simple(transf.Square)

    # Currently, Logistic is the only transformation class that is not "simple".
    def test_construct_Logistic(self):
        transf.Logistic._instances = []
        t = transf.Logistic(0, 1)
        self.assertIsInstance(t, transf.Transformation)
        self.assertIsInstance(t, transf.Logistic)
        self.assertEqual(transf.Logistic(0, 1), t)
        t2 = transf.Logistic(5, 10)
        self.assertNotEqual(t2, t)
        self.assertIsInstance(transf.Logistic._instances, list)
        self.assertEqual(len(transf.Logistic._instances), 2)


    def _test_callf_POSITIVE(self, cls):
        t = cls()
        self.assertIs(t.domain, dom._POSITIVE)
        p = t.f(0.)
        self.assertTrue(p >= 0.)

    def test_callf_Logexp(self):
        self._test_callf_POSITIVE(transf.Logexp)

    def test_callf_Exponent(self):
        self._test_callf_POSITIVE(transf.Exponent)

    def test_callf_Square(self):
        self._test_callf_POSITIVE(transf.Square)

    def _test_callf_NEGATIVE(self, cls):
        t = cls()
        self.assertIs(t.domain, dom._NEGATIVE)
        p = t.f(0.)
        self.assertTrue(p <= 0.)

    def test_callf_NegativeExponent(self):
        self._test_callf_NEGATIVE(transf.NegativeExponent)

    def test_callf_NegativeLogexp(self):
        self._test_callf_NEGATIVE(transf.NegativeLogexp)

    def _test_callf_BOUNDED(self, cls, lower=1.234, upper=5.678):
        t = cls(lower=lower, upper=upper)
        self.assertIs(t.domain, dom._BOUNDED)
        p = t.f(0.)
        self.assertEqual(t.lower, lower)
        self.assertEqual(t.upper, upper)
        self.assertTrue(p <= t.upper)
        self.assertTrue(p >= t.lower)

    def test_callf_Logistic(self):
        self._test_callf_BOUNDED(transf.Logistic)


    def _test_callfinv(self, t, p):
        self.assertAlmostEqual(t.f(t.finv(p)), p, delta=5e-16)

    def test_callfinv_Logexp(self):
        self._test_callfinv(transf.Logexp(), 1.234)

    def test_callfinv_Exponent(self):
        self._test_callfinv(transf.Exponent(), 1.234)

    def test_callfinv_Square(self):
        self._test_callfinv(transf.Square(), 1.234)

    def test_callfinv_NegativeExponent(self):
        self._test_callfinv(transf.NegativeExponent(), -2.345)

    def test_callfinv_NegativeLogexp(self):
        self._test_callfinv(transf.NegativeLogexp(), -2.345)

    def test_callfinv_Logistic(self):
        self._test_callfinv(transf.Logistic(5., 10.), 6.666)


if __name__ == "__main__":
    unittest.main()
