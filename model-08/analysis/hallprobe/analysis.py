#!/usr/bin/env python-sirius
"""Run analysis."""


import numpy as np
import matplotlib.pyplot as plt
from fieldmaptrack import hallprobe as hall
import mathphys as mp
import math


_fmap_files = None

c2e_B2 = {
    '381.7A': 2.852,
    '401.8A': 3.000,
    '421.9A': 3.148,
}

# media dos imas, apos procura com x0=8.165mm
c2e_B2 = {
    '381.7A': 2.8426315121951222,
    '401.8A': 2.990131219512195,
    '421.9A': 3.137303658536585,
}

# media dos imas, apos procura com x0=8.153mm
c2e_B2 = {
    '381.7A' : 2.84308943902439,
    '401.8A' : 2.990614,
    '421.9A' : 3.137824707317073,
}


def search_for_deflection_angle_B2():
    """."""
    init_energies = [2.852039/1.0032, 3.000021/1.0032, 3.147681/1.0032]  # IMA used values

    magnets = get_magnets_B2()
    currents = get_currents_B2()

    fstr = 'magnet:{}, current:{} => nr_iter:{:02d}, energy:{:8.6f} GeV'
    for i in range(len(currents)):
        curr = currents[i]
        for magnet in magnets:
            files = get_fmap_files_B2(magnet, curr)
            fa = hall.DoubleFMapAnalysis(magnet=magnet, fmap_fname=files[0])
            fa.traj_init_rx = 7.920 + 0.245
            fa.energy = init_energies[i]
            n = fa.search_energy(False)
            print(fstr.format(magnet, curr, n, fa.energy))


def load_search_deflection_angle_file(fname=None):
    """."""
    if fname is None:
        fname = 'search-energies.txt'
    with open(fname) as fp:
        text = fp.readlines()
    data = dict()
    for line in text:
        words = line.split(':')
        magnet = words[1].split(',')[0]
        current = words[2].split(' =>')[0]
        energy = float(words[4].split(' GeV')[0])
        if current not in data:
            data[current] = {magnet: energy}
        elif magnet not in data[current]:
            data[current][magnet] = energy
        else:
            raise ValueError()
    currents = tuple(data.keys())
    magnets = tuple(data[currents[0]].keys())
    energies = tuple(tuple(data[c][m] for m in magnets) for c in currents)
    return currents, magnets, energies


def load_search_reference_points_file():
    """."""
    with open('search-refpoint.txt') as fp:
        text = fp.readlines()
    data = dict()
    for line in text:
        words = line.split(':')
        magnet = words[1].split(',')[0]
        current = words[2].split(' =>')[0]
        energy = float(words[3].split(' GeV')[0])
        rx = float(words[4].split(' mm')[0])
        px = float(words[5].split(' deg')[0])
        if current not in data:
            data[current] = {magnet: (energy, rx, px)}
        elif magnet not in data[current]:
            data[current][magnet] = (energy, rx, px)
        else:
            raise ValueError()
    currs = tuple(data.keys())
    mags = tuple(data[currs[0]].keys())

    currents = tuple(c for m in mags for c in currs)
    energies = tuple(data[c][m][0] for m in mags for c in currs)
    rx = tuple(data[c][m][1] for m in mags for c in currs)
    px = tuple(data[c][m][2] for m in mags for c in currs)
    magnets = tuple(m for m in mags for c in currs)
    return currents, magnets, energies, rx, px

    # print(energies)
    # energies = tuple(tuple(data[c][m][0] for m in magnets) for c in currs)
    # rx = tuple(tuple(data[c][m][1] for m in magnets) for c in currs)
    # px = tuple(tuple(data[c][m][2] for m in magnets) for c in currs)
    # return currents, magnets, energies, rx, px


def load_search_reference_points_file_relaxed():
    """."""
    with open('search-refpoint-relaxed.txt') as fp:
        text = fp.readlines()
    # data = dict()
    for i in range(len(text)):
        if 'magnet' in text[i]:
            # text[i]
            line = text[i]
            words = line.split(' ')
            magnet = words[0].replace(',', '').split(':')[1]
            current = words[1].split(':')[1]
            energy = float(words[3].split(':')[1])
            x0 = float(words[6])
            px = float(words[8].split(':')[1])
            # text[i-1]
            line = text[i-1]
            # wordsdangp = line.split(' ')
            magnet = words[0].replace(',', '').split(':')[1]

            print(magnet, current, energy, x0, px)


