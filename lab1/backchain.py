from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    hows = []
    for rule in rules:
        if isinstance(rule.consequent(), basestring):
            cons = [rule.consequent()]
        else:
            cons = rule.consequent()
        for c in rule.consequent():
            m = match(c, hypothesis)
            if m is not None:
                instantiated_candidate = populate(c, m)
                hows.append(instantiated_candidate)

                antecedents_hows = []
                if isinstance(rule.antecedent(), basestring):
                    ants = [rule.antecedent()]
                else:
                    ants = rule.antecedent()
                for ant in ants:
                    p_ant = populate(ant, m) 
                    ant_hows = backchain_to_goal_tree(rules, p_ant)
                    antecedents_hows.append(ant_hows)
                
                if isinstance(rule.antecedent(), basestring) or isinstance(rule.antecedent(), OR) :
                    for ant_hows in antecedents_hows:
                        hows.append(ant_hows)
                elif isinstance(rule.antecedent(), AND):
                    hows.append(AND(*antecedents_hows))
                else:
                    raise ValueError, "something is wront with this antecedent: %s" % rule.antecedent()

    if not hows:
        return hypothesis
    else:
        return simplify(OR(hows))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
