# -*- coding: utf-8 -*-
import private_value_auction.models as models
from private_value_auction.utilities import ParticipantMixIn
import ptree.forms


class BidForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['bid_amount']

    def choices(self):
        return {'bid_amount': self.match.get_bid_field_choices()}

    def labels(self):
        return {'bid_amount': 'Your Bid Amount?'}
