# -*- coding: utf-8 -*-

"""
byceps.blueprints.board.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from wtforms import Form, TextAreaField
from wtforms.validators import Required


class PostingCreateForm(Form):
    body = TextAreaField('Text', validators=[Required()])
