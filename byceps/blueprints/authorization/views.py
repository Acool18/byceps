# -*- coding: utf-8 -*-

"""
byceps.blueprints.authorization.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...util.framework import create_blueprint

from .registry import permission_registry
from .models import Permission


blueprint = create_blueprint('authorization', __name__)


@blueprint.app_context_processor
def add_permission_enums_to_template_context():
    return {e.__name__: e for e in permission_registry.get_enums()}