__author__ = "Evripidis Gkanias"
__copyright__ = "Copyright 2021, School of Informatics, the University of Edinburgh"
__licence__ = "MIT"
__version__ = "1.1-alpha"
__maintainer__ = "Evripidis Gkanias"
__email__ = "ev.gkanias@ed.ac.uk"
__status__ = "Production"

import sys

import numpy as np
import matplotlib.pyplot as plt


def main(*args):

    gamma_k = .97
    gamma_d1 = .98
    gamma_d2 = .99

    plasticity = []
    uss_on = [-6., -1.2, -.6, 0., .5, 6.]

    for i, us_on in enumerate(uss_on):
        W = 1.
        time, css, uss, k, d1, d2, m, w = [], [], [], [], [], [], [], []
        for t, cs, us in handler_routine(us_on=us_on):
            time.append(t)
            css.append(cs)
            uss.append(us)
            if len(k) > 0:
                K = (1 - gamma_k) * cs + gamma_k * k[-1]
            else:
                K = cs
            k.append(np.clip(K, 0, 2))
            m.append(np.clip(k[-1] * np.maximum(W, 0), 0, 2))
            if len(d1) > 0 and len(d2) > 0:
                D1 = (1 - gamma_d1) * (us - 1. * m[-2]) + gamma_d1 * d1[-1]
                D2 = (1 - gamma_d2) * (us - 1. * m[-2]) + gamma_d2 * d2[-1]
            else:
                D1 = us
                D2 = us
            d1.append(np.clip(D1, 0, 2))
            d2.append(np.clip(D2, 0, 2))
            W += dopaminergic_plasticity_rule(k[-1], d1[-1], d2[-1], W, w_rest=1.)
            w.append(np.maximum(W, 0))

        plt.figure('learning-rule', figsize=(7, 5))

        plt.subplot(6, 6, i + 1)
        plt.title('%.1f s' % us_on, fontsize=8)
        plt.plot([0, 0], [-.05, 1.1], 'k:')
        plt.plot([0], [-.05], 'k', marker=6)
        plt.plot([us_on, us_on], [-.05, 1.1], 'r:')
        plt.plot([us_on], [-.05], 'r', marker=6)
        plt.plot(time, css, 'k')
        if i == 0:
            plt.text(-4, .5, 'CS', fontsize=8, rotation=0)
        plt.ylim(-.1, 1.1)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(6, 6, i + 7)
        plt.plot([0, 0], [-.05, 1.1], 'k:')
        plt.plot([0], [-.05], 'k', marker=6)
        plt.plot([us_on, us_on], [-.05, 1.1], 'r:')
        plt.plot([us_on], [-.05], 'r', marker=6)
        plt.plot(time, uss, 'r')
        if i == 0:
            plt.text(-4, .5, 'US', fontsize=8, rotation=0)
        plt.ylim(-.1, 1.1)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(6, 6, i + 13)
        plt.plot([0, 0], [-.05, 1.1], 'k:')
        plt.plot([0], [-.05], 'k', marker=6)
        plt.plot([us_on, us_on], [-.05, 1.1], 'r:')
        plt.plot([us_on], [-.05], 'r', marker=6)
        plt.plot(time, k, 'k')
        if i == 0:
            plt.text(-4, .5, 'KC', fontsize=8, rotation=0)
        plt.ylim(-.1, 1.1)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(6, 6, i + 19)
        plt.plot([0, 0], [-.35, .8], 'k:')
        plt.plot([0], [-.35], 'k', marker=6)
        plt.plot([us_on, us_on], [-.35, .8], 'r:')
        plt.plot([us_on], [-.35], 'r', marker=6)
        plt.plot(time, d1, 'm', label='D1')
        plt.plot(time, d2, 'orange', label='D2')
        plt.plot(time, np.array(d2) - np.array(d1), 'grey', alpha=.5, label='D2-D1')
        if i == 0:
            plt.text(-4, .8, 'dopamine', fontsize=8, rotation=0)
        plt.ylim(-.4, .8)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(6, 6, i + 25)
        plt.plot([0, 0], [-.1, 2.2], 'k:')
        plt.plot([0], [-.1], 'k', marker=6)
        plt.plot([us_on, us_on], [-.1, 2.2], 'r:')
        plt.plot([us_on], [-.1], 'r', marker=6)
        plt.plot(time, m, 'b')
        if i == 0:
            plt.text(-4, 1.5, 'MBON', fontsize=8, rotation=0)
        plt.ylim(-.2, 2.2)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(6, 6, i + 31)
        plt.plot([0, 0], [-.1, 2.2], 'k:')
        plt.plot([0], [-.1], 'k', marker=6)
        plt.plot([us_on, us_on], [-.1, 2.2], 'r:')
        plt.plot([us_on], [-.1], 'r', marker=6)
        plt.plot(time, w, 'g')
        if i == 0:
            plt.text(-4, 1.5, r'$W_{k2m}$', fontsize=8, rotation=0)
        plt.ylim(-.2, 2.2)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.tight_layout()

        plt.figure("dopamine-function", figsize=(7, 3))

        # dR1 = -(np.array(d2) - np.array(d1)) * np.array(k)
        # dR2 = -(np.array(d2) - np.array(d1)) * (np.array(w) - 1)
        dR1 = (np.maximum(np.array(d1) - np.array(d2), 0) * (np.array(k) - 1) +
               (np.array(d1) - np.array(d2)) * np.array(w))
        dR2 = np.minimum(np.array(d1) - np.array(d2), 0) * (np.array(k) - 1)
        # dR1 = -np.array(d1) - np.array(d2) * (np.array(k) + np.array(w))
        # dR2 = np.array(d1) * (np.array(k) + np.array(w)) + np.array(d2) * 1.

        plt.subplot(3, 6, i + 1)
        plt.title('%.1f s' % us_on, fontsize=8)
        plt.plot([0, 0], [-.09, .1], 'k:')
        plt.plot([0], [-.09], 'k', marker=6)
        plt.plot([us_on, us_on], [-.09, .1], 'r:')
        plt.plot([us_on], [-.09], 'r', marker=6)
        plt.plot(time, dR1, 'k')
        if i == 0:
            plt.text(-4, .05, 'ER-GCaMP\nDopR1', fontsize=8, rotation=0)
        plt.ylim(-.1, .1)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(3, 6, i + 7)
        plt.plot([0, 0], [-.09, .1], 'k:')
        plt.plot([0], [-.09], 'k', marker=6)
        plt.plot([us_on, us_on], [-.09, .1], 'r:')
        plt.plot([us_on], [-.09], 'r', marker=6)
        plt.plot(time, dR2, 'k')
        if i == 0:
            plt.text(-4, .05, 'cAMP\nDopR2', fontsize=8, rotation=0)
        plt.ylim(-.1, .1)
        plt.xlim(-7, 8)
        plt.axis('off')

        plt.subplot(3, 6, i + 13)
        plt.plot([0, 0], [-.09, .1], 'k:')
        plt.plot([0], [-.09], 'k', marker=6)
        plt.plot([us_on, us_on], [-.09, .1], 'r:')
        plt.plot([us_on], [-.09], 'r', marker=6)
        plt.plot(time, -dR1 - dR2, 'k')
        if i == 0:
            plt.text(-4, .05, 'effect', fontsize=8, rotation=0)
        plt.ylim(-.1, .1)
        plt.xlim(-7, 8)
        plt.axis('off')
        plt.tight_layout()

        plasticity.append(np.mean(-dR1 - dR2))

    plasticity = np.array(plasticity)
    plasticity[plasticity > 0] = plasticity[plasticity > 0] / plasticity.max() * .8
    plasticity[plasticity < 0] = -plasticity[plasticity < 0] / plasticity.min() * .8

    plt.figure('plasticity', figsize=(2, 3))
    plt.plot([-3, -1.2, -.6, 0, .5, 3], plasticity, 'k+-')
    plt.xticks([-3, -2, -1, 0, 1, 2, 3], [-6, -2, -1, 0, 1, 2, 6])
    plt.yticks([-1, 0, 1])
    plt.ylim(-1, 1)

    plt.show()


def handler_routine(us_on=0., us_duration=.6, cs_on=0., cs_duration=.5, nb_samples=1001):
    time_range = [-7, 8]

    for t in np.linspace(time_range[0], time_range[1], nb_samples, endpoint=True):
        cs, us = 0., 0.
        if cs_on <= t < cs_on+cs_duration:
            cs = 1.
        if us_on <= t < us_on+us_duration:
            us = 1.
        yield t, cs, us


# dw/dt = D (k + w - w_rest)
# dw/dt = D_1 k + D_2 (k + w - w_rest)
# D_1 = D^-  (short trace)
# D_2 = D^+  (longer trace)
def dopaminergic_plasticity_rule(k, D_1, D_2, w, w_rest):
    return (D_2 - D_1) * (k + w - w_rest)


if __name__ == '__main__':
    main(*sys.argv)
