# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'trust/Instructions.html', 'total_q': 1}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_answer_x', 'training_answer_y']
    question = (
        'Suppose that participant A sent 20 points to participant B. '
        'Having received the tripled amount, participant B sent 50 points to '
        'participant A. In the end, how many points would participant A and B '
        'have?'
    )

    def participate_condition(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}


class Feedback1(Page):
    template_name = 'trust/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1, 'x': self.player.training_answer_x,
            'y': self.player.training_answer_y
        }



class Send(Page):

    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    template_name = 'trust/Send.html'

    form_model = models.Group
    form_fields = ['sent_amount']

    def participate_condition(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}


class SendBack(Page):

    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    template_name = 'trust/SendBack.html'

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def participate_condition(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'sent_amount': self.group.sent_amount,
                'tripled_amount': tripled_amount,
                'prompt':
                'Please enter a number from 0 to %s:' % tripled_amount}


class ResultsWaitPage(WaitPage):


    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    """This page displays the earnings of each player"""

    template_name = 'trust/Results.html'

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'sent_amount': self.group.sent_amount,
                'tripled_amount': tripled_amount,
                'sent_back_amount': self.group.sent_back_amount,
                'role': self.player.role(),
                'bonus': Constants.bonus,
                'result': self.player.payoff - Constants.bonus,
                'total': self.player.payoff}


def pages():
    return [
        Introduction,
        Question1,
        Feedback1,
        Send,
        WaitPage,
        SendBack,
        ResultsWaitPage,
        Results,
    ]
