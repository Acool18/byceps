# -*- coding: utf-8 -*-

"""
byceps.blueprints.ticket_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import request

from ...database import db
from ...util.framework import create_blueprint
from ...util.templating import templated

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry
from ..party.models import Party
from ..ticket.models import Ticket

from .authorization import TicketPermission


blueprint = create_blueprint('ticket_admin', __name__)


permission_registry.register_enum(TicketPermission)


@blueprint.route('/for_party/<party_id>', defaults={'page': 1})
@blueprint.route('/for_party/<party_id>/pages/<int:page>')
@permission_required(TicketPermission.list)
@templated
def index_for_party(party_id, page):
    """List tickets for that party."""
    party = Party.query.get_or_404(party_id)

    per_page = request.args.get('per_page', type=int, default=15)
    query = Ticket.query \
        .for_party(party) \
        .options(
            db.joinedload('category'),
            db.joinedload('owned_by'),
            db.joinedload('occupied_seat').joinedload('area'),
        ) \
        .order_by(Ticket.created_at)

    tickets = query.paginate(page, per_page)

    return {
        'party': party,
        'tickets': tickets,
    }


@blueprint.route('/<uuid:id>')
@permission_required(TicketPermission.view)
@templated
def view(id):
    """Show a ticket."""
    ticket = Ticket.query \
        .options(
            db.joinedload('category'),
            db.joinedload('occupied_seat').joinedload('area'),
            db.joinedload('owned_by'),
            db.joinedload('seat_managed_by'),
            db.joinedload('user_managed_by'),
        ) \
        .get_or_404(id)

    return {
        'ticket': ticket,
    }
