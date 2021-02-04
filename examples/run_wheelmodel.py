from wheel import WheelModel
from results import run_main_experiments
from tools import read_arg, run_arg

if __name__ == '__main__':

    only_nids = read_arg(["--only-nids"])
    nb_kcs = read_arg(["-k", "--nb-kc", "--nb-kcs"], vtype=int, default=10)
    kc1 = read_arg(["-k1", "--nb-kc1", "--odour1"], vtype=int, default=nb_kcs // 2)
    kc2 = read_arg(["-k2", "--nb-kc2", "--odour2"], vtype=int, default=nb_kcs // 2)

    model = WheelModel(
        learning_rule="dlr", nb_apl=0, pn2kc_init="default", verbose=False, timesteps=3, trials=24,
        nb_kc=nb_kcs, nb_kc_odour_1=kc1, nb_kc_odour_2=kc2, has_real_names=False,
        has_fom=True, has_bm=True, has_rsom=True, has_ltm=True, has_mdm=True)

    models = run_main_experiments(model, reversal=True, unpaired=True, no_shock=True)

    run_arg(model, models, only_nids)
