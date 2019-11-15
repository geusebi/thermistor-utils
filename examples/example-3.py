import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from thermistor_utils import *

# Reported values of temperatures (Ts) and resistances (Rs)
# as repored by the datasheet
# from Murata Thermistor NCU18XH103D6SRB
Ts = tuple(range(-40, 151, 5))
Rs = (
    197_390, 149_390, 114_340, 88_381, 68_915, 54_166,
    42_889, 34_196, 27_445, 22_165, 18_010, 14_720,
    12_099, 10_000, 8_309, 6_939, 5_824, 4_911, 4_160,
    3_539, 3_024, 2_593, 2_233, 1_929, 1_673, 1_455,
    1_270, 1_112, 976, 860, 759, 673, 598,
    532, 476, 426, 383, 344, 311,
)

# Full temperature range scaled by 1 degree
temp_range = tuple(range(min(Ts), max(Ts) + 1))


def plot(title, Xs, Ys, label, outfile):
    """Utility function to plot subsequent charts."""
    plt.figure(figsize=(6, 3))
    plt.title(title)
    d_label = 'Datasheet reported values'

    ax = plt.gca()
    ax.yaxis.set_major_formatter(EngFormatter(unit='Ω'))

    plt.plot(Xs, Ys, "-", color='#999999', label=label)
    plt.plot(Ts, Rs, 'x', color='black', ms=3, label=d_label)

    plt.legend(loc='upper right')

    plt.savefig(outfile)
    plt.close()


# Steinhart & Hart converter
selected = (0, 25, 50)
tmin, tmid, tmax = selected
readings = tuple((t, Rs[Ts.index(t)], ) for t in selected)
sh_conv = SH_converter.from_points(readings)

# SH - temperature to resistance
plot(
    title="Steinhart & Hart (py) - temperature to resistance",
    label=f"SH_converter @ {tmin}-{tmid}-{tmax} C",
    Xs=temp_range,
    Ys=tuple(map(sh_conv.resistance, temp_range)),
    outfile="./sh-temp-res.png"
)

# SH - resistance to temperature
plot(
    title="Steinhart & Hart (py) - resistance to temperature",
    label=f"SH_converter @ {tmin}-{tmid}-{tmax} C",
    Xs=tuple(map(sh_conv.temperature, Rs)),
    Ys=Rs,
    outfile="./sh-res-temp.png"
)

# Beta converter
values = beta, R0, bmin, bmax = (3380, 10000, 25, 50)
beta_conv = Beta_converter(*values)

# Beta - temperature to resistance
plot(
    title="Beta (py) - temperature to resistance",
    label=f'Beta_converter ({beta}K @ {R0}ohm ({bmin}/{bmax})',
    Xs=temp_range,
    Ys=tuple(map(beta_conv.resistance, temp_range)),
    outfile="./beta-temp-res.png"
)

# Beta - resistance to temperature
plot(
    title="Beta (py) - resistance to temperature",
    label=f'Beta_converter ({beta}K @ {R0}ohm ({bmin}/{bmax})',
    Xs=tuple(map(beta_conv.temperature, Rs)),
    Ys=Rs,
    outfile="./beta-res-temp.png"
)