def plot_results_search_deflection_angle_B2():
    """."""
    currents, magnets, energies = load_search_deflection_angle_file()
    fst = 'current:{}  energy_avg:{:8.6f} Gev  energy_std:{:5.3f} %'
    for i in range(len(energies)):
        em = np.mean(energies[i])
        es = np.std(energies[i])
        ev = 100*(energies[i] - em)/em
        plt.plot(ev, 'o', label=currents[i])
        print(fst.format(currents[i], em, 100*es/em))
    plt.plot([0, len(ev)-1], [+0.05, ]*2, '--k', label='spec')
    plt.plot([0, len(ev)-1], [-0.05, ]*2, '--k',)
    plt.xlabel('Magnet Index')
    plt.ylabel('Nominal deflection energy spread [%]')
    plt.grid()
    plt.legend()
    plt.show()


def seach_for_reference_point_B2():
    """."""
    def calc_residue_new(f):
        a1, b1 = f.calc_asymptotic_line_coeffs(f.traj)
        a2, b2 = f.calc_asymptotic_line_coeffs(f.configN.traj)
        a1 = f.calc_deflection_angle(f.traj)
        a2 = f.calc_deflection_angle(f.configN.traj)
        da1 = abs(a1) - abs(f.model_nominal_angle/2)
        da2 = abs(a2) - abs(f.model_nominal_angle/2)
        return np.array([da1, da2,
                         b1 - f.model_nominal_refrx,
                         b2 - f.model_nominal_refrx])

    def calc_residue_old(f):
        rp = np.array(f.reference_point) - \
            np.array((f.model_nominal_refrx, 0))
        da = abs(f.deflection_angle) - abs(f.model_nominal_angle)
        return np.array([da, rp[0], rp[1]])

    def search(f, p0, dp):
        """."""
        calc_residue = calc_residue_new
        sfmt = ('residue - dangP:{:+6.3f} %, dangN:{:+6.3f} %, '
                'drefrxP:{:+7.2f} um, drefrxN:{:+7.2f} um')
        p = np.array(p0)
        dp = np.array(dp)
        # res0
        f.traj_init_rx = p[0]
        f.traj_init_px = p[1]
        f.energy = p[2]
        f.analysis_trajectory()
        res0 = calc_residue(f)
        resn = res0 / np.array(
            [0.01*abs(f.model_nominal_angle/2),
             0.01*abs(f.model_nominal_angle/2),
             0.001, 0.001])
        print(sfmt.format(*resn))
        m = np.zeros((len(res0), 3))

        for i in range(4):

            # --- m[:,0]
            f.traj_init_rx = p[0] + dp[0]
            f.traj_init_px = p[1]
            f.energy = p[2]
            f.analysis_trajectory()
            r = calc_residue(f)
            m[:, 0] = (r - res0)/dp[0]

            # --- m[:,1]
            f.traj_init_rx = p[0]
            f.traj_init_px = p[1] + dp[1]
            f.energy = p[2]
            f.analysis_trajectory()
            r = calc_residue(f)
            m[:, 1] = (r - res0)/dp[1]

            # --- m[:,2]
            f.traj_init_rx = p[0]
            f.traj_init_px = p[1]
            f.energy = p[2] + dp[2]
            f.analysis_trajectory()
            r = calc_residue(f)
            m[:, 2] = (r - res0)/dp[2]

            # --- solve
            dr, *_ = np.linalg.lstsq(m, -res0, None)
            # dr = np.linalg.solve(m, -res0)
            p = p + dr
            dp *= 0.8

            # res0
            f.traj_init_rx = p[0]
            f.traj_init_px = p[1]
            f.energy = p[2]
            f.analysis_trajectory()
            res0 = calc_residue(f)
            resn = res0 / np.array(
                [0.01*abs(f.model_nominal_angle/2),
                 0.01*abs(f.model_nominal_angle/2),
                 0.001, 0.001])
            print(sfmt.format(*resn))

        return p, res0

    c2e_B2 = {
        '381.7A': 2.852039,
        '401.8A': 3.000021,
        '421.9A': 3.147681,
    }

    fstr = ('magnet:{}, current:{} => energy:{:8.6f} '
            'GeV, x0:{:6.3f} mm, px:{:+7.4f} deg')

    magnets = get_magnets_B2()
    currents = get_currents_B2()
    for magnet in magnets:
        for curr in currents:
            fname = get_fmap_files_B2(magnet, curr)[0]
            # print(fname)
            f = hall.DoubleFMapAnalysis(
                magnet=magnet, fmap_fname=fname)
            f.analysis_rawfield()
            p0 = [7.92, 0.0, c2e_B2[curr]]
            dp = [0.5, 0.3, 0.05]
            p, res0 = search(f, p0, dp)
            print(fstr.format(magnet, curr, p[2], p[0], p[1]))


