from typing import List
import numpy as np


def reversal_routine(mb_model):
    """
    The reversal experimental paradigm as a routine. It allows alternately CS (odour) delivery and paired US (shock)
    delivery during trials 3, 5, 7, 9, 11, 14, 16, 18, 20, 22 and 24.

    :param mb_model: the mushroom body model to get and update the parameters.
    :return: a generator of stimuli based on the reversal experimental paradigm that returns tuples of the form (#trial,
    #in-trial-time-step, CS, US)
    """
    cs_on = np.arange(mb_model.nb_trials * 2)
    us_on = np.array([3, 5, 7, 9, 11, 14, 16, 18, 20, 22, 24])
    mb_model.routine_name = "reversal"
    return _routine_base(mb_model, odour=cs_on, shock=us_on)


def unpaired_routine(mb_model):
    """
    The unpaired experimental paradigm as a routine. It allows alternately CS (odour) delivery and unpaired US (shock)
    delivery during trials 3, 5, 7, 9, 11, 14, 16, 18, 20, 22 and 24.

    :param mb_model: the mushroom body model to get and update the parameters.
    :return: a generator of stimuli based on the unpaired experimental paradigm that returns tuples of the form (#trial,
    #in-trial-time-step, CS, US)
    """
    cs_on = np.arange(mb_model.nb_trials * 2)
    us_on = np.array([3, 5, 7, 9, 11, 14, 16, 18, 20, 22, 24])
    mb_model.routine_name = "unpaired"
    return _routine_base(mb_model, odour=cs_on, shock=us_on, paired=[3, 5, 7, 9, 11])


def no_shock_routine(mb_model):
    """
    The no-shock experimental paradigm as a routine. It allows alternately CS (odour) delivery and paired US (shock)
    delivery during trials 3, 5, 7, 9, 11.

    :param mb_model: the mushroom body model to get and update the parameters.
    :return: a generator of stimuli based on the no-shock experimental paradigm that returns tuples of the form (#trial,
    #in-trial-time-step, CS, US)
    """
    cs_on = np.arange(mb_model.nb_trials * 2)
    us_on = np.array([3, 5, 7, 9, 11])
    mb_model.routine_name = "no shock"
    return _routine_base(mb_model, odour=cs_on, shock=us_on)


def shock_routine(mb_model, timesteps=100):
    """
    The example used to explain the behaviour of the sub-circuits as a routine. It is composed by a single trial with
    100 time-steps (default). It is split into 5 phases:
    1. t =   0 - t_1 : no CS (odour) and no US (shock) is delivered,
    2. t = t_1 - t_2 : only CS is delivered,
    3. t = t_2 - t_3 : CS and US are delivered simultaneously,
    4. t = t_3 - t_4 : only CS is delivered, and
    5. t = t_4 - end : no CS and no US is delivered;
    where t_1 = 10%, t_2 = 30%, t_3 = 60% and t_4 = 80% of the duration of the experiment.

    :param mb_model: the mushroom body model to get and update the parameters.
    :param timesteps: (optional) the number of time-steps that show the duration of the experiment. Default is 100.
    :return: a generator of stimuli based on the punishing reinforcement example of the manuscript that returns tuples
    of the form (#trial=1, #in-trial-time-step, CS, US)
    """
    mb_model._t = 0
    mb_model.nb_trials = 1
    mb_model.nb_timesteps = timesteps
    mb_model.w_k2m = np.array([mb_model.w_k2m[0]] * (timesteps + 1))
    mb_model._v = np.array([mb_model._v[0]] * (timesteps + 1))
    mb_model._v_apl = np.array([mb_model._v_apl[0]] * (timesteps + 1))
    for timestep in range(timesteps):
        cs_ = mb_model.csa
        us_ = np.zeros(mb_model.us_dims, dtype=float)
        if mb_model.us_dims > 2:
            us_[4] = 2.
        else:
            us_[1] = 2.

        if timestep < .1 * timesteps:
            cs = cs_ * 0.
            us = us_ * 0.
        elif timestep < .3 * timesteps:
            cs = cs_ * 1.
            us = us_ * 0.
        elif timestep < .6 * timesteps:
            cs = cs_ * 1.
            us = us_ * 1.
        elif timestep < .8 * timesteps:
            cs = cs_ * 1.
            us = us_ * 0.
        else:
            cs = cs_ * 0.
            us = us_ * 0.

        yield 1, timestep, cs, us

        mb_model._t += 1


