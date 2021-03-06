from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools, random
import numpy as np



author = ''

doc = """
Modified Gift Exchange Game
"""



class Constants(BaseConstants):

    name_in_url = 'Andy_is_the_best'
    players_per_group = 2
    num_rounds = 3
    Endowment = 10
    instructions_template = 'Andy/Summary.html'
    Endowmenthigh= 12 #endowment after positive shock
    Endowmentlow=8 #endowment after - shock
    round_specials = [1,5,10,11,15] #these are the rounds with belief elicitation
    bonus_if_in_internal = 5 ##this is the belief payment

class Subsession(BaseSubsession):

    def creating_session(self):
        for g in self.get_groups():
            g.draw = np.random.random_integers(low=0,high=1)
            g.draw2 = np.random.random_integers(low=0, high=1)
            for p in g.get_players():
                p.type = ['principal', 'agent'][p.id_in_group - 1]

class Group(BaseGroup):
    actuale = models.IntegerField(initial=Constants.Endowment, min=1, max=100)                                          #endowment
    wage = models.IntegerField(min=1)                                                                                   #the wage snet by the firm
    effort = models.FloatField(min=0, max=4, widget= widgets.SliderInput(attrs={'step': '0.1'}))                        #the effort of worker in normal rounds
    steffort= models.FloatField(min=0, max=4)                                                                           #effort from strategy method
    draw = 0 #models.IntegerField(initial=np.random.random_integers(low=0,high=1))                                         #random draw to decide whether + or - shock
    random_round_payoff_1 = models.IntegerField()                                                                       #rnd draw to choose rounds to pay
    random_round_payoff_2 = models.IntegerField()
    random_method_payoff_1 = models.IntegerField()
    random_method_payoff_2 = models.IntegerField()
    random_line_belief_payoff_1 = models.IntegerField()
    random_line_belief_payoff_2 = models.IntegerField()
    paidinPoint1or2_draw1 = models.IntegerField(initial=0)
    paidinPoint1or2_draw2 = models.IntegerField(initial=0)

    def get_variables(self): #function to get effort stated in the strategy method
        players = self.get_players()
        for p in players:
            if p.type == 'agent':
                if self.round_number==1 or self.round_number==5 or self.round_number==10 or self.round_number==11 or self.round_number==15:
                    if self.wage == 10:
                        self.steffort = p.steffort10
                    elif self.wage == 2:
                        self.steffort= p.steffort2
                    elif self.wage == 3:
                        self.steffort= p.steffort3
                    elif self.wage == 4:
                        self.steffort= p.steffort4
                    elif self.wage == 5:
                        self.steffort= p.steffort5
                    elif self.wage == 6:
                        self.steffort= p.steffort6
                    elif self.wage == 7:
                        self.steffort= p.steffort7
                    elif self.wage == 8:
                        self.steffort= p.steffort8
                    elif self.wage == 9:
                        self.steffort= p.steffort9
                    else :
                        self.steffort= p.steffort1



    def calculate_payoff_final_1(self): #compute payoffs in the final round
        # choose randomly a round
        Liste_round = random.sample(list(range(1,Constants.num_rounds + 1)),2)
        print("This is liste round",Liste_round)
        print("this is the class of liste round", type(Liste_round))
        self.random_round_payoff_1 = Liste_round[0]
        self.random_round_payoff_2 = Liste_round[1]
        print("go fuck yourself_1", self.random_round_payoff_1)
        print("go fuck yourself_2", self.random_round_payoff_2)


        #if randomly choose round is in list then randomly choose a payoff method
        if self.random_round_payoff_1 in Constants.round_specials:
            self.paidinPoint1or2_draw1=1
            self.random_method_payoff_1 = 0 #np.random.choice(
                #[0, 1], 1,
                #p=[0.5, 0.5]
            #)[0]
            print("This is the method chosen (BELIEF vs STRATEGY):", self.random_method_payoff_1)
            if self.random_method_payoff_1 == 1:
                #Belief eliciation method
                self.random_line_belief_payoff_1 = random.randint(1,self.in_round(self.random_round_payoff_1).actuale)
                print("this is the first random line",self.random_line_belief_payoff_1)
                #now go find the choices of the players in that particular round
                for p in self.get_players():
                    if p.type == "agent":
                        # check accuracy
                        if p.in_round(self.random_round_payoff_1).wagebelief == self.in_round(self.random_round_payoff_1).wage:
                            print("In the interval")
                            p.belief_in_interval_1 = 1
                            p.final_payoff = Constants.bonus_if_in_internal
                        else:
                            print("Out of interval")
                            p.belief_in_interval_1 = 0
                    else:
                        print("the type is principal", p.type)

                        agent = p.get_others_in_group()[0]
                        print("This is agent", agent)
                        belief_effort = getattr(p.in_round(self.random_round_payoff_1),
                                              'eleffort{}'.format(self.random_line_belief_payoff_1))
                        strategy_effort = getattr(agent.in_round(self.random_round_payoff_1),
                                                'steffort{}'.format(self.random_line_belief_payoff_1))
                        print("this is belief effort", belief_effort)
                        print("this is strategy effort", strategy_effort)
                        # make the interval
                        upper_bound_belief_effort = strategy_effort + 0.1
                        lower_bound_belief_effort = strategy_effort - 0.1
                        # check if in interval
                        if lower_bound_belief_effort <= belief_effort <= upper_bound_belief_effort:
                            p.belief_in_interval_1 = 1
                            p.final_payoff = Constants.bonus_if_in_internal
                        else:
                            p.belief_in_interval_1 = 0

            else:
                print("Strategy method is going on")
                #strategy method
                for p in self.get_players():
                    if p.type == "agent":
                        strategy_effort = getattr(p.in_round(self.random_round_payoff_1),
                                          'steffort{}'.format(self.in_round(self.random_round_payoff_1).wage))
                for p in self.get_players():
                    if p.type == "agent":
                        print("this is the wage chosen for the strategy method", self.in_round(self.random_round_payoff_1).wage)
                        print("this is the effort chosen for the strategy method", strategy_effort)
                        print("something",self.in_round(self.random_round_payoff_1).actuale)
                        p.final_payoff = self.in_round(self.random_round_payoff_1).wage - ((strategy_effort) ** 2) / 2
                    else:
                        p.final_payoff = (self.in_round(self.random_round_payoff_1).actuale - self.in_round(self.random_round_payoff_1).wage) * strategy_effort
        else:
            print("Direct response method is going on")
            # direct-repsponse method
            for p in self.get_players():
                print("the type of the player", p.type)
                print("The information that we want", self.in_round(self.random_round_payoff_1).wage)

                if p.type == "agent":
                    p.final_payoff = self.in_round(self.random_round_payoff_1).wage - ((self.in_round(self.random_round_payoff_1).effort) ** 2) / 2
                else:
                    p.final_payoff = (self.in_round(self.random_round_payoff_1).actuale - self.in_round(self.random_round_payoff_1).wage) * self.in_round(self.random_round_payoff_1).effort

    def calculate_payoff_final_2(self): #compute payoffs in the final round 2
        print("***************** I'm in the method calculate payoff final 2 *****************")
        #if randomly choose round is in list then randomly choose a payoff method
        if self.random_round_payoff_2 in Constants.round_specials:
            self.paidinPoint1or2_draw2 = 1
            self.random_method_payoff_2 = 0 #np.random.choice(
                #[0, 1], 1,
                #p=[0.5, 0.5]
            #)[0]
            print("This is the method chosen (BELIEF vs STRATEGY):", self.random_method_payoff_2)
            if self.random_method_payoff_2 == 1:
                #Belief eliciation method
                self.random_line_belief_payoff_2 = random.randint(1,self.in_round(self.random_round_payoff_2).actuale)
                print("this is the second random line",self.random_line_belief_payoff_2)
                #now go find the choices of the players in that particular round
                for p in self.get_players():
                    if p.type == "agent":
                        #principal = self.get_others_in_group()[0]
                        #make the interval
                        upper_bound_belief_wage = self.in_round(self.random_round_payoff_2).wage + 1
                        lower_bound_belief_wage = self.in_round(self.random_round_payoff_2).wage - 1
                        print("this is upper belief wage",upper_bound_belief_effort)
                        print("this is lower belief wage",lower_bound_belief_effort)
                        print("this is belief wage",p.in_round(self.random_round_payoff_2).wagebelief)
                        # check if in interval
                        if lower_bound_belief_wage <= p.in_round(self.random_round_payoff_2).wagebelief <= upper_bound_belief_wage:
                            print("In the interval")
                            p.belief_in_interval_2 = 1
                            p.final_payoff += Constants.bonus_if_in_internal
                        else:
                            print("Out of interval")
                            p.belief_in_interval_2 = 0
                    else:
                        print("the type is principal", p.type)

                        print(p.get_others_in_group()[0])
                        agent = p.get_others_in_group()[0]
                        belief_effort = getattr(p.in_round(self.random_round_payoff_2),
                                              'eleffort{}'.format(self.random_line_belief_payoff_2))
                        strategy_effort = getattr(agent.in_round(self.random_round_payoff_2),
                                                'steffort{}'.format(self.random_line_belief_payoff_2))
                        print("this is belief effort", belief_effort)
                        print("this is strategy effort", strategy_effort)
                        # make the interval
                        upper_bound_belief_effort = strategy_effort + 0.1
                        lower_bound_belief_effort = strategy_effort - 0.1
                        # check if in interval
                        if lower_bound_belief_effort <= belief_effort <= upper_bound_belief_effort:
                            p.belief_in_interval_2 = 1
                            p.final_payoff += Constants.bonus_if_in_internal
                        else:
                            p.belief_in_interval_2 = 0

            else:
                print("Strategy method is going on")
                #strategy method
                for p in self.get_players():
                    if p.type == "agent":
                        print("take the agent")
                        strategy_effort = getattr(p.in_round(self.random_round_payoff_2),
                                                  'steffort{}'.format(self.in_round(self.random_round_payoff_2).wage))
                        print("this is the wage chosen for the strategy method", self.in_round(self.random_round_payoff_2).wage)
                        print("this is the effort chosen for the strategy method", strategy_effort)
                        print("something",self.in_round(self.random_round_payoff_2).actuale)
                        p.final_payoff += self.in_round(self.random_round_payoff_2).wage - ((strategy_effort) ** 2) / 2
                    else:
                        p.final_payoff += (self.in_round(self.random_round_payoff_2).actuale - self.in_round(self.random_round_payoff_2).wage) * strategy_effort
        else:
            print("Direct response method is going on")
            # direct-repsponse method
            for p in self.get_players():
                print("the type of the player", p.type)
                print("The information that we want", self.in_round(self.random_round_payoff_2).wage)

                if p.type == "agent":
                    p.final_payoff += self.in_round(self.random_round_payoff_2).wage - ((self.in_round(self.random_round_payoff_2).effort) ** 2) / 2
                else:
                    p.final_payoff += (self.in_round(self.random_round_payoff_2).actuale - self.in_round(self.random_round_payoff_2).wage) * self.in_round(self.random_round_payoff_2).effort


    def calculate_payoff(self): #payoffs as the game unravels - not paid
        players= self.get_players()
        if self.round_number >= 10 and self.in_round(10).draw == 1:
            high=1
        else:
            high=0
        for p in players:
            if p.type== 'agent':
                if self.round_number==1 or self.round_number==5 or self.round_number==10 or self.round_number==11 or self.round_number==15:
                    p.payoff = self.wage - ((self.steffort) ** 2) / 2
                else:
                    p.payoff = self.wage - ((self.effort) ** 2) / 2

            else:

                if self.round_number <= 10:
                    #if self.round_number != 1 and self.round_number !=5 and self.round_number != 10 and self.round_number != 11 and self.round_number != 15:
                    #    p.payoff = (Constants.Endowment - self.wage)*self.effort
                    if self.round_number == 1 or self.round_number ==5:
                        p.payoff = (Constants.Endowment - self.wage) * self.steffort
                        print("This is ACTUALE and the round is 1 or 5", self.actuale)
                    elif self.round_number == 10:
                        p.payoff = (Constants.Endowment - self.wage) * self.steffort
                        print("This is ACTUALE and the round is 10", self.actuale)
                        if high==1:
                            for g in self.in_rounds(self.round_number+1, Constants.num_rounds):
                                g.actuale = Constants.Endowmenthigh
                        else:
                            for g in self.in_rounds(self.round_number+1, Constants.num_rounds):
                                g.actuale = Constants.Endowmentlow
                    else:
                        p.payoff = (Constants.Endowment - self.wage) * self.effort
                else:

                    if (self.round_number == 11 or self.round_number == 15):
                        p.payoff = (self.actuale - self.wage) * self.steffort
                    else :
                        p.payoff = (self.actuale - self.wage) * self.effort
    def rounding(self):
        players= self.get_players()
        for p in players:
            p.final_payoff=round(p.final_payoff,1)

    def check_payoff(self):
        players= self.get_players()
        for p in players:
            if p.payoff < 0:
                p.payoff=0


class Player(BasePlayer):
    type = models.CharField()
    belief_in_interval_1 = models.IntegerField()
    belief_in_interval_2 = models.IntegerField()

    #FIRM: elicited effort
    eleffort1 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort2 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort3 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort4 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort5 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort6 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort7 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort8 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort9 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort10 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort11 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")
    eleffort12 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}),verbose_name="")

    #WORKER: strategy method effort
    steffort1 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort2 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort3 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort4 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort5 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort6 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort7 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort8 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort9 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort10 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort11 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")
    steffort12 = models.FloatField(min=0, max=4, widget=widgets.SliderInput(attrs={'step': '0.1'}), verbose_name="")

    #WORKER: elicited wage
    wagebelief = models.IntegerField(min=1, verbose_name='')

    #Payment at the end of the experiment
    final_payoff = models.FloatField()