def plot_results_search_reference_points_B2():
    """."""
    currents, magnets, energies, rx, px = load_search_reference_points_file()

    # energies x current

    # 381.7A: 2.850293 GeV  std: 0.026 %  minmax: [-0.050,+0.069] %
    # 401.8A: 2.998122 GeV  std: 0.023 %  minmax: [-0.036,+0.043] %
    # 421.9A: 3.145611 GeV  std: 0.028 %  minmax: [-0.044,+0.057] %

    data = dict()
    for i in range(len(currents)):
        if currents[i] in data:
            data[currents[i]].append(energies[i])
        else:
            data[currents[i]] = [energies[i], ]

    # print
    fstr = '{}: {:.6f} GeV  std: {:0.3f} %  minmax: [{:+0.3f},{:+0.3f}] %'
    print('Averages:')
    for cur in data:
        d = data[cur]
        avg = np.mean(d)
        std = np.std(d)
        de = 100*(d - avg)/avg
        print(fstr.format(cur, avg, 100*std/avg, min(de), max(de)))

    # plot
    for cur in data:
        d = data[cur]
        de = 100*(d - np.mean(d))/np.mean(d)
        plt.plot(de, 'o', label=cur)
    plt.legend()
    plt.grid()
    plt.xlabel('Magnet index')
    plt.ylabel('Energy deviation [%]')
    plt.show()

    # rx and px x magnet


def plot_results_search_reference_points_relaxed_B2():
    """."""
    d381p7A = np.array([
        [2.848880, 7.970, +0.0262],
        [2.849926, 7.964, -0.0063],
        [2.850784, 7.962, +0.0072],
        [2.849825, 7.963, -0.0155],
        [2.849165, 7.964, +0.0173],
        [2.849716, 7.967, +0.0053],
        [2.849981, 7.966, -0.0146],
        [2.852262, 7.960, -0.0265],
        [2.850515, 7.957, +0.0159],
        [2.851081, 7.955, -0.0107],
        [2.851349, 7.957, +0.0143],
        [2.849121, 7.964, -0.0032],
        [2.849671, 7.962, +0.0086],
        [2.850017, 7.961, +0.0324],
        [2.851427, 7.957, +0.0199],
        [2.850374, 7.961, -0.0207],
        [2.850050, 7.960, +0.0094],
        [2.849103, 7.966, -0.0305],
        [2.850035, 7.965, -0.0356],
        [2.849523, 7.966, -0.0071],
        [2.849699, 7.965, +0.0020],
        [2.850636, 7.964, +0.0051],
        [2.849966, 7.967, -0.0195],
        [2.850496, 7.965, +0.0035],
        [2.850935, 7.963, -0.0108],
        [2.851207, 7.963, -0.0068],
        [2.850787, 7.964, -0.0338],
        [2.849765, 7.967, +0.0317],
        [2.850790, 7.968, +0.0047],
        [2.850709, 7.967, -0.0079],
        [2.850909, 7.965, -0.0061],
        [2.849964, 7.968, +0.0083],
        [2.850044, 7.962, -0.0062],
        [2.849876, 7.966, +0.0019],
        [2.850034, 7.967, +0.0117],
        [2.849969, 7.963, -0.0229],
        [2.850028, 7.962, +0.0067],
        [2.849664, 7.963, -0.0019],
        [2.850995, 7.962, +0.0094],
        [2.851099, 7.963, +0.0194],
        [2.851654, 7.959, -0.0002]])

    avg = np.mean(d381p7A[:, 0])

    currents, magnets, energies, rx, px = load_search_reference_points_file()

    # energies x current

    # 381.7A: 2.850293 GeV  std: 0.026 %  minmax: [-0.050,+0.069] %
    # 401.8A: 2.998122 GeV  std: 0.023 %  minmax: [-0.036,+0.043] %
    # 421.9A: 3.145611 GeV  std: 0.028 %  minmax: [-0.044,+0.057] %

    data = dict()
    for i in range(len(currents)):
        if currents[i] in data:
            data[currents[i]].append(energies[i])
        else:
            data[currents[i]] = [energies[i], ]

    # print
    fstr = '{}: {:.6f} GeV  std: {:0.3f} %  minmax: [{:+0.3f},{:+0.3f}] %'
    print('Averages:')
    for cur in data:
        d = data[cur]
        avg = np.mean(d)
        std = np.std(d)
        de = 100*(d - avg)/avg
        print(fstr.format(cur, avg, 100*std/avg, min(de), max(de)))

    # plot
    for cur in data:
        d = data[cur]
        de = 100*(d - np.mean(d))/np.mean(d)
        plt.plot(de, 'o', label=cur)
    plt.legend()
    plt.grid()
    plt.xlabel('Magnet index')
    plt.ylabel('Energy deviation [%]')
    plt.show()

    # rx and px x magnet


