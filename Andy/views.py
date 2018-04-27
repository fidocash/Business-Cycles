from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import math


class Explications(Page):
    def is_displayed(self):
        return self.round_number == 1

class Basic(Page):
    def is_displayed(self):
        return self.round_number==1

class Experiment(Page):

    def is_displayed(self):
        return self.round_number==1

class Examples(Page):
    def is_displayed(self):
        return self.round_number==1

class Finalremarks(Page):
    def is_displayed(self):
        return self.round_number == 1

class assign_WORKER(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.type=="agent"

class assign_EMPLOYER(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.type =="principal"

class Shock(Page):
    def is_displayed(self):
        return self.round_number==11


class beliefelicitation_instructions(Page):
    def is_displayed(self):
        return (self.round_number == 1 or self.round_number == 5 or self.round_number == 10 or self.round_number == 11 or self.round_number == 15) and self.player.type == 'principal'
    def vars_for_template(self):
        return{
            'num_round': self.subsession.round_number
        }



class beliefelicitation(Page):
    def is_displayed(self):
        return (self.round_number == 1 or self.round_number == 5 or self.round_number == 10) and self.player.type == 'principal'
    form_model= models.Player
    form_fields= ['eleffort1', 'eleffort2','eleffort3','eleffort4','eleffort5','eleffort6','eleffort7','eleffort8','eleffort9','eleffort10']

class beliefelicitationPOSITIVE(Page):
    def is_displayed(self):
        return (self.round_number == 11 or self.round_number == 15) and self.player.type == 'principal' and self.group.in_round(10).draw ==1
    form_model= models.Player
    form_fields= ['eleffort1', 'eleffort2','eleffort3','eleffort4','eleffort5','eleffort6','eleffort7','eleffort8','eleffort9','eleffort10','eleffort11','eleffort12']

    def vars_for_template(self):
        return{
            'num_round' : self.subsession.round_number,
        }

class beliefelicitationNEGATIVE(Page):
    def is_displayed(self):
        return (self.round_number == 11 or self.round_number == 15) and self.player.type == 'principal' and self.group.in_round(10).draw ==0
    form_model= models.Player
    form_fields= ['eleffort1', 'eleffort2','eleffort3','eleffort4','eleffort5','eleffort6','eleffort7','eleffort8']

    def vars_for_template(self):
        return{
            'num_round' : self.subsession.round_number,
        }

class strategyinstructions(Page):
    def is_displayed(self):
        return (self.round_number == 1 or self.round_number == 5 or self.round_number == 10 or self.round_number == 11 or self.round_number == 15) and self.player.type == 'agent'
    def vars_for_template(self):
        return{
            'num_round' : self.subsession.round_number,
        }

class strategymethod(Page):
    def is_displayed(self):
        return (self.round_number == 1 or self.round_number == 5 or self.round_number == 10) and self.player.type == 'agent'
    form_model= models.Player
    form_fields= ['steffort1', 'steffort2','steffort3','steffort4','steffort5','steffort6','steffort7','steffort8','steffort9','steffort10']

class strategymethodPOSITIVE(Page):
    def is_displayed(self):
        return (self.round_number == 11 or self.round_number == 15) and self.player.type == 'agent' and self.group.in_round(10).draw ==1
    form_model= models.Player
    form_fields= ['steffort1', 'steffort2','steffort3','steffort4','steffort5','steffort6','steffort7','steffort8','steffort9','steffort10','steffort11','steffort12']

class strategymethodNEGATIVE(Page):
    def is_displayed(self):
        return (self.round_number == 11 or self.round_number == 15) and self.player.type == 'agent' and self.group.in_round(10).draw ==0
    form_model= models.Player
    form_fields= ['steffort1', 'steffort2','steffort3','steffort4','steffort5','steffort6','steffort7','steffort8']

class beliefworker(Page):
    form_model = models.Player
    form_fields = ['wagebelief']
    def is_displayed(self):
        return (self.round_number == 1 or self.round_number == 5 or self.round_number == 10 or self.round_number == 11 or self.round_number == 15) and self.player.type == 'agent'
    def vars_for_template(self):
        return{
            'num_round': self.subsession.round_number,
        }
    def wagebelief_max(self):
        return self.group.actuale

class Offre_Principal(Page):
    form_model = models.Group
    form_fields = ['wage']

    def vars_for_template(self):
        return {
            'num_round': self.subsession.round_number,
        }

    def is_displayed(self):
        return self.player.type == 'principal'

    def wage_max(self):
        return self.group.actuale


class Choix_Agent(Page):
    form_model = models.Group
    form_fields = ['effort']

    def is_displayed(self):
        return self.player.type == 'agent' and (self.round_number==2 or self.round_number == 3 or self.round_number==4 or self.round_number == 6 or self.round_number==7 or self.round_number == 8 or self.round_number==9 or self.round_number == 12 or self.round_number==13 or self.round_number == 14 or self.round_number==16 or self.round_number ==17 or self.round_number==18 or self.round_number == 19 or self.round_number==20)

    def effort_max(self):
        return round(math.sqrt(2*self.group.wage),2)

    def vars_for_template(self):
        return {
            'offre_wage': self.group.wage,
            'effort_max':round(math.sqrt(2*self.group.wage),2),
            'num_round':self.subsession.round_number,
        }

class WaitPage(WaitPage):
    title_text = "Waiting Page"
    body_text = "Please wait the other participant to make his decision"
    def after_all_players_arrive(self):
        self.group.get_variables()
        self.group.calculate_payoff()
        self.group.check_payoff()

class WaitPage_1(WaitPage):
    def after_all_players_arrive(self):
        pass

class WaitPage_2(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


    def after_all_players_arrive(self):
        self.group.calculate_payoff_final_1()
        self.group.calculate_payoff_final_2()
        self.group.rounding()

class Results(Page):
    def vars_for_template(self):
        return {
            'offre_wage': self.group.wage,
            'effort': self.group.effort,
            'payoff': self.player.payoff,
            'payoff_other': self.player.get_others_in_group()[0].payoff,
            'num_round  ': self.subsession.round_number,
        }
    def is_displayed(self):
        return self.round_number!=1 and self.round_number!=5 and self.round_number!=10 and self.round_number!=11 and self.round_number!=15

class Waitforeveryone(Page):
    pass

class ResultsStrategy(Page):
    def vars_for_template(self):
        return {
            'offre_wage': self.group.wage,
            'payoff': self.player.payoff,
            'steffort': self.group.steffort,
            'num_round': self.subsession.round_number,
            'payoff_other': self.player.get_others_in_group()[0].payoff,
        }
    def is_displayed(self):
        return self.round_number==1 or self.round_number==5 or self.round_number==10 or self.round_number==11 or self.round_number==15

class FinalPayoff(Page):
    def vars_for_template(self):
        return {
            'final_payoff': self.player.final_payoff,
            'random_round_payoff_1': self.group.random_round_payoff_1,
            'random_round_payoff_2': self.group.random_round_payoff_2,
            'paidinPoint1or2_draw1': self.group.paidinPoint1or2_draw1,
            'paidinPoint1or2_draw2': self.group.paidinPoint1or2_draw2,
            'random_method_payoff_1': self.group.random_method_payoff_1,
            'random_method_payoff_2': self.group.random_method_payoff_2,
        }
    def is_displayed(self):
        return self.round_number==Constants.num_rounds

page_sequence = [
    #Explications,
    #Basic,
    #Examples,
    #Finalremarks,
    assign_WORKER,
    assign_EMPLOYER,
    Shock,
    beliefelicitation_instructions,
    beliefelicitation,
    beliefelicitationPOSITIVE,
    beliefelicitationNEGATIVE,
    strategyinstructions,
    beliefworker,
    strategymethod,
    strategymethodPOSITIVE,
    strategymethodNEGATIVE,
    Offre_Principal,
    WaitPage_1,
    Choix_Agent,
    WaitPage,
    WaitPage_2,
    #Waitforeveryone,
    Results,
    ResultsStrategy,
    FinalPayoff,
]
