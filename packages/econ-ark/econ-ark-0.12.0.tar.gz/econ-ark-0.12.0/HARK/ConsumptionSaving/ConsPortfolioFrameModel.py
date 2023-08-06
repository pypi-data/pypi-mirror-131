"""
This file contains classes and functions for representing,
solving, and simulating agents who must allocate their resources
among consumption, saving in a risk-free asset (with a low return),
and saving in a risky asset (with higher average return).

This file also demonstrates a "frame" model architecture.
"""
import numpy as np
from scipy.optimize import minimize_scalar
from copy import deepcopy
from HARK.frame import Frame, FrameAgentType
from HARK.ConsumptionSaving.ConsPortfolioModel import (
    init_portfolio,
    PortfolioConsumerType,
)

from HARK.distribution import combine_indep_dstns, add_discrete_outcome_constant_mean
from HARK.distribution import (
    IndexDistribution,
    Lognormal,
    MeanOneLogNormal,
    Bernoulli  # Random draws for simulating agents
)
from HARK.utilities import (
    CRRAutility,
)

class PortfolioConsumerFrameType(FrameAgentType, PortfolioConsumerType):
    """
    A consumer type with a portfolio choice, using Frame architecture.

    A subclass of PortfolioConsumerType for now.
    This is mainly to keep the _solver_ logic intact.
    """

    def __init__(self, **kwds):
        params = init_portfolio.copy()
        params.update(kwds)
        kwds = params

        # Initialize a basic consumer type
        PortfolioConsumerType.__init__(
            self, **kwds
        )
        # Initialize a basic consumer type
        FrameAgentType.__init__(
            self, **kwds
        )

        self.shocks = {}
        self.controls = {}
        self.state_now = {}

    # TODO: streamline this so it can draw the parameters from context
    def birth_aNrmNow(self, N):
        """
        Birth value for aNrmNow
        """
        return Lognormal(
            mu=self.aNrmInitMean,
            sigma=self.aNrmInitStd,
            seed=self.RNG.randint(0, 2 ** 31 - 1),
        ).draw(N)

    # TODO: streamline this so it can draw the parameters from context
    def birth_pLvlNow(self, N):
        """
        Birth value for pLvlNow
        """
        pLvlInitMeanNow = self.pLvlInitMean + np.log(
            self.state_now["PlvlAgg"]
        )  # Account for newer cohorts having higher permanent income

        return Lognormal(
            pLvlInitMeanNow,
            self.pLvlInitStd,
            seed=self.RNG.randint(0, 2 ** 31 - 1)
        ).draw(N)

    def transition_Rport(self, **context):

        Rport = (
            context["Share"] * context["Risky"]
            + (1.0 - context["Share"]) * self.parameters['Rfree']
        )
        return Rport, 

    def transition_pLvl(self, **context):
        pLvlPrev = context['pLvl']
        
        # Calculate new states: normalized market resources and permanent income level
        pLvlNow = pLvlPrev * context['PermShk']  # Updated permanent income level

        return pLvlNow

    def transition_bNrm(self, **context):
        aNrmPrev = context['aNrm']

        # This should be computed separately in its own transition
        # Using IndShock get_Rfree instead of generic.
        RfreeNow = context['Rport']

        # "Effective" interest factor on normalized assets
        ReffNow = RfreeNow / context['PermShk']
        bNrmNow = ReffNow * aNrmPrev         # Bank balances before labor income

        return bNrmNow

    def transition_mNrm(self, **context):
        mNrm = context['bNrm'] + context['TranShk']  # Market resources after income

        return mNrm

    def transition_ShareNow(self, **context):
        """
        Transition method for ShareNow.
        """
        ## Changed from HARK. See #1049. Should be added to context.
        ShareNow = self.controls['Share'].copy()

        # Loop over each period of the cycle, getting controls separately depending on "age"
        for t in range(self.T_cycle):
            these = t == self.t_cycle

            # Get controls for agents who *can* adjust their portfolio share
            those = np.logical_and(these, context['Adjust'])

            ShareNow[those] = self.solution[t].ShareFuncAdj(context['mNrm'][those])

            # Get Controls for agents who *can't* adjust their portfolio share
            those = np.logical_and(
                these,
                np.logical_not(context['Adjust']))
            ShareNow[those] = self.solution[t].ShareFuncFxd(
                context['mNrm'][those], ShareNow[those]
            )

        return ShareNow,

    def transition_cNrmNow(self, **context):
        """
        Transition method for cNrmNow.
        """
        cNrmNow = np.zeros(self.AgentCount) + np.nan
        ShareNow = context["Share"]

        # Loop over each period of the cycle, getting controls separately depending on "age"
        for t in range(self.T_cycle):
            these = t == self.t_cycle

            # Get controls for agents who *can* adjust their portfolio share
            those = np.logical_and(these, context['Adjust'])
            cNrmNow[those] = self.solution[t].cFuncAdj(context['mNrm'][those])

            # Get Controls for agents who *can't* adjust their portfolio share
            those = np.logical_and(
                these,
                np.logical_not(context['Adjust']))
            cNrmNow[those] = self.solution[t].cFuncFxd(
                context['mNrm'][those], ShareNow[those]
            )
        
        return cNrmNow,

    def transition_poststates(self, **context):
        """
        Calculates end-of-period assets for each consumer of this type.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # should this be "Now", or "Prev"?!?
        # todo: don't store on self
        self.state_now['aNrm'] = context['mNrm'] - context['cNrm']
        # Useful in some cases to precalculate asset level
        self.state_now['aLvl'] = context['aNrm'] * context['pLvl']

        return (self.state_now['aNrm'], self.state_now['aLvl'])

    # maybe replace reference to init_portfolio to self.parameters?
    frames = [
        # todo : make an aggegrate value
        Frame(('PermShkAgg',), ('PermGroFacAgg',),
            transition = lambda self, PermGroFacAgg : (PermGroFacAgg,),
            aggregate = True
        ),
        Frame(
            ('PermShk'), None,
            default = {'PermShk' : 1.0}, # maybe this is unnecessary because the shock gets sampled at t = 0
            # this is discretized before it's sampled
            transition = IndexDistribution(
                    Lognormal.from_mean_std,
                    {
                        'mean' : init_portfolio['PermGroFac'],
                        'std' : init_portfolio['PermShkStd']
                    }
                ).approx(
                    init_portfolio['PermShkCount'], tail_N=0
                ),
        ),
        Frame(
            ('TranShk'), None,
            default = {'TranShk' : 1.0}, # maybe this is unnecessary because the shock gets sampled at t = 0
            transition = add_discrete_outcome_constant_mean(
                IndexDistribution(
                    MeanOneLogNormal,
                    {
                        'sigma' : init_portfolio['TranShkStd']
                    }).approx(
                        init_portfolio['TranShkCount'], tail_N=0
                    ),
                    p = init_portfolio['UnempPrb'], x = init_portfolio['IncUnemp'] 
            )
        ),
        Frame( ## TODO: Handle Risky as an Aggregate value
            ('Risky'),None, 
            transition = IndexDistribution(
                Lognormal.from_mean_std,
                {
                    'mean' : init_portfolio['RiskyAvg'],
                    'std' : init_portfolio['RiskyStd']
                }
                # seed=self.RNG.randint(0, 2 ** 31 - 1) : TODO: Seed logic
            ).approx(
                init_portfolio['RiskyCount']
            ),
            aggregate = True
        ),
        Frame(
            ('Adjust'),None, 
            default = {'Adjust' : False},
            transition = IndexDistribution(
                Bernoulli,
                {'p' : init_portfolio['AdjustPrb']},
                # seed=self.RNG.randint(0, 2 ** 31 - 1) : TODO: Seed logic
            ) # self.t_cycle input implied
        ),
        Frame(
            ('Rport'), ('Share', 'Risky'), 
            transition = transition_Rport
        ),
        Frame(
            ('PlvlAgg'), ('PlvlAgg', 'PermShkAgg'), 
            default = {'PlvlAgg' : 1.0},
            transition = lambda self, PlvlAgg, PermShkAgg : PlvlAgg * PermShkAgg,
            aggregate = True
        ),
        Frame(
            ('pLvl',),
            ('pLvl', 'PermShk'),
            default = {'pLvl' : birth_pLvlNow},
            transition = transition_pLvl
        ),
        Frame(
            ('bNrm',),
            ('aNrm', 'Rport', 'PermShk'),
            default = {'pLvl' : birth_pLvlNow},
            transition = transition_bNrm
        ),
        Frame(
            ('mNrm',),
            ('bNrm', 'TranShk'),
            transition = transition_mNrm
        ),
        Frame(
            ('Share'), ('Adjust', 'mNrm'),
            default = {'Share' : 0}, 
            transition = transition_ShareNow,
            control = True
        ),
        Frame(
            ('cNrm'), ('Adjust','mNrm','Share'), 
            transition = transition_cNrmNow,
            control = True
        ),
        Frame(
            ('U'), ('cNrm','CRRA'), ## Note CRRA here is a parameter not a state var
            transition = lambda self, cNrm, CRRA : (CRRAutility(cNrm, CRRA),),
            reward = True
        ),
        Frame(
            ('aNrm'), ('mNrm', 'cNrm'),
            default = {'aNrm' : birth_aNrmNow},
            transition = lambda self, mNrm, cNrm : (mNrm - cNrm,)
        ),
        Frame(
            ('aLvl'), ('aNrm', 'pLvl'),
            transition = lambda self, aNrm, pLvl : (aNrm * pLvl,)
        )
    ]