def generate_inputs_reference_point_B2():
    """."""
    print('incomplete...')
    currents, magnets, energies, rx, px = load_search_reference_points_file()

    # c2e_B2 = {
    #     '381.7A': 2.852039,
    #     '401.8A': 3.000021,
    #     '421.9A': 3.147681,
    # }
    path_base = (
        '/home/fac_files/lnls-ima/si-dipoles-b2/model-08/analysis/'
        'hallprobe/production/refpoint/')

    for i in range(len(currents)):
        magnet = magnets[i]
        current = currents[i]
        path = path_base + magnet + '/' + current.replace('.', 'p') + '/'
        fname = get_fmap_files_B2(magnet, current)[0]
        f = hall.DoubleFMapAnalysis(magnet=magnet, fmap_fname=fname)
        # default_s_step = f.get_defaults()['traj_rk_s_step']
        print(path, f)





def run():
    """."""
    # hall.search_for_deflection_angle('B2')
    # hall.plot_results_search_deflection_angle('search-energies-shifted-x0-2.txt')
    # hall.generate_inputs(c2e_B2, '8p153', dipole_type='B2')
    # hall.load_analysis_result('x0-8p153mm/', 'B2', ('dangle', 'refrx', 'quad'))
    # hall.save_readme_files(c2e_B2, 'x0-8p153mm/', 'B2')
    # hall.calc_average_angles('x0-8p153mm/', 'B2')
    # hall.plot_trajectories('x0-8p153mm/', 'B2')

    # hall.plot_reference_trajectory('B2')
    hall.save_reference_trajectory('B2')



    # generate_inputs_B2()
    # seach_for_reference_point_B2()
    # load_search_reference_points_file()
    # plot_results_search_reference_points_B2()
    # generate_inputs_reference_point_B2()
    # load_analysis_result('x0-8p165mm/', ('dangle', 'refrx', 'quad'))
    # hall.load_analysis_result('x0-8p165mm/', ('dangle', 'refrx', 'quad'))
    # load_search_reference_points_file_relaxed()
    # plot_results_search_reference_points_relaxed_B2()
    # save_readme_files()

    # currents, magnets, energies = \
    #     load_search_deflection_angle_file(fname='search-energies-shifted-x0.txt')
    # e = [[], [], []]
    # for i in range(len(currents)):
    #     if currents[i] == '381.7A':
    #         e[0].append(energies[i])
    #     elif currents[i] == '401.8A':
    #         e[1].append(energies[i])
    #     elif currents[i] == '421.9A':
    #         e[2].append(energies[i])
    #
    # print(e[0])
    # print(np.mean(np.array(e[0])))
    # print()
    #
    # print(e[1])
    # print(np.mean(np.array(e[1])))
    # print()
    #
    # print(e[2])
    # print(np.mean(np.array(e[2])))
    # print()

run()
