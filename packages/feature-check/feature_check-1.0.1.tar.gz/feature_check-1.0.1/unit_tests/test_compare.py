# Copyright (c) 2018, 2019, 2021  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

""" Test the version comparison functions. """

import unittest

import ddt  # type: ignore

from feature_check import expr as fexpr

from . import data


@ddt.ddt
class TestExpr(unittest.TestCase):
    """Test the full expression parsing and comparison."""

    @ddt.data(*data.COMPARE)
    @ddt.unpack
    def test_compare(self, var: str, op_name: str, right: str, expected: bool) -> None:
        """Test the comparison functions with word operands."""
        return self.do_test_compare(var, op_name, right, expected)

    @ddt.data(*data.COMPARE)
    @ddt.unpack
    def test_synonyms(self, var: str, op_name: str, right: str, expected: bool) -> None:
        """Test the comparison functions with word operands."""
        return self.do_test_compare(var, data.SYNONYMS[op_name], right, expected)

    def do_test_compare(
        self, var: str, op_name: str, right: str, expected: bool
    ) -> None:
        # pylint: disable=no-self-use
        """Test the comparison functions."""
        feature = " ".join([var, op_name, right])
        expr = fexpr.parse_simple(feature)
        assert isinstance(expr, fexpr.ExprOp)
        assert len(expr.args) == 2
        assert isinstance(expr.args[0], fexpr.ExprFeature)
        assert isinstance(expr.args[1], fexpr.ExprVersion)

        res = expr.evaluate(data.FEATURES)
        assert isinstance(res, fexpr.ResultBool)
        assert res.value == expected
