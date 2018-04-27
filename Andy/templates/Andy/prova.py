def calculate_payoff_final_2(self):  # compute payoffs in the final round 2
    print("***************** I'm in the method calculate payoff final 2 *****************")
    # if randomly choose round is in list then randomly choose a payoff method
    if self.random_round_payoff_2 in Constants.round_specials:
        self.paidinPoint1or2_draw2 = 1
        self.random_method_payoff_2 = np.random.choice(
            [0, 1], 1,
            p=[0.5, 0.5]
        )[0]
        print("This is the method chosen (BELIEF vs STRATEGY):", self.random_method_payoff_2)
        if self.random_method_payoff_2 == 1:
            # Belief eliciation method
            self.random_line_belief_payoff_2 = random.randint(1, self.in_round(self.random_round_payoff_2).actuale)
            print("this is the second random line", self.random_line_belief_payoff_2)
            # now go find the choices of the players in that particular round
            for p in self.get_players():
                if p.type == "agent":
                    # principal = self.get_others_in_group()[0]
                    # make the interval
                    upper_bound_belief_wage = self.in_round(self.random_round_payoff_2).wage + 1
                    lower_bound_belief_wage = self.in_round(self.random_round_payoff_2).wage - 1
                    print("this is upper belief wage", upper_bound_belief_effort)
                    print("this is lower belief wage", lower_bound_belief_effort)
                    print("this is belief wage", p.in_round(self.random_round_payoff_2).wagebelief)
                    # check if in interval
                    if lower_bound_belief_wage <= p.in_round(
                            self.random_round_payoff_2).wagebelief <= upper_bound_belief_wage:
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
            # strategy method
            for p in self.get_players():
                if p.type == "agent":
                    print("take the agent")
                    strategy_effort = getattr(p.in_round(self.random_round_payoff_2),
                                              'steffort{}'.format(self.in_round(self.random_round_payoff_2).wage))
                    print("this is the wage chosen for the strategy method",
                          self.in_round(self.random_round_payoff_2).wage)
                    print("this is the effort chosen for the strategy method", strategy_effort)
                    print("something", self.in_round(self.random_round_payoff_2).actuale)
                    p.final_payoff += self.in_round(self.random_round_payoff_2).wage - ((strategy_effort) ** 2) / 2
                else:
                    p.final_payoff += (self.in_round(self.random_round_payoff_2).actuale - self.in_round(
                        self.random_round_payoff_2).wage) * strategy_effort
    else:
        print("Direct response method is going on")
        # direct-repsponse method
        for p in self.get_players():
            print("the type of the player", p.type)
            print("The information that we want", self.in_round(self.random_round_payoff_2).wage)

            if p.type == "agent":
                p.final_payoff += self.in_round(self.random_round_payoff_2).wage - ((self.in_round(
                    self.random_round_payoff_2).effort) ** 2) / 2
            else:
                p.final_payoff += (self.in_round(self.random_round_payoff_2).actuale - self.in_round(
                    self.random_round_payoff_2).wage) * self.in_round(self.random_round_payoff_2).effort