def rewarding_routine(mb_model, timesteps=100):
    """
    The example used to explain the behaviour of the sub-circuits as a routine. It is composed by a single trial with
    100 time-steps (default). It is split into 5 phases:
    1. t =   0 - t_1 : no CS (odour) and no US (reward) is delivered,
    2. t = t_1 - t_2 : only CS is delivered,
    3. t = t_2 - t_3 : CS and US are delivered simultaneously,
    4. t = t_3 - t_4 : only CS is delivered, and
    5. t = t_4 - end : no CS and no US is delivered;
    where t_1 = 10%, t_2 = 30%, t_3 = 60% and t_4 = 80% of the duration of the experiment.

    :param mb_model: the mushroom body model to get and update the parameters.
    :param timesteps: (optional) the number of time-steps that show the duration of the experiment. Default is 100.
    :return: a generator of stimuli based on the rewarding reinforcement example of the manuscript that returns tuples
    of the form (#trial=1, #in-trial-time-step, CS, US)
    """
    mb_model._t = 0
    mb_model.nb_trials = 1
    mb_model.nb_timesteps = timesteps
    mb_model.w_k2m = np.array([mb_model.w_k2m[0]] * (timesteps + 1))
    mb_model._v = np.array([mb_model._v[0]] * (timesteps + 1))
    mb_model._v_apl = np.array([mb_model._v_apl[0]] * (timesteps + 1))
    for timestep in range(timesteps):
        cs_ = mb_model.csa
        us_ = np.zeros(mb_model.us_dims, dtype=float)
        if mb_model.us_dims > 0:
            us_[0] = 2.

        if timestep < .1 * timesteps:
            cs = cs_ * 0.
            us = us_ * 0.
        elif timestep < .3 * timesteps:
            cs = cs_ * 1.
            us = us_ * 0.
        elif timestep < .6 * timesteps:
            cs = cs_ * 1.
            us = us_ * 1.
        elif timestep < .8 * timesteps:
            cs = cs_ * 1.
            us = us_ * 0.
        else:
            cs = cs_ * 0.
            us = us_ * 0.

        yield 1, timestep, cs, us

        mb_model._t += 1


def _routine_base(mb_model, odour=None, shock=None, paired=None):
    """
    Takes as input the model to be used and the trials where we want the odour and shock delivered, and generates the
    CS and US input to the model.

    :param mb_model: the mushroom body model to get and update the parameters.
    :param odour: (optional) a list of the trials to deliver the odours. Default is all.
    :type odour: List[int] | np.ndarray[int]
    :param shock: (optional) a list of the trials to deliver the shock. Default is all.
    :type shock: List[int] | np.ndarray[int]
    :param paired: (optional) a list of the trials to have the shock and odour delivery at the same time. Default is
    all.
    :type paired: List[int] | np.ndarra[int]
    :return: a generator that returns tuples of (#trial, #in-trial-time-step, CS, US) until the experiment is over
    """
    mb_model._t = 0
    if odour is None:
        odour = np.arange(mb_model.nb_trials * 2)
    if shock is None:
        shock = np.arange(mb_model.nb_trials * 2)
    if paired is None:
        paired = np.arange(mb_model.nb_trials * 2)

    for trial in range(1, mb_model.nb_trials // 2 + 2):
        for cs_ in [mb_model.csa, mb_model.csb]:
            if mb_model._t >= mb_model.nb_trials * mb_model.nb_timesteps:
                break

            trial_ = mb_model._t // mb_model.nb_timesteps

            # odour is presented only in specific trials
            cs__ = cs_ * float(trial_ in odour)

            # shock is presented only in specific trials
            us__ = np.zeros(mb_model.us_dims, dtype=float)
            if mb_model.us_dims > 2:
                us__[4] = float(trial_ in shock)
            else:
                us__[1] = float(trial_ in shock)

            for timestep in range(mb_model.nb_timesteps):

                # we skip odour in the first timestep of the trial
                cs = cs__ * float(timestep > 0)
                if trial_ in paired:
                    # shock is presented only after the 4th sec of the trial
                    us = us__ * float(4 <= 5 * (timestep + 1) / mb_model.nb_timesteps)
                else:
                    us = us__ * float(timestep < 1)

                yield trial, timestep, cs, us

                mb_model._t += 1